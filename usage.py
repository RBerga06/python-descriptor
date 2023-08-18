"""Usage of Python descriptors, and static type checkers behaviour."""
from dataclasses import dataclass
from typing import Any, Never, Protocol, reveal_type
from typing_extensions import override
from descriptor import *       # type: ignore
from property import property


@dataclass
class Constant[T](
    # Explicit protocol implementation
    #   is useful, but not mandatory
    WithGet[Any, T, T],
    WithSet[Never, Never],
    WithDelete[Never],
):
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


class Proto(Protocol):
    foo: AttrGet[int]        # <-- nothing *defined* here, only *declared*
    bar: AttrGet[int]        #     (this enables real subclasses with real attributes)
    # baz: AttrGetOnly[int]  # <-- these would require a descriptor
    # qux: AttrGetOnly[int]  #     (but without Intersection and Not it can't work)

class Foo(Proto):
    foo: int    # ok
    bar: int    # ok
    # baz: int    # error
    # qux: Never  # ok (whatever this means)

class Bar(Proto):
    # ok
    @property
    @override
    def foo(self) -> int:
        return 42

    # also ok
    @property
    @override
    def bar(self) -> int:  # type: ignore[reportGeneralTypeIssues]
        return 42
    @bar.setter
    def bar(self, bar: int) -> None:
        return

    # # error: has a setter (but shouldn't)
    # @property
    # @override
    # def baz(self) -> int:  # type: ignore[reportGeneralTypeIssues]
    #     return 42
    # @baz.setter
    # def baz(self, baz: int) -> None:
    #     return
    # reveal_type(baz)

    # # error: has a setter (but shouldn't)
    # def getQux(self) -> int:
    #     return 42
    # def setQux(self, qux: int) -> None:
    #     return
    # qux = property(getQux, setQux)
    # reveal_type(qux)
