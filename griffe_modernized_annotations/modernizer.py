from __future__ import annotations

from typing import Optional

from griffe_modernized_annotations.proposals import PEP
from griffe_modernized_annotations.types import Expression


class AnnotationModernizer:
    def __init__(self, proposals: list[PEP]) -> None:
        self._proposals = proposals

    def modernize(self, annotation: Optional[Expression]) -> Optional[Expression]:
        if annotation is None:
            return None

        for proposal in self._proposals:
            annotation = proposal.adopt(annotation)

        return annotation

    def __call__(self, annotation: Optional[Expression]) -> Optional[Expression]:
        return self.modernize(annotation)
