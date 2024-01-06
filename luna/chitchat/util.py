import pandas as pd
import torch

from itertools import chain
from transformers import AutoTokenizer


def featurize(question_id, answer_id, tokenizer, with_eos=True):
    bos = tokenizer.convert_tokens_to_ids('<bos>')
    eos = tokenizer.convert_tokens_to_ids('<eos>')
    user = tokenizer.convert_tokens_to_ids('<user>')
    system = tokenizer.convert_tokens_to_ids('<system>')

    instance = {}

    sequence = [[bos]] + [question_id] + \
        [[system] + answer_id + ([eos] if with_eos else [])]
    sequence = [sequence[0]] + [[user if (len(sequence) - i) % 2 else system] +
                                s for i, s in enumerate(sequence[1:-1])] + sequence[-1:]

    l = len([i for s in sequence for i in s])
    ctx = 128

    if l > ctx:
        i = 1
        while l > ctx:
            d = sequence.pop(i)
            l -= len(d)

    instance["input_ids"] = list(chain(*sequence))
    instance["token_type_ids"] = [user if i % 2 or i ==
                                  0 else system for i, s in enumerate(sequence) for _ in s]
    instance["labels"] = ([-100] * sum(len(s)
                          for s in sequence[:-1])) + [-100] + sequence[-1][1:]

    return instance


def get_features():
    tokenizer = AutoTokenizer.from_pretrained("distilgpt2")
    tokenizer.add_special_tokens({'additional_special_tokens': [
        '<pad>', '<eos>', '<bos>', '<user>', '<system>']})
    df = pd.read_csv('luna/data/qna_chitchat_friendly.tsv', sep='\t')
    df = df.drop(['Source', 'Metadata'], axis=1)
    rs = []
    features = [f for f in [featurize(tokenizer.encode(row['Question']), tokenizer.encode(
        row['Answer']), tokenizer) for index, row in df.iterrows()] if f is not None]
    max_l = max([len(feature['input_ids']) for feature in features])
    padding_id = tokenizer.convert_tokens_to_ids('<pad>')

    for feature in features:
        temp_dict = {}
        for name in feature.keys():
            temp = feature[name] + [padding_id if name !=
                                    "labels" else -100] * (max_l - len(feature[name]))
            temp_dict[name] = torch.tensor(temp)
        rs.append(temp_dict)

    return rs
