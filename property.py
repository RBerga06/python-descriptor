#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Usage example: Python property."""
from dataclasses import InitVar, dataclass, field
from typing import Any, Callable, Never, Self, overload, reveal_type
from typing_extensions import override
from descriptor import *  # type: ignore


@dataclass(slots=True)
class property[
    X,
    Tget = Never,
    Tset = Never,
    Xdel = Never,  # in a perfect, world, `Xdel: X = Never`
](
    WithGet[X, Tget, Any],
    WithSet[X, Tset],
    WithDelete[Xdel],
    WithSetName[X],
):
    """Like Python's `builtins.property`, but correctly typed."""
    #ref: https://docs.python.org/3/howto/descriptor.html#properties
    fget: Callable[[X], Tget]       | None = None
    fset: Callable[[X, Tset], None] | None = None
    fdel: Callable[[Xdel], None]    | None = None
    doc: InitVar[str | None]               = None
    __doc__: str | None = field(init=False)
    name: str           = field(init=False, default="")

    def __post_init__(self, doc: str | None, /) -> None:
        if doc is None:
            doc = getattr(self.fget, '__doc__', None)
        self.__doc__ = doc

    @override
    def __set_name__(self, obj: X, name: str) -> None:
        self.name = name

    @overload
    def __get__(self, obj: X, cls: type[X], /) -> Tget: ...
    @overload
    def __get__(self, obj: None, cls: type[X], /) -> Self: ...
    @override
    def __get__(self, obj: X | None, cls: type[X], /) -> Tget | Self:
        if obj is None:
            return self
        if self.fget is None:
            raise AttributeError(f"property '{self.name}' has no getter")
        return self.fget(obj)

    @override
    def __set__(self, obj: X, value: Tset, /) -> None:
        if self.fset is None:
            raise AttributeError(f"property '{self.name}' has no setter")
        self.fset(obj, value)

    @override
    def __delete__(self, obj: Xdel, /) -> None:
        if self.fdel is None:
            raise AttributeError(f"property '{self.name}' has no deleter")
        self.fdel(obj)

    def getter[Uget](self, fget: Callable[[X], Uget], /) -> "property[X, Uget, Tset, Xdel]":
        prop = property[X, Uget, Tset, Xdel](fget, self.fset, self.fdel, self.__doc__)
        prop.name = self.name
        return prop

    def setter[Uset](self, fset: Callable[[X, Uset], None], /) -> "property[X, Tget, Uset, Xdel]":
        prop = property[X, Tget, Uset, Xdel](self.fget, fset, self.fdel, self.__doc__)
        prop.name = self.name
        return prop

    def deleter(self, fdel: Callable[[X], None], /) -> "property[X, Tget, Tset, X]":
        prop = property[X, Tget, Tset, X](self.fget, self.fset, fdel, self.__doc__)
        prop.name = self.name
        return prop


class Foo:
    @property
    def foo(self, /) -> int:     # type: ignore[reportGeneralTypeIssues]
        return 42

    reveal_type(foo)             # property[Self@Foo, int, Never, Never]

    @foo.setter
    def foo(self, x: int) -> None:
        return

    reveal_type(foo)             # property[Self@Foo, int, int, Never]
    reveal_type(foo.__set__)     # (Self@Foo, int) -> None
    reveal_type(foo.__get__)     # Overload[
                                 #   (Self@Foo, type[Self@Foo]) -> int,
                                 #   (None, type[Self@Foo]) -> property[Foo, int, int, Never])
                                 # ]
    reveal_type(foo.__delete__)  # (Never) -> None

    # Qt-like Python property
    def getBar(self) -> int: ...
    def setBar(self, bar: int | str) -> None: ...
    def delBar(self) -> None: ...
    bar = property(getBar, setBar, delBar, "The 'bar' property.")



reveal_type(Foo().foo)  # int
reveal_type(Foo.foo)    # property[Foo, int, int, Never]
Foo().foo = 42          # ok
del Foo().foo           # error: cannot delete
del Foo().bar           # ok
