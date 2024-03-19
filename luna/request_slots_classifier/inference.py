import torch

from transformers import AutoTokenizer

from luna.request_slots_classifier.model import RequestSlotsClassifier
from luna.request_slots_classifier.label import request_slots_labels


class RequestSlotsClassifierInference:
    def __init__(self):
        model_weights = torch.load(
            "luna/request_slots_classifier/checkpoints/request_slots_classifier.bin",
            map_location=torch.device("cpu"),
        )

        for key in list(model_weights):
            model_weights[key.replace("request_slots_classifier.", "")] = (
                model_weights.pop(key)
            )

        self.model = RequestSlotsClassifier(request_slots_labels)
        self.model.load_state_dict(model_weights)
        self.model.eval()
        self.tokenizer = AutoTokenizer.from_pretrained("distilroberta-base")

    def classify(self, text):
        input = self.tokenizer(
            text,
            max_length=125,
            padding="max_length",
            return_tensors="pt",
        )

        with torch.no_grad():
            _, logits = self.model(**input)

        probs = torch.nn.Sigmoid()(logits)
        rs = torch.where(probs >= 0.5, 1, 0).squeeze()

        return [
            label
            for idx, label in enumerate(request_slots_labels)
            if rs[idx].item() == 1
        ]
