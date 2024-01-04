import torch

from transformers import AutoModel


class SlotClassifier(torch.nn.Module):
    def __init__(self, labels):
        super().__init__()

        self.model_transformers = AutoModel.from_pretrained('roberta-base')
        self.labels = labels
        self.num_labels = len(self.labels)
        self.dropout = torch.nn.Dropout(0.1)
        self.linear = torch.nn.Linear(
            self.model_transformers.config.hidden_size, self.num_labels)

    def forward(self, input_ids, attention_mask, labels_ids=None):
        x = self.model_transformers(input_ids, attention_mask=attention_mask)
        x = self.dropout(x.last_hidden_state)
        logits = self.linear(x)
        loss = None

        if labels_ids is not None:
            loss_fct = torch.nn.CrossEntropyLoss(ignore_index=0)
            if attention_mask is not None:
                active_loss = attention_mask.view(-1) == 1
                active_logits = logits.view(-1, self.num_labels)[active_loss]
                active_labels = labels_ids.view(-1)[active_loss]
                loss = loss_fct(active_logits, active_labels)
            else:
                loss = loss_fct(logits.view(-1, self.num_labels),
                                labels_ids.view(-1))

        return loss, logits
