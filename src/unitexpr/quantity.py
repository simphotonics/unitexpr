from __future__ import annotations

from numbers import Number
from typing import Callable, Union

from .errors import OperationNotSupported
from .unit import UnitBase, UnitExprBase


class Quantity:
    """
    A quantity that can be described by a numerical value
    of type `int`, `float`, or `complex` and a unit.
    The attribute `info` can be used to store object information in the
    form of a string.
    """

    _unit_types = (UnitBase, UnitExprBase)

    __slots__ = ("__value", "__unit", "info")

    def __new__(
        cls,
        value: Number,
        unit: Union[UnitBase, UnitExprBase, float] = 1.0,
        info: str = "",
    ) -> Quantity:
        """
        Returns an object of type `Quantity`. The object attributes
        are set in `__init__`.
        """
        return super().__new__(cls)

    def __init__(
        self,
        value: Number,
        unit: Union[UnitBase, UnitExprBase, float] = 1.0,
        info: str = "",
    ):
        """
        Initializes object attributes.
        """
        self.info = info
        self.__value, self.__unit = self.__normalize(value, unit)
        self.__unit = unit

    @classmethod
    def __idem(
        cls,
        value: Number,
        unit: Union[UnitBase, UnitExprBase, float] = 1.0,
        info: str = "",
    ) -> Quantity:
        """
        Constructs an object of type `Quantity` without normalizing the unit.
        """
        obj = super().__new__(cls)
        obj.__value = value
        obj.__unit = unit
        obj.info = info
        return obj

    @property
    def unit(self):
        """Returns the unit of the quantity."""
        return self.__unit

    @property
    def value(self):
        """Returns the numerical value of the quantity."""
        return self.__value

    @classmethod
    def __normalize(cls, value, unit) -> tuple:
        """
        Returns a tuple with entries scaled value and normalized unit.
        The function is used in `__init__`.
        """
        if not isinstance(value, Number):
            raise TypeError(
                f"Parameter 'value' must be numerical. Found {value}."
            )

        try:
            factor = (
                unit.factor
                if isinstance(unit, cls._unit_types)
                else float(unit)
            )
        except ValueError as error:
            raise ValueError(
                "Expected a 'unit', a 'unit expression', or input that be "
                + f"converted to a float. Found:{unit.__repr__()}."
            ) from error

        if factor == 1.0:
            return (value, unit)

        if factor == 0.0:
            raise ValueError(
                f"Could not set unit with zero magnitude: {value}."
            )
        return (value * factor, unit / factor)

    def __str__(self) -> str:
        """Returns a string representing `self`."""
        return f"{self.__value} {self.__unit}"

    def __repr__(self) -> str:
        """Returns a string representing `self`."""
        result = (
            f"{self.__class__.__name__}({self.__value}, "
            + f"unit={self.__unit}"
        )

        if self.info.strip():
            result += f", info={self.info.__repr__()})"
        else:
            result += ")"
        return result

    def copy(self):
        """Returns a copy of `self`."""
        return self.__idem(self.__value, self.__unit, self.info)

    def __add__(self, other) -> Quantity:
        """Returns the result of adding `self` and `other`."""
        other_unit = getattr(other, "unit", 1.0)
        other_value = getattr(other, "value", other)

        # If units match simply add values.
        if self.__unit == other_unit:
            return self.__idem(self.__value + other_value, self.__unit)

        alpha = other_unit / self.__unit

        if isinstance(alpha, float):
            return self.__idem(self.__value + other_value * alpha, self.__unit)

        if (
            isinstance(alpha, UnitExprBase)
            and alpha.base_exponents == alpha.base_exponents_zero
        ):
            return self.__idem(
                self.__value + other_value * alpha.base_factor, self.__unit
            )
        raise OperationNotSupported(self, other, "+")

    def __sub__(self, other) -> Quantity:
        """Returns the result of subtracting `other` from `self`."""
        other_unit = getattr(other, "unit", 1.0)
        other_value = getattr(other, "value", other)

        # If units match simply subtract values.
        if self.__unit == other_unit:
            return self.__idem(self.__value - other_value, self.__unit)

        alpha = other_unit / self.__unit

        if isinstance(alpha, float):
            return self.__idem(self.__value - other_value * alpha, self.__unit)

        if (
            isinstance(alpha, UnitExprBase)
            and alpha.base_exponents == alpha.base_exponents_zero
        ):
            return self.__idem(
                self.__value - other_value * alpha.base_factor, self.__unit
            )
        raise OperationNotSupported(self, other, "-")

    def __mul__(self, other) -> Quantity:
        """
        Returns the result of multiplying `self` with `other`.
        """
        if isinstance(other, self._unit_types):
            return self.__class__(self.__value, self.__unit * other)

        other_unit = getattr(other, "unit", 1.0)
        other_value = getattr(other, "value", other)
        try:
            return self.__class__(
                self.__value * other_value, self.__unit * other_unit
            )
        except TypeError:
            return NotImplemented

    def __rmul__(self, other) -> Quantity:
        """
        Returns the result of multiplying `other` with `self`.
        """
        if isinstance(other, self._unit_types):
            return self.__class__(self.__value, other * self.__unit)

        other_unit = getattr(other, "unit", 1.0)
        other_value = getattr(other, "value", other)
        return self.__class__(
            other_value * self.__value,
            other_unit * self.__unit,
        )

    def __truediv__(self, other) -> Quantity:
        """
        Returns the result of dividing the `self` by `other`.
        """
        if isinstance(other, self._unit_types):
            return self.__class__(self.__value, self.__unit / other)

        other_unit = getattr(other, "unit", 1.0)
        other_value = getattr(other, "value", other)

        try:
            return self.__class__(
                self.__value / other_value,
                self.__unit / other_unit,
            )
        except TypeError:
            return NotImplemented

    def __rtruediv__(self, other) -> Quantity:
        """
        Returns the result of dividing `other` by `self`.
        """
        if isinstance(other, self._unit_types):
            return self.__class__(self.__value, other / self.__unit)

        other_unit = getattr(other, "unit", 1.0)
        other_value = getattr(other, "value", other)
        return self.__class__(
            other_value / self.__value,
            other_unit / self.__unit,
        )

    def __pow__(self, other: Union[float, int]) -> Quantity:
        """Returns the result of `self ** other`."""
        return self.__class__(self.__value ** other, self.__unit ** other)

    def __abs__(self) -> Quantity:
        """Returns `abs(self)`. Note: The operator affects the value only."""
        return self.__idem(self.__value.__abs__(), self.__unit)

    def __neg__(self) -> Quantity:
        """Returns `-self`. Note: The operator affects the value only."""
        return self.__idem(-self.__value, self.__unit)

    def __pos__(self) -> Quantity:
        """Returns `+self`. Note: The operator affects the value only."""
        return self.__idem(self.__value.__pos__(), self.__unit)

    def __eq__(self, other) -> bool:
        """Returns `True` if `self == other` and `False` otherwise."""
        result = self.compare(other, self.__value.__eq__)
        if result is None:
            return False
        return result

    def __le__(self, other) -> bool:
        """Returns `True` if `self <= other` and `False` otherwise."""
        result = self.compare(other, self.__value.__le__)
        if result is None:
            raise OperationNotSupported(self, other, "<=")
        return result

    def __ge__(self, other) -> bool:
        """Returns `True` if `self >= other` and `False` otherwise."""
        result = self.compare(other, self.__value.__ge__)
        if result is None:
            raise OperationNotSupported(self, other, ">=")
        return result

    def __gt__(self, other) -> bool:
        """Returns `True` if `self > other` and `False` otherwise."""
        result = self.compare(other, self.__value.__gt__)
        if result is None:
            raise OperationNotSupported(self, other, ">")
        return result

    def __lt__(self, other) -> bool:
        """Returns `True` if `self < other` and `False` otherwise."""
        result = self.compare(other, self.__value.__lt__)
        if result is None:
            raise OperationNotSupported(self, other, "<")
        return result

    def compare(
        self, other, comparison_operator: Callable
    ) -> Union[bool, None]:
        """
        Generic comparison function that handles input of type `Number`,
        `ndarray` and `qarray` using `comparison_operator`.

        Returns `None` if the comparison failed due to incompatible units.
        """
        other_unit = getattr(other, "unit", 1.0)
        other_value = getattr(other, "value", other)

        if self.__unit == other_unit:
            return comparison_operator(other_value)

        alpha = other_unit / self.__unit

        if isinstance(alpha, float):
            return comparison_operator(other_value * alpha)

        if (
            isinstance(alpha, UnitExprBase)
            and alpha.base_exponents == alpha.base_exponents_zero
        ):
            return comparison_operator(other_value * alpha.base_factor)

        return None
