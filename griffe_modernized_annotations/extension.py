from griffe import Attribute, Class, Extension, Function, Module

from griffe_modernized_annotations.modernizer import AnnotationModernizer
from griffe_modernized_annotations.proposals import PEP585, PEP604
from griffe_modernized_annotations.traversal import walk_objects_of
from griffe_modernized_annotations.utils import canonical_path_of


class ModernizedAnnotationsExtension(Extension):
    def __init__(self) -> None:
        self._modernizer = AnnotationModernizer(
            proposals=[
                PEP585(),
                PEP604(),
            ]
        )

    def on_package_loaded(self, *, pkg: Module) -> None:
        for cls in walk_objects_of(pkg, type=Class):
            self._handle_class(cls)

        for function in walk_objects_of(pkg, type=Function):
            self._handle_function(function)

        for attribute in walk_objects_of(pkg, type=Attribute):
            self._handle_attribute(attribute)

    def _handle_class(self, cls: Class) -> None:
        cls.bases = [self._modernizer(base) for base in cls.bases]  # type: ignore[misc]

    def _handle_function(self, function: Function) -> None:
        for parameter in function.parameters:
            parameter.annotation = self._modernizer(parameter.annotation)

        function.returns = self._modernizer(function.returns)

    def _handle_attribute(self, attribute: Attribute) -> None:
        if attribute.annotation is not None:
            if canonical_path_of(attribute.annotation) in ("typing.TypeAlias", "typing_extensions.TypeAlias"):
                attribute.value = self._modernizer(attribute.value)
            else:
                attribute.annotation = self._modernizer(attribute.annotation)
