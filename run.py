from __future__ import annotations

from griffe import Extensions, temporary_visited_package

from griffe_modernized_annotations import ModernizedAnnotationsExtension

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


            variable: Union[Foo, int, Optional[float]]


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
    print(str(Buffer.value))
