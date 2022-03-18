from numbers import Number

from .qarray import qarray


def quantity(value: Number, unit=1.0, info=""):
    """
    Constructs a quantity described by
    a numerical value or a numerical array,
    a unit and an optional string
    containing additional information.
    The instance attribute `info` can be used to store
    object documentation.
    """
    return qarray.from_input(value, unit=unit, info=info)
