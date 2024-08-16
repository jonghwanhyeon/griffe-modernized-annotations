from __future__ import annotations

from typing import Iterable, Sequence

from griffe import ExprBinOp, ExprSubscript
from typing_extensions import TypeGuard

from griffe_modernized_annotations.predicates import instance_of, is_sequence, is_subscript_with
from griffe_modernized_annotations.proposals.pep import PEP
from griffe_modernized_annotations.transforms import transform_expression
from griffe_modernized_annotations.traversal import chain
from griffe_modernized_annotations.types import Expression
from griffe_modernized_annotations.utils import canonical_path_of, deduplicate


class PEP604(PEP):
    _priorities = {
        "bool": 0,
        "bytearray": 0,
        "bytes": 0,
        "complex": 0,
        "float": 0,
        "int": 0,
        "str": 0,
        "dict": 1,
        "frozenset": 1,
        "list": 1,
        "memoryview": 1,
        "range": 1,
        "set": 1,
        "tuple": 1,
        "type": 1,
        "object": 2,
        "...": 3,
        "None": 4,
    }

    def adopt(self, annotation: Expression) -> Expression:
        annotation = self._transform_union(annotation)
        annotation = self._transform_optional(annotation)
        annotation = self._transform_to_left_associative(annotation)
        annotation = self._sort_operands(annotation)
        return annotation

    def _transform_union(self, annotation: Expression) -> Expression:
        def func(subscript: ExprSubscript) -> Expression:
            slice = subscript.slice
            operands = slice.elements if is_sequence(slice) else [slice]
            return self._chain_operands("|", operands)

        return transform_expression(
            expression=annotation,
            predicate=is_subscript_with("typing.Union"),
            func=func,
        )

    def _transform_optional(self, annotation: Expression) -> Expression:
        return transform_expression(
            expression=annotation,
            predicate=is_subscript_with("typing.Optional"),
            func=lambda subscript: ExprBinOp(left=subscript.slice, operator="|", right="None"),
        )

    def _transform_to_left_associative(self, annotation: Expression) -> Expression:
        def predicate(expression: Expression) -> TypeGuard[ExprBinOp]:
            return isinstance(expression, ExprBinOp) and isinstance(expression.right, ExprBinOp)

        def func(operation: ExprBinOp) -> ExprBinOp:
            # (left operator (right.left right.operator right.right))
            # -> ((left operator right.left) right.operator right.right)
            left, operator, right = operation.left, operation.operator, operation.right
            assert isinstance(right, ExprBinOp)

            return ExprBinOp(
                left=ExprBinOp(left=left, operator=operator, right=right.left),
                operator=right.operator,
                right=right.right,
            )

        return transform_expression(annotation, predicate=predicate, func=func)

    def _sort_operands(self, annotation: Expression) -> Expression:
        def flatten(expression: Expression) -> Iterable[Expression]:
            if isinstance(expression, ExprBinOp):
                yield from flatten(expression.left)
                yield from flatten(expression.right)
            else:
                yield expression

        def key_of(operand: Expression) -> int:
            default = self._priorities["object"]
            return self._priorities.get(canonical_path_of(operand), default)

        transformed: set[int] = set()

        def func(operation: ExprBinOp) -> Expression:
            if id(operation) in transformed:
                return operation

            operands = [*deduplicate(flatten(operation))]
            operands = sorted(operands, key=key_of)

            output = self._chain_operands("|", operands)
            transformed.update(id(operation) for operation in chain(output, "left"))
            return output

        return transform_expression(annotation, predicate=instance_of(ExprBinOp), func=func)

    def _chain_operands(self, operator: str, operands: Sequence[Expression]) -> Expression:
        chained = operands[0]
        for operand in operands[1:]:
            chained = ExprBinOp(left=chained, operator=operator, right=operand)

        return chained
