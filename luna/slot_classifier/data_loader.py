
import torch
import pytorch_lightning as pl
import slot_labels

from pandas import DataFrame
from torch.utils.data import Dataset, DataLoader
from transformers import AutoTokenizer
from sklearn.model_selection import train_test_split
from data_process import get_input_examples


class FashionDataset(Dataset):
    def __init__(self, data: DataFrame, labels, tokenizer):
        self.tokenizer = tokenizer
        self.data = data
        self.cls_token = self.tokenizer.cls_token
        self.sep_token = self.tokenizer.sep_token
        self.unk_token = self.tokenizer.unk_token
        self.pad_token_id = self.tokenizer.pad_token_id
        self.max_seq_len = 50
        self.mask_padding_with_zero = True
        self.pad_token_label_id = 0
        self.labels = labels

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        data_row = self.data.iloc[idx]
        words = data_row['words']
        sls = []

        for s in data_row['slot'].split():
            sls.append(self.labels.index(s))

        tokens = []
        labels_ids = []

        for word, slot_label in zip(words, sls):
            word_tokens = self.tokenizer.tokenize(word)
            if not word_tokens:
                word_tokens = [self.unk_token]
            tokens.extend(word_tokens)
            labels_ids.extend(
                [int(slot_label)] + [self.pad_token_label_id] * (len(word_tokens) - 1))

        special_tokens_count = 2
        if len(tokens) > self.max_seq_len - special_tokens_count:
            tokens = tokens[:(self.max_seq_len - special_tokens_count)]
            labels_ids = labels_ids[:(self.max_seq_len - special_tokens_count)]

        tokens += [self.sep_token]
        labels_ids += [self.pad_token_label_id]

        tokens = [self.cls_token] + tokens
        labels_ids = [self.pad_token_label_id] + labels_ids

        input_ids = self.tokenizer.convert_tokens_to_ids(tokens)
        attention_mask = [
            1 if self.mask_padding_with_zero else 0] * len(input_ids)

        padding_length = self.max_seq_len - len(input_ids)
        input_ids = input_ids + ([self.pad_token_id] * padding_length)
        attention_mask = attention_mask + \
            ([0 if self.mask_padding_with_zero else 1] * padding_length)
        labels_ids = labels_ids + ([self.pad_token_label_id] * padding_length)

        return dict(
            input_ids=torch.tensor(input_ids),
            attention_mask=torch.tensor(attention_mask),
            labels_ids=torch.tensor(labels_ids),
        )


class FashionDataModule(pl.LightningDataModule):
    def __init__(self):
        super().__init__()

    def setup(self, stage):
        input_examples = get_input_examples()
        tokenizer = AutoTokenizer.from_pretrained('roberta-base')
        train_df, val_df = train_test_split(
            input_examples, test_size=0.1, random_state=42)
        self.batch_size = 32
        self.train_dataset = FashionDataset(train_df, slot_labels, tokenizer)
        self.val_dataset = FashionDataset(val_df, slot_labels, tokenizer)

    def train_dataloader(self):
        return DataLoader(self.train_dataset, batch_size=self.batch_size, shuffle=True)

    def val_dataloader(self):
        return DataLoader(self.val_dataset, batch_size=self.batch_size)
