import torch
import torch.nn.functional as F

from transformers import AutoTokenizer

from luna.generator.model import ChitChat
from luna.generator.util import featurize


class ChitChatInference:
    def __init__(self):
        model_weights = torch.load(
            'luna/generator/checkpoints/generator.bin', map_location=torch.device('cpu'))

        for key in list(model_weights):
            model_weights[key.replace("chitchat.", "")
                          ] = model_weights.pop(key)

        self.model = ChitChat()
        self.model.load_state_dict(model_weights)
        self.model.eval()
        self.tokenizer = AutoTokenizer.from_pretrained("gpt2")
        self.tokenizer.add_special_tokens(
            {'additional_special_tokens': ['<pad>', '<eos>', '<bos>', '<user>', '<system>']})
        self.eos = [self.tokenizer.convert_tokens_to_ids('<eos>')]

    def generate(self, text: str):
        i = 0
        current_output = []
        question_id = self.tokenizer.encode(text)

        while i < 100:
            instance = featurize(question_id, current_output,
                                 self.tokenizer, with_eos=False)
            input_ids = torch.tensor(instance["input_ids"]).unsqueeze(0)
            token_type_ids = torch.tensor(
                instance["token_type_ids"]).unsqueeze(0)

            with torch.no_grad():
                outputs = self.model(input_ids=input_ids,
                                     token_type_ids=token_type_ids)

            logits = outputs.logits[0, -1, :] / 0.9
            filter_value = -float('Inf')
            threshold = -float('Inf')

            sorted_logits, sorted_indices = torch.sort(logits, descending=True)
            cumulative_probabilities = torch.cumsum(
                F.softmax(sorted_logits, dim=-1), dim=-1)
            sorted_indices_to_remove = cumulative_probabilities > 0.8
            sorted_indices_to_remove[...,
                                     1:] = sorted_indices_to_remove[..., :-1].clone()
            sorted_indices_to_remove[..., 0] = 0

            indices_to_remove = sorted_indices[sorted_indices_to_remove]
            logits[indices_to_remove] = filter_value
            indices_to_remove = logits < threshold
            logits[indices_to_remove] = filter_value

            probs = F.softmax(logits, dim=-1)
            prev = torch.multinomial(probs, 1)

            if i < 1 and prev.item() in self.eos:
                b = 0
                while prev.item() in self.eos:
                    if b == 3:
                        break
                    prev = torch.multinomial(probs, num_samples=1)
                    b += 1

            if prev.item() in self.eos:
                break

            current_output.append(prev.item())
            i += 1

        return self.tokenizer.decode(current_output, skip_special_tokens=False)
