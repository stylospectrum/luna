import pytorch_lightning as pl

from torch.utils.data import Dataset, DataLoader
from sklearn.model_selection import train_test_split

from luna.generator.util import get_features


class ChitChatDataset(Dataset):
    def __init__(self, data):
        self.data = data

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        data_row = self.data[idx]

        return dict(
            input_ids=data_row["input_ids"],
            token_type_ids=data_row["token_type_ids"],
            labels=data_row["labels"],
        )


class ChitChatDataModule(pl.LightningDataModule):
    def __init__(self):
        super().__init__()

    def setup(self, stage: str):
        features = get_features()
        train_df, val_df = train_test_split(features, test_size=0.2, random_state=42)
        self.train_dataset = ChitChatDataset(train_df)
        self.val_dataset = ChitChatDataset(val_df)
        self.batch_size = 32

    def train_dataloader(self):
        return DataLoader(self.train_dataset, batch_size=self.batch_size, shuffle=True)

    def val_dataloader(self):
        return DataLoader(self.val_dataset, batch_size=self.batch_size)
