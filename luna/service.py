import bentoml

from bentoml.io import JSON
from pydantic import BaseModel
from luna.runners.slot_classifier import slot_classifier_runner


class MessageModel(BaseModel):
    content: str


svc = bentoml.Service("luna", runners=[
                      slot_classifier_runner])


@svc.api(input=JSON(pydantic_model=MessageModel), output=JSON())
async def chat(message: MessageModel) -> list:
    content: str = message.model_dump()['content']
    res = await slot_classifier_runner.predict.async_run(content)

    return res
