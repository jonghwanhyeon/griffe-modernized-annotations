from __future__ import annotations

from griffe import Extensions, temporary_visited_package
from utils import annotations_from_function

from griffe_modernized_annotations import ModernizedAnnotationsExtension


def test_modernized_annotations() -> None:
    with temporary_visited_package(
        "package",
        modules={
            "__init__.py": """
                from typing import Dict, Generic, List, Optional, Set, Tuple, TypeVar, Union

                from typing_extensions import TypeAlias

                A = TypeVar("A")
                B = TypeVar("B")
                C = TypeVar("C")
                Buffer: TypeAlias = Union[bytes, bytearray, memoryview]


                class Foo(Generic[A, B, C]):
                    def f1(self, a: A) -> A:
                        return a

                    def f2(self, b: B) -> B:
                        return b

                    def f3(self, c: C) -> C:
                        return c


                class Bar(
                    Foo[
                        Union[int, float],
                        Optional[Union[List[int], Tuple[int, ...]]],
                        A,
                    ],
                    Generic[A],
                ):
                    def f1(self, a: Union[int, float]) -> Union[int, float]:
                        return super().f1(a)

                    def f2(self, b: Optional[Union[List[int], Tuple[int, ...]]]) -> Optional[Union[List[int], Tuple[int, ...]]]:
                        return super().f2(b)


                variable: Union[Foo, int, Optional[Buffer]]


                def function(
                    a: List[int],
                    b: Set[float],
                    c: Tuple[int, Tuple[float, ...], Optional[int]],
                    d: List[Dict[str, Tuple[Optional[Union[int, float]]]]],
                ) -> Optional[Union[Bar, Foo, int, float]]:
                    return None
            """,
        },
        extensions=Extensions(ModernizedAnnotationsExtension()),
    ) as package:
        Buffer = package["Buffer"]
        assert str(Buffer.value) == "bytes | bytearray | memoryview"

        Foo = package["Foo"]
        assert tuple(annotations_from_function(Foo["f1"])) == ("None", "A", "A")
        assert tuple(annotations_from_function(Foo["f2"])) == ("None", "B", "B")
        assert tuple(annotations_from_function(Foo["f3"])) == ("None", "C", "C")

        Bar = package["Bar"]
        assert tuple(annotations_from_function(Bar["f1"])) == ("None", "int | float", "int | float")
        assert tuple(annotations_from_function(Bar["f2"])) == (
            "None",
            "list[int] | tuple[int, ...] | None",
            "list[int] | tuple[int, ...] | None",
        )

        variable = package["variable"]
        assert str(variable.annotation) == "int | Foo | Buffer | None"

        function = package["function"]
        assert tuple(annotations_from_function(function)) == (
            "list[int]",
            "set[float]",
            "tuple[int, tuple[float, ...], int | None]",
            "list[dict[str, tuple[int | float | None]]]",
            "int | float | Bar | Foo | None",
        )
