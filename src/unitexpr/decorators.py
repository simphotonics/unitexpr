""" Provides the decorator `protect`. It is used to annotate the
    class method `__setattr__` in order to prevent attribute
    modificaton.

    Should be used in meta-classes and classes that are not instantiated often
    since the nested decorator is called every time an attribute is set.
"""
from functools import wraps
from inspect import signature
from typing import Iterable


class ProtectedAttributeError(AttributeError):
    """Error indicating an attempted modification of a protected attribute."""


def protect(
    attr_names: Iterable[str] = (),
    error_type: Exception = ProtectedAttributeError,
):
    """
    Function used to decorate `__setattr__`.
    It raises an exception during an attempt to
    modify any class attributes specified by `attr_names` after the
    attributes have been initially set.

    - `attr_names`: A tuple containing the names of
      all class attributes that must not be modified.
      The default value of `attr_names` is an empty tuple
      indicating that all
      attributes should be protected.
    - `error_type`: Optional parameter used to
       specify the type of error raised.
    """
    if isinstance(attr_names, str):
        attr_names = (attr_names,)

    def _protect(func):
        @wraps(func)
        def inner(*args, **kwargs):
            # Map args onto kwargs:
            all_argument_names = tuple(signature(func).parameters.keys())
            mapped_kwargs = kwargs.copy()
            for index, arg_value in enumerate(args):
                mapped_kwargs[all_argument_names[index]] = arg_value
            # Check attempted modification of protected attributes.
            if (
                mapped_kwargs["name"] in attr_names or not attr_names
            ) and hasattr(mapped_kwargs["self"], mapped_kwargs["name"]):
                # mapped_kwargs['name'] in mapped_kwargs['self'].__dict__:
                raise error_type(
                    f"Class attribute `{mapped_kwargs['name']}"
                    "must not be modified."
                )

            return func(*args, **kwargs)

        return inner

    return _protect
