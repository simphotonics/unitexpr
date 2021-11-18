"""
Numpy array with the additional attribute `unit`.
"""

from __future__ import annotations

from typing import Union

import numpy as np

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

    def __str__(self) -> str:
        return super().__str__() + " unit: " + str(self.unit)

    def __repr__(self) -> str:
        return super().__repr__() + " unit: " + str(self.unit)

    @property
    def unit(self):
        """
        Returns the unit of the object.
        """
        return self.__unit

    @unit.setter
    def unit(self, value) -> None:
        if isinstance(value, self._unit_types):
            if value.factor == 1.0:
                self.__unit = value
            elif value.factor == 0.0:
                raise ValueError(
                    f"Could not set unit with zero magnitude: {value}."
                )
            else:
                self *= value.factor
                self.__unit = value / value.factor
        elif isinstance(value, (float, int)):
            if value == 1.0:
                self.__unit = value
            else:
                self *= value
                self.__unit = 1.0
        else:
            raise TypeError(
                "Could not set array unit. Expected a numeric value "
                + f"or a unit! Found: {type(value)}: {value}."
            )

    def __add__(self, other) -> QArray:
        scaling_factor = self.unit.scaling_factor(other.unit)
        if scaling_factor == 1.0:
            obj = super().__add__(other)
            obj.unit = self.unit
            return obj

        if not scaling_factor:
            raise OperationNotSupported(self, other, "+")

        obj = super().__add__(other * scaling_factor)
        obj.unit = self.unit
        return obj

    def __sub__(self, other) -> QArray:
        scaling_factor = self.unit.scaling_factor(other.unit)
        if scaling_factor == 1.0:
            obj = super().__sub__(other)
            obj.unit = self.unit
            return obj

        if not scaling_factor:
            raise OperationNotSupported(self, other, "-")

        obj = super().__sub__(other * scaling_factor)
        obj.unit = self.unit
        return obj

    def __mul__(self, other) -> QArray:
        """
        Returns the result of multiplying the united ndarray `self`
        with `other`.
        """
        if isinstance(other, UnitBase):
            obj = self.copy()
            obj.unit = self.unit * other
            return obj

        if isinstance(other, UnitExprBase):
            if other.factor == 1.0:
                obj = self.copy()
                obj.unit = self.unit * other
            else:
                obj = self.__mul__(other.factor)
                obj.unit = self.unit * other.unit.scale(1.0 / other.factor)
            return obj

        obj = super().__mul__(other)
        try:
            obj.unit = self.unit * other.unit
        except AttributeError:
            obj.unit = self.unit
        return obj

    def __rmul__(self, other) -> QArray:
        """
        Returns the result of multiplying `other` with the united array
        `self`.
        """
        if isinstance(other, UnitBase):
            obj = self.copy()
            obj.unit = other * self.unit
            return obj

        if isinstance(other, UnitExprBase):
            if other.factor == 1.0:
                obj = self.copy()
                obj.unit = other * self.unit
            else:
                obj = self.__mul__(other.factor)
                obj.unit = other.unit.scale(1.0 / other.factor) * self.unit
            return obj

        obj = super().__mul__(other)
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
        if isinstance(other, UnitBase):
            obj = self.copy()
            obj.unit = self.unit / other
            return obj

        if isinstance(other, UnitExprBase):
            if other.factor == 1.0:
                obj = self.copy()
                obj.unit = self.unit / other
            else:
                obj = self.__truediv__(other.factor)
                obj.unit = self.unit / other.unit.scale(other.factor)
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
