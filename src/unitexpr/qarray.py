"""
Numpy array with the additional attribute `unit`.
"""

from __future__ import annotations

from typing import Union
from numbers import Real, Number

import numpy as np
from numpy.core._exceptions import UFuncTypeError

from .errors import OperationNotSupported
from .unit import UnitBase, UnitExprBase


class QArray(np.ndarray):
    """
    An array with elements representing a quantity that can be
    described by a numerical value and a unit.

    `QArray` is a sub-class of ndarray with the additional instance
    attribute `unit`.

    Implementation closely follows:
    https://numpy.org/devdocs/user/basics.subclassing.html#basics-subclassing
    """

    _unit_types = (UnitBase, UnitExprBase)
    __slots__ = ("__unit",)

    def __new__(
        subtype,
        shape,
        dtype=float,
        buffer=None,
        offset=0,
        strides=None,
        order=None,
        unit=1.0,
    ):
        # The call in the next line triggers a call to
        # QArray.__array_finalize__
        obj = super().__new__(
            subtype, shape, dtype, buffer, offset, strides, order
        )
        obj.unit = unit
        return obj

    def __array_finalize__(self, obj):
        # ``self`` is a new object resulting from
        # ndarray.__new__(QArray, ...), therefore it only has
        # attributes that the ndarray.__new__ constructor gave it -
        # i.e. those of a standard ndarray.
        #
        # We could have got to the ndarray.__new__ call in 3 ways:
        # From an explicit constructor - e.g. QArray():
        #    obj is None
        #    (we're in the middle of the QArray.__new__
        #    constructor, and self.unit will be set when we return to
        #    QArray.__new__)
        if obj is None:
            return
        # From view casting - e.g arr.view(QArray):
        #    obj is arr
        #    (type(obj) can be QArray)
        # From new-from-template - e.g infoarr[:3]
        #    type(obj) is QArray
        #
        # Note that it is here, rather than in the __new__ method,
        # that we set the default value for 'unit', because this
        # method sees all creation of default objects - with the
        # QArray.__new__ constructor, but also with
        # arr.view(QArray).
        self.__unit = getattr(obj, "unit", 1.0)

    @classmethod
    def from_input(cls, input, unit=1.0) -> QArray:
        """Constructs a `QArray` from an existing ndarray
        or from a (nested) sequence of entries.
        """
        obj = np.asarray(input).view(cls)
        obj.unit = unit
        return obj

    def __str__(self) -> str:
        return super().__str__() + " unit: " + str(self.unit)

    def __repr__(self) -> str:
        return super().__repr__() + " unit: " + str(self.unit)

    @property
    def unit(self):
        """Returns the unit of the object."""
        return self.__unit

    @unit.setter
    def unit(self, value) -> None:
        factor = value.factor if isinstance(value, self._unit_types) else value

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

    def __add__(self, other) -> QArray:
        # If units match simply add arrays.
        if self.unit == other.unit:
            return super().__add__(other)

        alpha = other.unit / self.unit

        if isinstance(alpha, Real):
            return super().__add__(other * alpha)

        if (
            isinstance(alpha, UnitExprBase)
            and alpha.base_exponents == alpha.base_exponents_zero
        ):
            return super().__add__(other * alpha.base_factor)

        raise OperationNotSupported(self, other, "+")

    def __sub__(self, other) -> QArray:
        # If units match simply subtract arrays.
        if self.unit == other.unit:
            return super().__sub__(other)

        alpha = other.unit / self.unit

        if isinstance(alpha, Real):
            return super().__sub__(other * alpha)

        if (
            isinstance(alpha, UnitExprBase)
            and alpha.base_exponents == alpha.base_exponents_zero
        ):
            return super().__sub__(other * alpha.base_factor)

        raise OperationNotSupported(self, other, "-")

    def __mul__(self, other) -> QArray:
        """
        Returns the result of multiplying the united ndarray `self`
        with `other`.
        """
        if isinstance(other, Number):
            return super().__mul__(other)

        if isinstance(other, self._unit_types):
            obj = self.copy()
            obj.unit = self.unit * other
            return obj

        obj = super().__mul__(other)
        try:
            obj.unit = self.unit * other.unit
        except AttributeError:
            # Enable multiplication with ndarray (without units)
            obj.unit = self.unit
        return obj

    def __rmul__(self, other) -> QArray:
        """
        Returns the result of multiplying `other` with the united array
        `self`.
        """
        if isinstance(other, Number):
            return super().__rmul__(other)

        if isinstance(other, self._unit_types):
            obj = self.copy()
            obj.unit = other * self.unit
            return obj

        obj = super().__rmul__(other)
        try:
            obj.unit = other.unit * self.unit
        except AttributeError:
            obj.unit = self.unit
        return obj

    def __truediv__(self, other) -> QArray:
        """
        Returns the result of dividing the united ndarray `self`
        with `other`.
        """
        if isinstance(other, Number):
            return super().__truediv__(other)

        if isinstance(other, self._unit_types):
            obj = self.copy()
            obj.unit = self.unit / other
            return obj

        obj = super().__truediv__(other)
        try:
            obj.unit = self.unit / other.unit
        except AttributeError:
            obj.unit = self.unit
        return obj

    # def __rtruediv__(self, other):
    #     '''
    #     Returns the result of dividing `other` by the united ndarray `self`.
    #     '''
    #     if isinstance(other, UnitBase):
    #         obj = self.copy()
    #         obj.unit = other/self.unit
    #         return obj

    #     if isinstance(other, UnitExprBase):
    #         if other.factor == 1.0:
    #             obj = self.copy()
    #             obj.unit = other/self.unit
    #         else:
    #             obj = self.__rtruediv__(other.factor)
    #             obj.unit = other.unit.scale(other.factor)/self.unit
    #         return obj

    #     obj = super().__rtruediv__(other)
    #     try:
    #         obj.unit = other.unit/self.unit
    #     except AttributeError:
    #         obj.unit = self.unit**-1
    #     return obj

    def __pow__(self, other: Union[float, int]) -> QArray:
        obj = super().__pow__(other)
        obj.unit = self.unit.__pow__(other)
        return obj

    def __abs__(self) -> QArray:
        obj = super().__abs__()
        obj.unit = self.unit
        return obj

    def __neg__(self) -> QArray:
        obj = super().__neg__()
        obj.unit = self.unit
        return obj

    def __pos__(self) -> QArray:
        obj = super().__pos__()
        obj.unit = self.unit.__pos__()
        return obj

    def __le__(self, other) -> QArray:
        if self.unit == other.unit:
            obj = super().__le__(other)
            obj.__unit = 1.0
            return obj

        alpha = other.unit / self.unit

        if isinstance(alpha, Real):
            obj = super().__le__(other * alpha)
            obj.__unit = 1.0
            return obj

        if (
            isinstance(alpha, UnitExprBase)
            and alpha.base_exponents == alpha.base_exponents_zero
        ):
            obj = super().__le__(other * alpha.base_factor)
            obj.__unit = 1.0
            return obj

        raise OperationNotSupported(self, other, "<=")

    def __ge__(self, other) -> QArray:
        if self.unit == other.unit:
            obj = super().__ge__(other)
            obj.__unit = 1.0
            return obj

        alpha = other.unit / self.unit

        if isinstance(alpha, Real):
            obj = super().__ge__(other * alpha)
            obj.__unit = 1.0
            return obj

        if (
            isinstance(alpha, UnitExprBase)
            and alpha.base_exponents == alpha.base_exponents_zero
        ):
            obj = super().__ge__(other * alpha.base_factor)
            obj.__unit = 1.0
            return obj

        raise OperationNotSupported(self, other, "<=")

    def __gt__(self, other) -> QArray:
        if self.unit == other.unit:
            obj = super().__gt__(other)
            obj.__unit = 1.0
            return obj

        alpha = other.unit / self.unit

        if isinstance(alpha, Real):
            obj = super().__gt__(other * alpha)
            obj.__unit = 1.0
            return obj

        if (
            isinstance(alpha, UnitExprBase)
            and alpha.base_exponents == alpha.base_exponents_zero
        ):
            obj = super().__gt__(other * alpha.base_factor)
            obj.__unit = 1.0
            return obj

        raise OperationNotSupported(self, other, "<=")

    def __lt__(self, other) -> QArray:
        if self.unit == other.unit:
            obj = super().__lt__(other)
            obj.__unit = 1.0
            return obj

        alpha = other.unit / self.unit

        if isinstance(alpha, Real):
            obj = super().__lt__(other * alpha)
            obj.__unit = 1.0
            return obj

        if (
            isinstance(alpha, UnitExprBase)
            and alpha.base_exponents == alpha.base_exponents_zero
        ):
            obj = super().__lt__(other * alpha.base_factor)
            obj.__unit = 1.0
            return obj

        raise OperationNotSupported(self, other, "<=")
