"""Descriptor protocol[s] definitions."""
from typing import Never, Protocol, overload


class WithGet[X, T, U](Protocol):
    """'__get__(...)' invocation:
    Let x be an instance of X, that defines a descriptor instance 'd'.
    >>> class X:
    ...     d = MyDescriptor(...)
    >>> x = X()
    >>> d = vars(X)['d']  # access the descriptor instance
    >>> x.d  # <=> d.__get__(x, X)
    >>> X.d  # <=> d.__get__(None, X)
    """
    #ref: https://docs.python.org/3/howto/descriptor.html#technical-tutorial
    @overload
    def __get__(self, obj: X, cls: type[X], /) -> T: ...
    @overload
    def __get__(self, obj: None, cls: type[X], /) -> U: ...


class WithSet[X, T](Protocol):
    def __set__(self, obj: X, value: T, /) -> None: ...


class WithDelete[X, _: (None, Never) = None](Protocol):
    @overload
    def __delete__(self: WithDelete[X, Never], obj: Never, /) -> None: ...
    @overload
    def __delete__(self: WithDelete[X, None], obj: X, /) -> None: ...
    def __delete__(self, obj: X, /) -> None: ...


class WithSetName[X, N: str = str](Protocol):
    def __set_name__(self, obj: X, name: N, /) -> None: ...
