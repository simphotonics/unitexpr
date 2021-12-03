from numbers import Number

from .qarray import QArray


class Quantity(QArray):
    """
    A quantity described by
    a numerical value, a unit and an optional string
    containing additional information.

    Equivalent to a `QArray` with shape (1,).

    The instance attribute `info` can be used to store
    object documentation.
    """

    __slots__ = ("__info",)

    def __new__(subtype, value: Number, unit=1.0, info=""):
        obj = super().__new__(
            subtype,
            (1,),
            dtype=type(value),
            buffer=None,
            offset=0,
            strides=None,
            unit=unit,
        )
        obj.fill(value)
        obj.__info = info
        return obj

    def __array_finalize__(self, obj):
        if obj is None:
            return
        self.unit = getattr(obj, "unit", 1.0)

    @property
    def value(self):
        """ Copies the entry stored at `self[0]` to a
        standard Python scalar and returns the result.
        """
        return self.item()

    @property
    def info(self):
        try:
            return self.__info
        except AttributeError:
            return ""

    def __str__(self) -> str:
        return f"{self[0]} {self.unit}"

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}({self[0]}, "
            + f"unit={self.unit}, info={self.info.__repr__()})"
        )

    def min(self):
        return self[0]

    def max(self):
        return self[0]

    def mean(self):
        return self[0]

    @classmethod
    def from_input(cls, input, unit=1.0):
        raise NotImplementedError()

    def reshape(self, shape, order):
        raise NotImplementedError(
            f"Objects of type '{self.__class__.__name__}' cannot be reshaped."
        )

    def resize(self, new_shape, refcheck=True):
        raise NotImplementedError(
            f"Objects of type '{self.__class__.__name__}' cannot be resized."
        )
