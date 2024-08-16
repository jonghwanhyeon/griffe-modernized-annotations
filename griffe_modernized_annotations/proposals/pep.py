from abc import ABC, abstractmethod

from griffe_modernized_annotations.types import Expression


class PEP(ABC):
    @abstractmethod
    def adopt(self, annotation: Expression) -> Expression: ...
