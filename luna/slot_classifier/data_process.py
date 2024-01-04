import spacy
import itertools
import re
import pandas as pd
import json

with open('../data/simmc2.1_dials_dstc11_train.json') as j:
    raw_data = json.load(j)


class SpacyTokenizer:
    def __init__(self):
        self.nlp = spacy.load('en_core_web_sm')

    def tokenize(self, text):
        doc = self.nlp(text)
        tokens = [tok.lemma_ for tok in doc if not tok.is_punct]
        return tokens


def remove_unnecessary_sentence(dialogue, slots, nlp):
    doc = nlp(dialogue)
    result = []
    for sent in doc.sents:
        count = 0
        for v in slots.values():
            if v in sent.text:
                count += 1
        if count > 0:
            result.append(sent.text)
    return '. '.join(result)


def get_raw_slot_labels():
    slots = [dialogue['transcript_annotated']['act_attributes']['slot_values'] for dialogue_data in raw_data['dialogue_data']
             for dialogue in dialogue_data['dialogue'] if dialogue['transcript_annotated']['act'] == 'REQUEST:GET']
    slot_labels = [list(slot.keys()) for slot in slots]
    flattened_slot_labels = itertools.chain(*slot_labels)

    return list(dict.fromkeys(flattened_slot_labels))


def process_text(text):
    if '&' in text:
        text = re.sub('&', 'and', text)
    text = re.sub(r"\W$", "", text)
    text = re.sub("shortsleeved", "short sleeved", text)
    return text.lower()


def process_tok(tok):
    return re.sub(r"\W$", "", tok)


def process_slot_value(words, slot_label, slot_value):
    if slot_label == 'customerReview' and slot_value == 'good':
        if set(['well', 'rate']).issubset(set(words)):
            return 'well rate'
        if set(['highly', 'rate']).issubset(set(words)):
            return 'highly rate'
        if set(['high', 'rating']).issubset(set(words)):
            return 'high rating'
        if set(['decent', 'rating']).issubset(set(words)):
            return 'decent rating'
        if set(['high', 'review']).issubset(set(words)):
            return 'high review'
        if set(['solid', 'rating']).issubset(set(words)):
            return 'solid rating'

    if slot_label == 'pattern' and 'stripe' in slot_value:
        if set(['striped']).issubset(set(words)):
            return 'striped'
        if set(['stripe']).issubset(set(words)):
            return 'stripe'

    if slot_label == 'type' and slot_value == 'tshirt':
        if set(['shirt']).issubset(set(words)) and not set(['t']).issubset(set(words)):
            return 'shirt'
        if set(['t', 'shirt']).issubset(set(words)):
            return 'shirt'
        if set(['tee']).issubset(set(words)):
            return 'tee'

    if slot_label == 'type' and slot_value == 'coat':
        if set(['blazer']).issubset(set(words)):
            return 'blazer'
        if set(['jacket']).issubset(set(words)):
            return 'jacket'

    if slot_label == 'price' and slot_value == 'expensive':
        if set(['pricey']).issubset(set(words)):
            return 'pricey'
        if set(['high', 'price']).issubset(set(words)) and not set(['high', 'in', 'price']).issubset(set(words)):
            return 'high price'
        if set(['high', 'end']).issubset(set(words)):
            return 'high end'

    if slot_label == 'price' and slot_value == 'cheap':
        if set(['affordable', 'price']).issubset(set(words)):
            return 'affordable'
        if set(['inexpensive']).issubset(set(words)):
            return 'inexpensive'

    if set(['extra', 'small']).issubset(set(words)) and slot_label == 'size' and (slot_value == 'XS' or slot_value == 'xs'):
        return 'extra small'

    if set(['small']).issubset(set(words)) and not set(['extra']).issubset(set(words)) and slot_label == 'size' and (slot_value == 's' or slot_value == 'S'):
        return 'small'

    if set(['medium']).issubset(set(words)) and slot_label == 'size' and (slot_value == 'M' or slot_value == 'm'):
        return 'medium'

    if set(['large']).issubset(set(words)) and not set(['extra']).issubset(set(words)) and slot_label == 'size' and (slot_value == 'l' or slot_value == 'L'):
        return 'large'

    if set(['extra', 'large']).issubset(set(words)) and slot_label == 'size' and (slot_value == 'XL' or slot_value == 'xl'):
        return 'extra large'

    if set(['shirt']).issubset(set(words)) and slot_label == 'type' and slot_value == 'blouse':
        return 'shirt'

    if set(['pant']).issubset(set(words)) and slot_label == 'type' and (slot_value == 'trousers' or slot_value == 'jeans' or slot_value == 'joggers'):
        return 'pant'

    if set(['affordably', 'price']).issubset(set(words)) and slot_label == 'price' and slot_value == 'affordable':
        return 'affordably'

    if set(['budget', 'friendly']).issubset(set(words)) and slot_label == 'price' and (slot_value == 'affordable' or slot_value == 'cheap'):
        return 'budget friendly'

    if set(['gray']).issubset(set(words)) and slot_label == 'color' and slot_value == 'grey':
        return 'gray'

    if set(['long', 'sleeve']).issubset(set(words)) and slot_label == 'sleeveLength' and slot_value == 'full':
        return 'long'

    return slot_value


def get_input_examples():
    tokenizer = SpacyTokenizer()
    result = []
    slot_labels = get_raw_slot_labels()

    for dialogue_data in raw_data['dialogue_data']:
        if dialogue_data['domain'] == 'fashion':
            for dialogue in dialogue_data['dialogue']:
                if dialogue['transcript_annotated']['act'] == 'REQUEST:GET':
                    s = ''
                    slots = dialogue['transcript_annotated']['act_attributes']['slot_values']
                    text = remove_unnecessary_sentence(
                        dialogue['transcript'], slots, tokenizer.nlp)
                    words = tokenizer.tokenize(process_text(text))
                    new_slots = slots.copy()

                    for word in words:
                        word = process_tok(word)

                        temp_slot = {
                            'text': None
                        }

                        for slot_label, slot_value in slots.items():
                            if slot_label in slot_labels:
                                slot_value = process_slot_value(
                                    words, slot_label, process_text(slot_value))
                                slot_toks = tokenizer.tokenize(slot_value) if isinstance(
                                    slot_value, str) else [str(slot_value)]
                                new_slots[slot_label] = slot_value

                                for slot_tok_idx, slot_tok in enumerate(slot_toks):
                                    slot_tok = process_tok(slot_tok)

                                    if slot_tok == word:
                                        temp_slot = {
                                            'label': slot_label,
                                            'text': slot_tok,
                                            'idx': slot_tok_idx
                                        }

                        if temp_slot['text'] == word:
                            if temp_slot['idx'] == 0:
                                s += f"B-{temp_slot['label']} "
                            else:
                                s += f"I-{temp_slot['label']} "
                        else:
                            s += 'O '

                    result.append({
                        'text': text,
                        'words': words,
                        'slots': new_slots,
                        'slot': s.strip()
                    })

    df = pd.DataFrame(result)
    df = df[df['slot'].str.find('B-') > -1]

    return df
