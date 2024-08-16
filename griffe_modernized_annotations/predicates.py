from __future__ import annotations

import operator
from typing import Any, TypeVar, Union

from griffe import ExprList, ExprName, ExprSubscript, ExprTuple
from typing_extensions import TypeGuard, overload

from griffe_modernized_annotations.types import Expression, Predicate
from griffe_modernized_annotations.utils import canonical_path_of

T = TypeVar("T")
T1 = TypeVar("T1")
T2 = TypeVar("T2")
T3 = TypeVar("T3")


@overload
def instance_of(type: type[T]) -> Predicate[T]: ...
@overload
def instance_of(type: tuple[type[T1], type[T2]]) -> Predicate[Union[T1, T2]]: ...
@overload
def instance_of(type: tuple[type[T1], type[T2], type[T3]]) -> Predicate[Union[T1, T2, T3]]: ...


def instance_of(type: Any) -> Predicate[Any]:
    def predicate(value: Any) -> TypeGuard[Any]:
        return isinstance(value, type)

    return predicate


is_sequence = instance_of((ExprList, ExprTuple))


def is_subscript_with(canonical_path: Union[str, set[str]]) -> Predicate[ExprSubscript]:
    comparator = operator.eq if isinstance(canonical_path, str) else operator.contains

    def predicate(expression: Expression) -> TypeGuard[ExprSubscript]:
        return (
            isinstance(expression, ExprSubscript)
            and isinstance(expression.left, ExprName)
            and (comparator(canonical_path, canonical_path_of(expression.left)))
        )

    return predicate
