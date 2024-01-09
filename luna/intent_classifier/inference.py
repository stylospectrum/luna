import torch

from transformers import AutoTokenizer

from luna.intent_classifier.model import IntentClassifier
from luna.intent_classifier.label import intent_labels


class IntentClassifierInference:
    def __init__(self):
        model_weights = torch.load(
            'luna/intent_classifier/checkpoints/intent_classifier.bin', map_location=torch.device('cpu'))

        for key in list(model_weights):
            model_weights[key.replace(
                "intent_classifier.", "")] = model_weights.pop(key)

        self.model = IntentClassifier(intent_labels)
        self.model.load_state_dict(model_weights)
        self.model.eval()
        self.tokenizer = AutoTokenizer.from_pretrained('distilroberta-base')

    def classify(self, text):
        input = self.tokenizer(
            text,
            max_length=125,
            padding="max_length",
            return_tensors='pt',
        )

        with torch.no_grad():
            _, logits = self.model(**input)
        _, predicted = torch.max(logits.cpu(), dim=1)

        return intent_labels[predicted]
