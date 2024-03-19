import torch

from transformers import AutoModel


class RequestSlotsClassifier(torch.nn.Module):
    def __init__(self, labels):
        super().__init__()

        self.model_transformers = AutoModel.from_pretrained(
            "distilroberta-base", return_dict=True
        )
        self.dropout = torch.nn.Dropout(0.1)
        self.linear = torch.nn.Linear(
            self.model_transformers.config.hidden_size, len(labels)
        )
        self.criterion = torch.nn.BCEWithLogitsLoss()

    def forward(self, input_ids, attention_mask, label_ids=None):
        x = self.model_transformers(input_ids=input_ids, attention_mask=attention_mask)
        x = self.dropout(x.pooler_output)
        logits = self.linear(x)
        loss = 0

        if label_ids is not None:
            loss = self.criterion(logits, label_ids)

        return loss, logits
