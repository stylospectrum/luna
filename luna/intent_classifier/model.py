import torch
import torch.nn as nn

from transformers import AutoModel


class IntentClassifier(torch.nn.Module):
    def __init__(self, labels):
        super().__init__()

        self.model_transformers = AutoModel.from_pretrained("distilroberta-base")
        self.dropout = nn.Dropout(0.1)
        self.linear = nn.Linear(self.model_transformers.config.hidden_size, len(labels))
        self.criterion = nn.CrossEntropyLoss()

    def forward(self, input_ids, attention_mask, label_ids=None, return_features=False):
        x = self.model_transformers(input_ids=input_ids, attention_mask=attention_mask)

        if return_features:
            return x.pooler_output

        x = self.dropout(x.pooler_output)
        logits = self.linear(x)
        loss = 0

        if label_ids is not None:
            loss = self.criterion(logits, label_ids.long())

        return loss, logits
