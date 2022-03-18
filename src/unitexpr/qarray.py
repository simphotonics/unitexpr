"""
Numpy array with the additional attribute `unit`.
"""

from __future__ import annotations

from typing import Callable, Union

import numpy as np
from numpy.core._exceptions import UFuncTypeError

from .errors import OperationNotSupported
from .unit import UnitBase, UnitExprBase


class qarray(np.ndarray):
    """
    An array with elements representing the magnitudes of quantity that can be
    described by a numerical value and a unit.

    `qarray` is a sub-class of ndarray with the additional instance
    attributes `unit` and `info`.

    Implementation closely follows:
    https://numpy.org/devdocs/user/basics.subclassing.html#basics-subclassing
    """

    __unit_types = (UnitBase, UnitExprBase)
    __slots__ = ("__unit", "__info")

    def __new__(
        subtype,
        shape,
        dtype=float,
        buffer=None,
        offset=0,
        strides=None,
        order=None,
        unit=1.0,
        info="",
    ):
        # The call in the next line triggers a call to
        # qarray.__array_finalize__
        obj = super().__new__(
            subtype, shape, dtype, buffer, offset, strides, order
        )
        obj.unit = unit
        obj.__info = info
        return obj

    def __array_finalize__(self, obj):
        # ``self`` is a new object resulting from
        # ndarray.__new__(qarray, ...), therefore it only has
        # attributes that the ndarray.__new__ constructor gave it -
        # i.e. those of a standard ndarray.
        #
        # We could have got to the ndarray.__new__ call in 3 ways:
        # From an explicit constructor - e.g. qarray():
        #    obj is None
        #    (we're in the middle of the qarray.__new__
        #    constructor, and self.unit will be set when we return to
        #    qarray.__new__)
        if obj is None:
            return
        # From view casting - e.g arr.view(qarray):
        #    obj is arr
        #    (type(obj) can be qarray)
        # From new-from-template - e.g infoarr[:3]
        #    type(obj) is qarray
        #
        # Note that it is here, rather than in the __new__ method,
        # that we set the default value for 'unit', because this
        # method sees all creation of default objects - with the
        # qarray.__new__ constructor, but also with
        # arr.view(qarray).
        self.__unit = getattr(obj, "unit", 1.0)

    @classmethod
    def from_input(cls, input, unit=1.0, info="") -> qarray:
        """Constructs a `qarray` from an existing ndarray
        or from a (nested) sequence of entries.
        """
        obj = np.asarray(input).view(cls)
        obj.unit = unit
        obj.info = info
        return obj

    @property
    def unit(self):
        """Returns the unit of the object."""
        return self.__unit

    @unit.setter
    def unit(self, value) -> None:
        factor = (
            value.factor
            if isinstance(value, self.__unit_types)
            else float(value)
        )

        if factor == 1.0:
            self.__unit = value
            return None

        if factor == 0.0:
            raise ValueError(
                f"Could not set unit with zero magnitude: {value}."
            )

        try:
            self *= factor
            self.__unit = value / factor
        except UFuncTypeError:
            cfactor = self.dtype.type(factor)
            if cfactor == factor:
                self *= cfactor
                self.__unit = value / factor
            else:
                # If factor can not be safely converted to dtype do not
                # normalize unit:
                self.__unit = value

    @property
    def info(self):
        try:
            return self.__info
        except AttributeError:
            return ""

    @info.setter
    def info(self, value: str) -> None:
        self.__info = value

    @property
    def base(self):
        """
        Returns the quantity in terms of base units.
        Note: Returns `self` if the quantity has `unit == 1.0`.
        """
        if self.unit == 1.0:
            return self
        other = self.copy()
        other.unit = self.unit.base_expr
        return other

    def __format__(self, __format_spec: str) -> str:
        if self.ndim == 0:
            return self.__str__()
        return super().__format__(__format_spec)

    def __str__(self) -> str:
        if self.ndim == 0:
            unit = f" {self.unit}" if (self.unit != 1.0) else ""
            return super().__str__() + unit
        else:
            unit = f" unit: {self.unit}" if (self.unit != 1.0) else ""
            return super().__str__() + unit

    def __repr__(self) -> str:
        unit = f", unit={self.unit}" if self.unit != 1.0 else ""
        info = f", info={self.info.__repr__()}" if self.info != "" else ""
        return super().__repr__()[:-1] + unit + info + ")"

    def __add__(self, other) -> qarray:
        if isinstance(other, self.__unit_types):
            beta = other.scaling_factor(self.unit)
            if beta is None:
                raise OperationNotSupported(self, other, "+")
            return super().__add__(1.0 / beta)

        other_unit = getattr(other, "unit", 1.0)
        # If units match simply add arrays.
        if self.unit == other_unit:
            return super().__add__(other)

        alpha = other_unit / self.unit

        if isinstance(alpha, float):
            return super().__add__(other * alpha)

        if (
            isinstance(alpha, UnitExprBase)
            and alpha.base_exponents == alpha.base_exponents_zero
        ):
            return super().__add__(other * alpha.base_factor)

        raise OperationNotSupported(self, other, "+")

    def __radd__(self, other) -> qarray:
        return self.__add__(other)

    def __sub__(self, other) -> qarray:
        if isinstance(other, self.__unit_types):
            beta = other.scaling_factor(self.unit)
            if beta is None:
                raise OperationNotSupported(self, other, "+")
            return super().__sub__(1.0 / beta)

        other_unit = getattr(other, "unit", 1.0)
        # If units match simply subtract arrays.
        if self.unit == other_unit:
            return super().__sub__(other)

        alpha = other_unit / self.unit

        if isinstance(alpha, float):
            return super().__sub__(other * alpha)

        if (
            isinstance(alpha, UnitExprBase)
            and alpha.base_exponents == alpha.base_exponents_zero
        ):
            return super().__sub__(other * alpha.base_factor)

        raise OperationNotSupported(self, other, "-")

    def __mul__(self, other) -> qarray:
        """
        Returns the result of multiplying the united ndarray `self`
        with `other`.
        """
        if isinstance(other, self.__unit_types):
            obj = self.copy()
            obj.unit = self.unit * other
            return obj

        obj = super().__mul__(other)
        other_unit = getattr(other, "unit", 1.0)
        obj.unit = self.unit * other_unit
        return obj

    def __rmul__(self, other) -> qarray:
        """
        Returns the result of multiplying `other` with the united array
        `self`.
        """
        if isinstance(other, self.__unit_types):
            obj = self.copy()
            obj.unit = other * self.unit
            return obj

        obj = super().__rmul__(other)
        other_unit = getattr(other, "unit", 1.0)
        obj.unit = other_unit * self.unit
        return obj

    def __truediv__(self, other) -> qarray:
        """
        Returns the result of dividing the united ndarray `self`
        with `other`.
        """
        if isinstance(other, self.__unit_types):
            obj = self.copy()
            obj.unit = self.unit / other
            return obj

        obj = super().__truediv__(other)
        other_unit = getattr(other, "unit", 1.0)
        obj.unit = self.unit / other_unit
        return obj

    def __rtruediv__(self, other) -> qarray:
        """
        Returns the result of dividing `other` by the united ndarray `self`.
        """
        if isinstance(other, self.__unit_types):
            obj = super().__rtruediv__(other.factor)
            obj.unit = other / self.unit
            return obj

        obj = super().__rtruediv__(other)
        other_unit = getattr(other, "unit", 1.0)
        obj.unit = other_unit / self.unit
        return obj

    def __pow__(self, other: Union[float, int]) -> qarray:
        obj = super().__pow__(other)
        obj.unit = self.unit.__pow__(other)
        return obj

    def __abs__(self) -> qarray:
        obj = super().__abs__()
        obj.unit = self.unit
        return obj

    def __neg__(self) -> qarray:
        obj = super().__neg__()
        obj.unit = self.unit
        return obj

    def __pos__(self) -> qarray:
        obj = super().__pos__()
        obj.unit = self.unit.__pos__()
        return obj

    def __eq__(self, other) -> qarray:
        result = self.compare(other, super().__eq__)
        if result is None:
            result = super().__eq__(other)
            result.unit = 1.0
            result.fill(False)
        return result

    def __le__(self, other) -> qarray:
        result = self.compare(other, super().__le__)
        if result is None:
            raise OperationNotSupported(self, other, "<=")
        return result

    def __ge__(self, other) -> qarray:
        result = self.compare(other, super().__ge__)
        if result is None:
            raise OperationNotSupported(self, other, ">=")
        return result

    def __gt__(self, other) -> qarray:
        result = self.compare(other, super().__gt__)
        if result is None:
            raise OperationNotSupported(self, other, ">")
        return result

    def __lt__(self, other) -> qarray:
        result = self.compare(other, super().__lt__)
        if result is None:
            raise OperationNotSupported(self, other, "<")
        return result

    def compare(
        self, other, comparison_operator: Callable
    ) -> Union[qarray, None]:
        """
        Generic comparison function that handles input of type `Number`,
        `ndarray` and `qarray` using `comparison_operator`.

        Returns `None` if the comparison failed due to incompatible units.
        """
        if isinstance(other, self.__unit_types):
            beta = other.scaling_factor(self.unit)
            if beta is None:
                return None
            obj = comparison_operator(1.0 / beta)
            obj.unit = 1.0
            return obj

        other_unit = getattr(other, "unit", 1.0)

        if self.unit == other_unit:
            obj = comparison_operator(other)
            obj.unit = 1.0
            return obj

        alpha = other_unit / self.unit

        if isinstance(alpha, float):
            obj = comparison_operator(other * alpha)
            obj.unit = 1.0
            return obj

        if (
            isinstance(alpha, UnitExprBase)
            and alpha.base_exponents == alpha.base_exponents_zero
        ):
            obj = comparison_operator(other * alpha.base_factor)
            obj.unit = 1.0
            return obj

        return None
