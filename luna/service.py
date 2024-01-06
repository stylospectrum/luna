import bentoml

from typing import Dict, Any
from bentoml.io import JSON
from pydantic import BaseModel

from luna.runners.classifier import classifier_runner
from luna.runners.chitchat import chitchat_runner


class MessageModel(BaseModel):
    content: str


svc = bentoml.Service("luna", runners=[chitchat_runner, classifier_runner])


@svc.api(input=JSON(pydantic_model=MessageModel), output=JSON())
async def predict(message: MessageModel) -> Dict[str, Any]:
    content: str = message.model_dump()['content']
    intent = await classifier_runner.classify.async_run(content, 'intent')
    text = None
    slot = None
    request_slots = None

    if intent == 'chitchat':
        text = await chitchat_runner.generate.async_run(content)

    if intent == 'buy' or intent == 'ask':
        slot = await classifier_runner.classify.async_run(content, 'slot')

    if intent == 'ask':
        request_slots = await classifier_runner.classify.async_run(content)

    return {
        'intent': intent,
        'text': text,
        'slot': slot,
        'request_slots': request_slots
    }
