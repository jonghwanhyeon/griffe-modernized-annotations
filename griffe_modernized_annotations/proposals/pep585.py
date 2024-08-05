from griffe import ExprName

from griffe_modernized_annotations.predicates import is_subscript_with
from griffe_modernized_annotations.proposals.pep import PEP
from griffe_modernized_annotations.traversal import walk_expressions
from griffe_modernized_annotations.types import Expression
from griffe_modernized_annotations.utils import canonical_path_of


class PEP585(PEP):
    _collections = {
        "typing.Tuple": "tuple",
        "typing.List": "list",
        "typing.Dict": "dict",
        "typing.Set": "set",
        "typing.FrozenSet": "frozenset",
        "typing.Type": "type",
    }

    def adopt(self, annotation: Expression) -> Expression:
        predicate = is_subscript_with(set(self._collections.keys()))

        for subscript in walk_expressions(annotation, predicate=predicate):
            left = subscript.left
            assert isinstance(left, ExprName)
            left.name = self._collections[canonical_path_of(left)]

        return annotation
