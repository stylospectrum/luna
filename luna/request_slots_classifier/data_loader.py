import numpy as np
import pandas as pd
import torch
import pytorch_lightning as pl

from torch.utils.data import Dataset, DataLoader
from sklearn.model_selection import train_test_split
from transformers import AutoTokenizer

from luna.request_slots_classifier.util import get_input_examples


class RequestSlotsDataset(Dataset):
    def __init__(self, data: pd.DataFrame, labels, tokenizer):
        self.data = data
        self.num_labels = len(labels)
        self.tokenizer = tokenizer

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        data_row = self.data.iloc[idx]
        sentence = data_row['text']

        encoding = self.tokenizer(
            sentence,
            max_length=125,
            padding="max_length",
            return_tensors='pt',
        )

        return dict(
            input_ids=encoding["input_ids"].flatten(),
            attention_mask=encoding["attention_mask"].flatten(),
            label_ids=torch.tensor(
                data_row[-self.num_labels:].values.astype(np.float32))
        )


class RequestSlotsDataModule(pl.LightningDataModule):
    def __init__(self, labels):
        super().__init__()
        self.labels = labels

    def setup(self, stage: str):
        input_examples = get_input_examples()
        tokenizer = AutoTokenizer.from_pretrained("distilroberta-base")
        train_df, val_df = train_test_split(
            input_examples, test_size=0.2, random_state=42)
        self.train_dataset = RequestSlotsDataset(
            train_df, self.labels, tokenizer)
        self.val_dataset = RequestSlotsDataset(val_df, self.labels, tokenizer)
        self.batch_size = 64

    def train_dataloader(self):
        return DataLoader(self.train_dataset, batch_size=self.batch_size, shuffle=True)

    def val_dataloader(self):
        return DataLoader(self.val_dataset, batch_size=self.batch_size)
