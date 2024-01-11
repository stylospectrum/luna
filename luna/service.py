import json
import random
import redis
import bentoml
import os


from bentoml.io import JSON, Text
from pydantic import BaseModel
from dotenv import load_dotenv

from luna.runners.classifier import classifier_runner
from luna.runners.chitchat import chitchat_runner
from luna.response.collect_user_preference import collect_user_preference
from luna.response.answer_request_slots import answer_request_slots
from luna.response.suggest_products import suggest_products

load_dotenv()


class MessageModel(BaseModel):
    user_id: str
    content: str


redis_port = int(os.environ.get('REDIS_PORT'))
r = redis.Redis(host='localhost', port=redis_port, decode_responses=True)
svc = bentoml.Service('luna', runners=[chitchat_runner, classifier_runner])

with open('luna/data/products.json') as f:
    products = json.load(f)


@svc.api(input=JSON(pydantic_model=MessageModel), output=Text())
async def predict(message: MessageModel) -> dict[str, str]:
    content: str = message.model_dump()['content']
    user_id: str = message.model_dump()['user_id']

    info = r.hgetall(f'luna:{user_id}')
    context = '' if 'context' not in info else info['context']
    user_preferences = {} if 'user_preferences' not in info else json.loads(
        info['user_preferences'])
    intent = await classifier_runner.classify.async_run(content, 'intent')

    if intent == 'chitchat' and (context == '' or context is None):
        return await chitchat_runner.generate.async_run(content)

    if intent == 'add-to-cart':
        r.delete(f'luna:{user_id}')
        return 'Your item has been added to cart.'

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

        if intent == 'ask':
            request_slots: list[str] = await classifier_runner.classify.async_run(content)

            return answer_request_slots(request_slots, slot, suggested_products)

        else:
            if (bot_active == 'collect_user_preference' or len(user_preferences) > 0):
                if intent == 'buy':
                    text = collect_user_preference(slot)

                    for key, value in slot.items():
                        user_preferences[key] = value
                        text = text.replace(f'[{key}]', value)

                    r.hset(f'luna:{user_id}', 'user_preferences',
                           json.dumps(user_preferences))
                    return text
                else:
                    for key, value in slot.items():
                        user_preferences[key] = value

                    if len(user_preferences) == 4:
                        response, sps = suggest_products(
                            user_preferences, products, active='ask')
                        r.hset(f'luna:{user_id}',
                               'suggested_products', json.dumps(sps))
                        return response

                    r.hset(f'luna:{user_id}', 'user_preferences',
                           json.dumps(user_preferences))
                    text = collect_user_preference(user_preferences)

                    for key, value in user_preferences.items():
                        text = text.replace(f'[{key}]', value)

                    return text
            else:
                response, sps = suggest_products(slot, products)
                r.hset(f'luna:{user_id}',
                       'suggested_products', json.dumps(sps))
                return response

    return 'I don\'t understand what you mean.'
