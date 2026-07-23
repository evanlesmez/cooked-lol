from types import FunctionType
from typing import NoReturn


class DataReadOnlyMeta(type):
    """
    Data read only class
    Only enforces runtime
    """

    def __new__(mcs, name, bases, namespace):
        # mcs means  metaclass
        for base in bases:
            if isinstance(base, DataReadOnlyMeta):
                raise TypeError(f"Cannot subclass {base.__name__!r}")
        for attr_name, value in namespace.items():
            if attr_name.startswith("__") and attr_name.endswith("__"):
                continue
            if isinstance(value, (FunctionType, classmethod, staticmethod, property)):
                raise TypeError(
                    f"{name!r} is data-only: method {attr_name!r} is not allowed"
                )
        return super().__new__(mcs, name, bases, namespace)

    def __setattr__(cls, name, value):
        raise AttributeError(
            f"Cannot reassng {name!r} on static readonly class {cls.__name__!r}"
        )

    def __delattr__(cls, name) -> NoReturn:
        raise AttributeError(
            f"Cannot delete {name!r} on static readonly class {cls.__name__!r}"
        )

    def __call__(cls, *args, **kwargs) -> NoReturn:
        raise TypeError(f"{cls.__name__} cannot be instantiated")
