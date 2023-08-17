"""Usage of Python descriptors, and static type checkers behaviour."""
from dataclasses import dataclass
from typing import Any, Never, reveal_type
from typing_extensions import override
from descriptor import *  # type: ignore


@dataclass
class Constant[T](WithGet[Any, T, T], WithSet[Never, Never], WithDelete[Never]):
    value: T

    @override
    def __set__(self, obj: Never, value: Never) -> None:
        raise ValueError("Constants are read-only.")

    @override
    def __delete__(self, obj: Never) -> None:
        raise ValueError("Constants are read-only.")

    @override
    def __get__[X](self, obj: X | None, cls: type[X], /) -> T:
        return self.value


class X:
    const = Constant(42)

    def hello(self, /) -> None:
        print("hello!")


reveal_type(X().const)  # int
reveal_type(X.const)    # int as well
