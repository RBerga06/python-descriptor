# How to correctly type descriptors in Python.

This approach is 100% supported by the pyright type checker.

Have a look at the Python files in this repo:

- `descriptor.py` contains the definition of all descriptor protocols
- `property.py` contains a redefinition of Python's builtin `property` type, *but* it's correctly typed.
- `usage.py` contains some examples

> [!WARNING] Everything here needs Python 3.13 installed
> (e.g. `pyenv install 3.13-dev`) to work correctly.
> If you need it in an older Python version,
> simply use the old `TypeVar` syntax.
