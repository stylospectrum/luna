import bentoml
import typing as t
from typing import TYPE_CHECKING
from luna.slot_classifier.inference import SlotClassifierInference

if TYPE_CHECKING:
    from bentoml._internal.runner.runner import RunnerMethod

    class RunnerImpl(bentoml.Runner):
        encode: RunnerMethod


class SlotClassifierRunnable(bentoml.Runnable):
    SUPPORTED_RESOURCES = ("cpu",)
    SUPPORTS_CPU_MULTI_THREADING = False

    def __init__(self):
        self.inference = SlotClassifierInference()

    @bentoml.Runnable.method(batchable=False)
    def predict(self, text: str) -> list:
        return self.inference.predict(text)


slot_classifier_runner = t.cast(
    "RunnerImpl", bentoml.Runner(
        SlotClassifierRunnable, name="slot_classifier")
)
