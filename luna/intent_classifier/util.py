import json
import pandas as pd

def get_fashion_dataset():
  with open('luna/data/simmc2.1_dials_dstc11_train.json') as j:
    raw = json.load(j)

  rs = []
  intent_map = {
    'REQUEST:GET': 'buy',
    'ASK:GET': 'ask',
    'REQUEST:COMPARE': 'compare'
  }

  for dialogue_data in raw['dialogue_data']:
    if dialogue_data['domain'] == 'fashion':
      for dialogue in dialogue_data['dialogue']:
        if dialogue['transcript_annotated']['act'] == 'REQUEST:GET' or dialogue['transcript_annotated']['act'] == 'ASK:GET' or dialogue['transcript_annotated']['act'] == 'REQUEST:COMPARE':
          rs.append({
              'text': dialogue['transcript'],
              'intent': intent_map[dialogue['transcript_annotated']['act']]
          })
  return rs

def get_input_examples():
  fashion_dataset = pd.DataFrame(get_fashion_dataset())
  chit_chat_dataset = pd.read_csv('qna_chitchat_friendly.tsv', sep='\t')
  chit_chat_dataset = chit_chat_dataset.drop(['Answer', 'Source', 'Metadata'], axis=1)
  chit_chat_dataset['intent'] = ['other' for _ in range(len(chit_chat_dataset['Question']))]
  chit_chat_dataset.rename(columns={'Question': 'text'}, inplace=True)
  return pd.concat([fashion_dataset, chit_chat_dataset], ignore_index=True)