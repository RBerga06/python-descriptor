"""Descriptor protocol[s] definitions."""
from typing import Any, Protocol, overload


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


class WithDelete[X](Protocol):
    def __delete__(self, obj: X, /) -> None: ...


class WithSetName[X, N: str = str](Protocol):
    def __set_name__(self, obj: X, name: N, /) -> None: ...


class WithGetAndSet[X, Tget, Uget, Tset](WithGet[X, Tget, Uget], WithSet[X, Tset], Protocol):
    """Equivalent to `WithGet[X, Tget, Uget] & WithSet[X, Tset]`."""
    # '&' here denotes an intersection. Not yet introduced in the Python typing system (but soon might be).


type AttrGet[T] = T | WithGet[Any, T, Any]
type AttrSet[T] = T | WithSet[Any, T]
type Attr[T]    = T | WithGetAndSet[Any, T, Any, T]
# type AttrGetOnly[T] = AttrGet[T] & (AttrSet[Never] | ~AttrSet[Any])
#   (requires Intersection and Not, that might be introduced in future Python versions)
