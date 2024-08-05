from __future__ import annotations

import copy
from typing import Any, Iterable, Optional, TypeVar, Union

from griffe import Expr, Object

from griffe_modernized_annotations.types import Expression

T = TypeVar("T")


def canonical_name_of(instance: Expression) -> str:
    return instance.canonical_name if isinstance(instance, Expr) else instance


def path_of(instance: Union[Expression, Object]) -> str:
    return instance.path if isinstance(instance, (Expr, Object)) else instance


def canonical_path_of(instance: Union[Expression, Object]) -> str:
    return instance.canonical_path if isinstance(instance, (Expr, Object)) else instance


def type_path_of(expression: Expression, scope: Object) -> str:
    return f"{canonical_path_of(expression)}@{scope.canonical_path}"


def deepcopy(instance: T, shared: Optional[set[str]] = None) -> T:
    memo: dict[int, Any] = {}
    if shared is not None:
        for attribute in shared:
            if hasattr(instance, attribute):
                value = getattr(instance, attribute)
                memo[id(value)] = value

    return copy.deepcopy(instance, memo=memo)


def deduplicate(sequence: Iterable[T]) -> Iterable[T]:
    seen: list[T] = []  # Since `Expr` is not `Hashable`, use `list` instead of `set`
    for item in sequence:
        if item not in seen:
            yield item
            seen.append(item)
