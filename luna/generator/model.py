import torch

from transformers import GPT2LMHeadModel, AutoTokenizer


class ChitChat(torch.nn.Module):
    def __init__(self):
        super().__init__()

        tokenizer = AutoTokenizer.from_pretrained("gpt2")
        tokenizer.add_special_tokens(
            {
                "additional_special_tokens": [
                    "<pad>",
                    "<eos>",
                    "<bos>",
                    "<user>",
                    "<system>",
                ]
            }
        )
        self.gpt2 = GPT2LMHeadModel.from_pretrained("gpt2")
        self.gpt2.resize_token_embeddings(len(tokenizer))

    def forward(self, input_ids, token_type_ids, labels=None):
        return self.gpt2(
            input_ids=input_ids, token_type_ids=token_type_ids, labels=labels
        )
