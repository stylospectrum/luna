import torch
import torchmetrics
import pytorch_lightning as pl

from transformers import get_linear_schedule_with_warmup
from pytorch_lightning.callbacks import ModelCheckpoint, EarlyStopping
from pytorch_lightning.loggers import TensorBoardLogger

from luna.request_slots_classifier.model import RequestSlotsClassifier
from luna.request_slots_classifier.label import request_slots_labels
from luna.request_slots_classifier.data_loader import RequestSlotsDataModule


class RequestSlotsClassifierSystem(pl.LightningModule):
    def __init__(self, labels):
        super().__init__()

        self.request_slots_classifier = RequestSlotsClassifier(labels)
        self.lr = 5e-5
        self.weight_decay = 0.0
        self.adam_epsilon = 1e-8
        self.accuracy = torchmetrics.Accuracy(task="multilabel", num_labels=len(labels))

    def forward(self, input_ids, attention_mask, label_ids=None):
        return self.request_slots_classifier(input_ids, attention_mask, label_ids)

    def training_step(self, batch, batch_idx):
        loss, logits = self(**batch)
        accuracy = self.accuracy(logits, batch["label_ids"])

        self.log("train_loss", loss, prog_bar=True, logger=True, batch_size=len(batch))
        self.log(
            "train_accuracy",
            accuracy,
            prog_bar=True,
            logger=True,
            batch_size=len(batch),
        )

        return loss

    def validation_step(self, batch, batch_idx):
        loss, logits = self(**batch)
        accuracy = self.accuracy(logits, batch["label_ids"])

        self.log("val_loss", loss, prog_bar=True, logger=True, batch_size=len(batch))
        self.log(
            "val_accuracy", accuracy, prog_bar=True, logger=True, batch_size=len(batch)
        )

        return loss

    def configure_optimizers(self):
        no_decay = ["bias", "LayerNorm.weight"]
        optimizer_grouped_parameters = [
            {
                "params": [
                    p
                    for n, p in self.request_slots_classifier.model_transformers.named_parameters()
                    if not any(nd in n for nd in no_decay)
                ],
                "weight_decay": self.weight_decay,
            },
            {
                "params": [
                    p
                    for n, p in self.request_slots_classifier.model_transformers.named_parameters()
                    if any(nd in n for nd in no_decay)
                ],
                "weight_decay": 0.0,
            },
        ]
        optimizer = torch.optim.AdamW(
            optimizer_grouped_parameters, lr=self.lr, eps=self.adam_epsilon
        )
        scheduler = get_linear_schedule_with_warmup(
            optimizer,
            num_warmup_steps=0,
            num_training_steps=self.trainer.estimated_stepping_batches,
        )
        scheduler = {"scheduler": scheduler, "interval": "step", "frequency": 1}
        return [optimizer], [scheduler]


checkpoint_callback = ModelCheckpoint(
    dirpath="checkpoints",
    filename="request_slots_classifier",
    save_top_k=1,
    verbose=True,
    monitor="val_loss",
    mode="min",
)

logger = TensorBoardLogger("lightning_logs", name="request_slots_classifier")

early_stopping_callback = EarlyStopping(monitor="val_loss", patience=2)

trainer = pl.Trainer(
    logger=logger,
    callbacks=[early_stopping_callback, checkpoint_callback],
    max_epochs=4,
    accelerator="gpu",
    devices=1,
)

data_module = RequestSlotsDataModule(request_slots_labels)
model_system = RequestSlotsClassifierSystem(request_slots_labels)

trainer.fit(model_system, data_module)

check_point = torch.load("checkpoints/request_slots_classifier.ckpt")
torch.save(check_point["state_dict"], "checkpoints/request_slots_classifier.bin")
