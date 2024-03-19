import bentoml
import typing as t
from typing import TYPE_CHECKING
from luna.generator.inference import ChitChatInference

if TYPE_CHECKING:
    from bentoml._internal.runner.runner import RunnerMethod

    class RunnerImpl(bentoml.Runner):
        generate: RunnerMethod


class ChitChatRunnable(bentoml.Runnable):
    SUPPORTED_RESOURCES = ("cpu",)
    SUPPORTS_CPU_MULTI_THREADING = True

    def __init__(self):
        self.inference = ChitChatInference()

    @bentoml.Runnable.method(batchable=False)
    def generate(self, text: str) -> str:
        return self.inference.generate(text)


generator_runner = t.cast(
    "RunnerImpl", bentoml.Runner(ChitChatRunnable, name="generator")
)
