import pytorch_lightning as pl
import torch

from pytorch_lightning.callbacks import ModelCheckpoint, EarlyStopping
from pytorch_lightning.loggers import TensorBoardLogger
from transformers import get_linear_schedule_with_warmup
from seqeval.metrics import f1_score
from luna.slot_classifier.data_loader import FashionDataModule
from luna.slot_classifier.model import SlotClassifier
from luna.slot_classifier.label import slot_labels


class SlotClassifierSystem(pl.LightningModule):
    def __init__(self, labels):
        super().__init__()
        self.slot_classifier = SlotClassifier(labels)
        self.labels = labels
        self.lr = 2e-5
        self.adam_epsilon = 1e-8
        self.weight_decay = 0.0

    def forward(self, input_ids, attention_mask, labels_ids):
        return self.slot_classifier(input_ids, attention_mask, labels_ids)

    def training_step(self, batch, batch_idx):
        loss, _ = self(**batch)
        self.log("train_loss", loss, prog_bar=True, logger=True, batch_size=len(batch))
        return loss

    def validation_step(self, batch, batch_idx):
        loss, logits = self(**batch)
        preds = torch.argmax(logits.detach().cpu(), dim=2).numpy()
        labels_ids = batch["labels_ids"].detach().cpu().numpy()

        label_map = {i: label for i, label in enumerate(self.labels)}
        y_hat = [[] for _ in range(labels_ids.shape[0])]
        y = [[] for _ in range(labels_ids.shape[0])]

        for i in range(labels_ids.shape[0]):
            for j in range(labels_ids.shape[1]):
                if labels_ids[i, j] != 0:
                    y_hat[i].append(label_map[preds[i][j]])
                    y[i].append(label_map[labels_ids[i][j]])

        self.log("val_loss", loss, prog_bar=True, logger=True, batch_size=len(batch))
        self.log(
            "val_f1",
            f1_score(y, y_hat),
            prog_bar=True,
            logger=True,
            batch_size=len(batch),
        )

    def configure_optimizers(self):
        no_decay = ["bias", "LayerNorm.weight"]
        optimizer_grouped_parameters = [
            {
                "params": [
                    p
                    for n, p in self.slot_classifier.model_transformers.named_parameters()
                    if not any(nd in n for nd in no_decay)
                ],
                "weight_decay": self.weight_decay,
            },
            {
                "params": [
                    p
                    for n, p in self.slot_classifier.model_transformers.named_parameters()
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
    filename="slot_classifier",
    save_top_k=1,
    verbose=True,
    monitor="val_loss",
    mode="min",
)

logger = TensorBoardLogger("lightning_logs", name="slot_classifier")

early_stopping_callback = EarlyStopping(monitor="val_loss", patience=2)

trainer = pl.Trainer(
    logger=logger,
    callbacks=[early_stopping_callback, checkpoint_callback],
    max_epochs=4,
    accelerator="gpu",
    devices=1,
)

data_module = FashionDataModule()
model_system = SlotClassifierSystem(slot_labels)

trainer.fit(model_system, data_module)

check_point = torch.load("checkpoints/slot_classifier.ckpt")
torch.save(check_point["state_dict"], "checkpoints/slot_classifier.bin")
