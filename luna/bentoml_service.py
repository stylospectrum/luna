import json
import random
import redis
import bentoml

from pandas import Series
from bentoml.io import JSON, NumpyNdarray, PandasSeries, Text
from pydantic import BaseModel

from luna.config.settings import settings
from luna.intent_classifier.label import intent_labels
from luna.request_slots_classifier.label import request_slots_labels
from luna.runners.classifier import classifier_runner
from luna.runners.generator import generator_runner
from luna.response.collect_user_preference import collect_user_preference
from luna.response.answer_request_slots import answer_request_slots
from luna.response.suggest_products import suggest_products


class MessageModel(BaseModel):
    user_id: str
    content: str


redis_port = int(settings.REDIS_PORT)
r = redis.Redis(host='localhost', port=redis_port, decode_responses=True)
svc = bentoml.Service('luna', runners=[generator_runner, classifier_runner])

with open('luna/data/products.json') as f:
    products = json.load(f)

not_intent_buy_labels = intent_labels.copy()
not_intent_buy_labels.remove('buy')
not_intent_buy_labels.remove('ask')
not_intent_buy_labels.remove('add_to_cart')


@svc.api(input=JSON(pydantic_model=MessageModel), output=JSON())
async def predict(message: MessageModel) -> dict[str, str]:
    content: str = message.model_dump()['content']
    user_id: str = message.model_dump()['user_id']
    response = 'I don\'t understand what you mean.'

    info = r.hgetall(f'luna:{user_id}')
    context = '' if 'context' not in info else info['context']
    user_preferences = {} if 'user_preferences' not in info else json.loads(
        info['user_preferences'])
    intent = await classifier_runner.classify.async_run(content, 'intent')

    if (intent in not_intent_buy_labels and (context == '' or context is None)) or intent == 'add_to_cart':
        response = await generator_runner.generate.async_run(content)

        if intent == 'add_to_cart':
            r.delete(f'luna:{user_id}')
            context = ''

    if intent == 'buy':
        r.hset(f'luna:{user_id}', 'context', 'buy')
        context = 'buy'

    if context == 'buy':
        slot: dict[str, str] = await classifier_runner.classify.async_run(content, 'slot')
        bot_active = random.choice(
            ['collect_user_preference', 'suggest_products'])
        suggested_products = r.hget(f'luna:{user_id}', 'suggested_products')
        suggested_products = [] if suggested_products is None else json.loads(
            suggested_products)

        for request_slot in request_slots_labels:
            if request_slot in slot:
                bot_active = 'suggest_products'
                break

        if intent == 'ask':
            request_slots: list[str] = await classifier_runner.classify.async_run(content)
            response = answer_request_slots(
                request_slots, slot, suggested_products)
        else:
            if bot_active == 'collect_user_preference' or len(user_preferences) > 0:
                if intent == 'buy' and len(user_preferences) == 0:
                    text = collect_user_preference(slot)

                    for key, value in slot.items():
                        if key not in request_slots_labels:
                            user_preferences[key] = value
                            text = text.replace(f'[{key}]', value)

                    r.hset(f'luna:{user_id}', 'user_preferences',
                           json.dumps(user_preferences))
                    response = text
                else:
                    for key, value in slot.items():
                        if key not in request_slots_labels:
                            user_preferences[key] = value

                    if len(user_preferences) == 4:
                        res, sps = suggest_products(
                            user_preferences, products, active='ask')
                        r.hset(f'luna:{user_id}',
                               'suggested_products', json.dumps(sps))
                        response = res
                    else:
                        r.hset(f'luna:{user_id}', 'user_preferences',
                               json.dumps(user_preferences))
                        text = collect_user_preference(user_preferences)

                        for key, value in user_preferences.items():
                            text = text.replace(f'[{key}]', value)

                        response = text
            else:
                res, sps = suggest_products(slot, products)
                r.hset(f'luna:{user_id}',
                       'suggested_products', json.dumps(sps))
                response = res

    return {
        'content': response
    }


@svc.api(input=PandasSeries(), output=NumpyNdarray())
async def get_embeddings(texts: Series):
    texts = texts.to_list()
    texts = list(filter(lambda x: x != '', list(texts[0])))
    embeddings = await classifier_runner.classify.async_run(texts, 'intent', 'get_embeddings')
    return embeddings.numpy()

@svc.api(input=Text(), output=Text())
async def classify(text: str):
    return await classifier_runner.classify.async_run(text, 'intent')