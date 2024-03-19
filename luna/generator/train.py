import pytorch_lightning as pl
import torch

from pytorch_lightning.callbacks import ModelCheckpoint, EarlyStopping
from pytorch_lightning.loggers import TensorBoardLogger

from luna.generator.model import ChitChat
from luna.generator.data_loader import ChitChatDataModule


class ChitChatSystem(pl.LightningModule):
    def __init__(self):
        super().__init__()

        self.chitchat = ChitChat()
        self.lr = 6.25e-5

    def forward(self, input_ids, token_type_ids, labels=None):
        return self.chitchat(
            input_ids=input_ids, token_type_ids=token_type_ids, labels=labels
        )

    def training_step(self, batch, batch_idx):
        outputs = self(**batch)
        self.log("train_loss", outputs.loss)
        return outputs.loss

    def validation_step(self, batch, batch_idx):
        outputs = self(**batch)
        self.log("val_loss", outputs.loss)

    def configure_optimizers(self):
        optimizer = torch.optim.AdamW(self.parameters(), lr=self.lr)
        return optimizer


checkpoint_callback = ModelCheckpoint(
    dirpath="checkpoints",
    filename="chitchat",
    save_top_k=1,
    verbose=True,
    monitor="val_loss",
    mode="min",
)

logger = TensorBoardLogger("/content/lightning_logs", name="chitchat")

early_stopping_callback = EarlyStopping(monitor="val_loss", patience=2)

trainer = pl.Trainer(
    logger=logger,
    callbacks=[early_stopping_callback, checkpoint_callback],
    max_epochs=10,
    accelerator="gpu",
    devices=1,
)

data_module = ChitChatDataModule()
model_system = ChitChatSystem()
trainer.fit(model_system, data_module)

check_point = torch.load("checkpoints/chitchat.ckpt")
torch.save(check_point["state_dict"], "checkpoints/chitchat.bin")
