import json
import pandas as pd

from sklearn.preprocessing import MultiLabelBinarizer

from luna.request_slots_classifier.label import request_slots_labels


def get_input_examples():
    with open('luna/data/simmc2.1_dials_dstc11_train.json') as j:
        raw = json.load(j)

    rs = []
    label_encoder = MultiLabelBinarizer(classes=request_slots_labels)

    for dialogue_data in raw['dialogue_data']:
        if dialogue_data['domain'] == 'fashion':
            for dialogue in dialogue_data['dialogue']:
                request_slots = dialogue['transcript_annotated']['act_attributes']['request_slots']
                if (dialogue['transcript_annotated']['act'] == 'ASK:GET' or dialogue['transcript_annotated']['act'] == 'REQUEST:COMPARE') and len(request_slots) > 0:
                    rs.append({
                        'text': dialogue['transcript'],
                        'request_slots': request_slots
                    })

    df = pd.DataFrame(rs)
    label_ids = label_encoder.fit_transform(df['request_slots'])
    label_ids = label_ids.T

    for idx, label in enumerate(request_slots_labels):
        df[label] = label_ids[idx]

    return df
