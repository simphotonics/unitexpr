from numbers import Number

from .qarray import qarray


class Quantity(qarray):
    """
    A quantity described by
    a numerical value, a unit and an optional string
    containing additional information.

    Equivalent to a `QArray` with shape (1,).

    The instance attribute `info` can be used to store
    object documentation.
    """

    def __new__(subtype, value: Number, unit=1.0, info=""):
        obj = super().__new__(
            subtype,
            (1,),
            dtype=type(value),
            buffer=None,
            offset=0,
            strides=None,
            unit=unit,
            info=info,
        )
        obj.fill(value)
        return obj

    def __array_finalize__(self, obj):
        if obj is None:
            return
        self.unit = getattr(obj, "unit", 1.0)

    @property
    def value(self):
        """Returns the entry stored at `self[0]`.
        ..
        """
        return self.item()

    def __str__(self) -> str:
        unit = f" {self.unit}" if (self.unit != 1.0) else ""
        return f"{self[0]}{unit}"

    def __repr__(self) -> str:
        unit = f", unit={self.unit}" if self.unit != 1.0 else ""
        info = f", info={self.info.__repr__()}" if self.info != "" else ""
        return f"{self.__class__.__name__}({self[0]}" + unit + info + ")"

    def __add__(self, other) -> qarray:

        
        return super().__add__(other)

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
