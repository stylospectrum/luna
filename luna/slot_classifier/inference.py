import spacy
import torch
import numpy as np

from transformers import AutoTokenizer
from luna.slot_classifier import slot_labels
from luna.slot_classifier.model import SlotClassifier


class SlotClassifierInference:
    def __init__(self):
        model_weights = torch.load(
            'luna/slot_classifier/checkpoints/slot_classifier.bin', map_location=torch.device('cpu'))
        for key in list(model_weights):
            model_weights[key.replace(
                "slot_classifier.", "")] = model_weights.pop(key)

        self.model = SlotClassifier(slot_labels)
        self.model.load_state_dict(model_weights)
        self.model.eval()
        self.tokenizer = AutoTokenizer.from_pretrained('roberta-base')
        self.nlp = spacy.load('en_core_web_sm')

    def predict(self, text: str):
        cls_token = self.tokenizer.cls_token
        sep_token = self.tokenizer.sep_token
        unk_token = self.tokenizer.unk_token
        pad_token_id = self.tokenizer.pad_token_id
        doc = self.nlp(text)
        words = [tok.lemma_ for tok in doc if not tok.is_punct]
        max_seq_len = 50
        mask_padding_with_zero = True
        pad_token_label_id = 0
        rs = []

        tokens = []
        label_mask = []
        for word in words:
            word_tokens = self.tokenizer.tokenize(word)
            if not word_tokens:
                word_tokens = [unk_token]
            tokens.extend(word_tokens)
            label_mask.extend([pad_token_label_id + 1] +
                              [pad_token_label_id] * (len(word_tokens) - 1))

        special_tokens_count = 2
        if len(tokens) > max_seq_len - special_tokens_count:
            tokens = tokens[:(max_seq_len - special_tokens_count)]
            label_mask = label_mask[:(max_seq_len - special_tokens_count)]

        tokens += [sep_token]
        label_mask += [pad_token_label_id]

        tokens = [cls_token] + tokens
        label_mask = [pad_token_label_id] + label_mask

        input_ids = self.tokenizer.convert_tokens_to_ids(tokens)
        attention_mask = [1 if mask_padding_with_zero else 0] * len(input_ids)

        padding_length = max_seq_len - len(input_ids)

        input_ids = torch.tensor(
            input_ids + ([pad_token_id] * padding_length)).unsqueeze(0)
        attention_mask = torch.tensor(
            attention_mask + ([0 if mask_padding_with_zero else 1] * padding_length)).unsqueeze(0)
        label_mask = torch.tensor(
            label_mask + ([pad_token_label_id] * padding_length)).numpy()

        with torch.no_grad():
            _, logits = self.model(input_ids=input_ids,
                                   attention_mask=attention_mask)

        preds = np.argmax(logits.detach().cpu().numpy(), axis=2)

        slot_label_map = {i: label for i, label in enumerate(slot_labels)}
        preds_list = [[] for _ in range(preds.shape[0])]

        for i in range(preds.shape[1]):
            if label_mask[i] != pad_token_label_id:
                preds_list.append(slot_label_map[preds[0][i]])

        preds_list.pop(0)

        for word, pred in zip(words, preds_list):
            if pred != 'O':
                rs.append({
                    'word': word,
                    'label': pred
                })

        return rs
