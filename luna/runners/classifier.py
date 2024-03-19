import bentoml
import typing as t
from typing import TYPE_CHECKING, Any

from luna.request_slots_classifier.inference import RequestSlotsClassifierInference
from luna.intent_classifier.inference import IntentClassifierInference
from luna.slot_classifier.inference import SlotClassifierInference

if TYPE_CHECKING:
    from bentoml._internal.runner.runner import RunnerMethod

    class RunnerImpl(bentoml.Runner):
        classify: RunnerMethod


class ClassifierRunnable(bentoml.Runnable):
    SUPPORTED_RESOURCES = ("cpu",)
    SUPPORTS_CPU_MULTI_THREADING = True

    def __init__(self):
        self.intent_classifier = IntentClassifierInference()
        self.slot_classifier = SlotClassifierInference()
        self.request_slots_classifier = RequestSlotsClassifierInference()

    @bentoml.Runnable.method(batchable=False)
    def classify(self, text: str | list[str], type: str = "", action="classify") -> Any:
        if action == "classify":
            if type == "slot":
                return self.slot_classifier.classify(text)

            if type == "intent":
                return self.intent_classifier.classify(text)

            return self.request_slots_classifier.classify(text)
        else:
            return self.intent_classifier.get_embeddings(text)


classifier_runner = t.cast(
    "RunnerImpl", bentoml.Runner(ClassifierRunnable, name="classifier")
)
