from __future__ import annotations

from operator import add, neg, sub
from typing import TYPE_CHECKING, Any, Iterable, NamedTuple, Tuple, Type

from .decorators import protect
from .errors import OperationNotSupported
from .unit_dict import UnitDict
from .unit_symbol import UnitSymbol

if TYPE_CHECKING:
    from .unit import UnitBase


class UnitExprMeta(type):
    """
    Meta-class of objects representing unit expressions. Initializes
    class attributes.
    """

    def __new__(
        cls,
        cls_name,
        bases,
        attrs,
        unit_symbols: Tuple[UnitSymbol],
        unit_type: Type,
    ):
        attrs["unit_symbols"] = tuple(unit_symbols)
        attrs["dim"] = len(unit_symbols)
        attrs["base_exponents_zero"] = (0.0,) * attrs["dim"]
        attrs["unit_type"] = unit_type
        return super().__new__(cls, cls_name, bases, attrs)

    def __init__(
        self,
        cls_name,
        bases,
        attrs,
        unit_symbols: Iterable[UnitSymbol],
        unit_type: Type,
    ):
        self.one = self(
            terms=(),
            exponents=(),
            factor=1.0,
            base_exponents=self.base_exponents_zero,
            base_factor=1.0,
        )
        self.valid_types = (self, self.unit_type)
        super().__init__(cls_name, bases, attrs)

    @protect()
    def __setattr__(self, name: str, value: Any) -> None:
        return super().__setattr__(name, value)


class UnitExprBase(
    NamedTuple(
        "_UnitExprBase",
        terms=Tuple["UnitBase"],
        exponents=Tuple[float],
        factor=float,
        base_exponents=Tuple[float],
        base_factor=float,
    ),
):
    """
    Class representing an expression (multiplication) of
    units and real numbers.
    """

    __slots__ = ()

    def __new__(
        cls,
        terms: Tuple[UnitBase],
        exponents: Tuple[float],
        factor: float,
        base_exponents: Tuple[float],
        base_factor: float,
    ):
        """
        Constructs a new unit expression instance.
        This method is reserved for internal use. Parameters are not
        validated.

        To create consistent unit expression combine
        existing units and unit expressions using the arithmetic operators
        `+`, `-`, `*`, `/`, and `**`.

        * terms: A tuple with entries of type `cls.unit_type`.
        * exponents: The expression exponent for each term.
        * factor: A scaling factor of type `int` or `float`.
        * base_exponents: The exponents with respect to the system
        base units.
        * base_factor: The scaling factor of the expression when written
        in terms of base unit.
        """
        if cls is UnitExprBase:
            raise TypeError(f"Instantiation of {cls} not allowed.")

        return super().__new__(
            cls, terms, exponents, factor, base_exponents, base_factor
        )

    @classmethod
    def from_dict(cls, dexpr: dict, factor: float = 1.0):
        """
        Returns a unit expression representing the terms and
        exponents specified in `dict` and scaled with `factor`.

        Note: Unit expression classes are available after creating
        a unit class and can be accessed using the
        class attribute `expr_type` (see example below).

        ``` python
        # Type shortcut
        SiUnitExpr = SiUnit.expr_type
        expr = SiUnitExpr(dexpr={m:1, s:-1}, factor=10.0)
        print(expr)
        # Prints: 10.0*m*s**-1
        ```
        """
        base_exponents = cls.base_exponents_zero
        base_factor = factor
        for term, exponent in dexpr.items():
            cls.validate_term(term)
            base_exponents = list(
                map(
                    add,
                    base_exponents,
                    [x * exponent for x in term.base_exponents],
                )
            )
            base_factor *= term.base_factor ** exponent

        return cls(
            tuple(dexpr.keys()),
            tuple(dexpr.values()),
            factor,
            tuple(base_exponents),
            base_factor,
        )

    def scale(self, factor: float) -> UnitExprBase:
        """
        Returns a copy of the unit expression `self` scaled by `factor`.
        """
        return self.__class__(
            terms=self.terms,
            exponents=self.exponents,
            factor=factor * self.factor,
            base_exponents=self.base_exponents,
            base_factor=factor * self.base_factor,
        )

    @classmethod
    def validate_term(cls, term) -> None:
        """
        Raises a `TypeError` if `term` does not have type `cls.unit_type`.
        """
        if not isinstance(term, cls.unit_type):
            raise TypeError(
                "Unit expression contains an invalid term: "
                + f"'{term}' of type '{type(term)}'. \n "
                + f"Expected objects of type: {cls}."
            )

    @property
    def dexpr(self):
        """
        Return the unit expression in the form of a dictionary with keys
        containing the unit symbols and values containing the
        corresponding exponent.

        Note: The actual expression is scaled with the instance attribute
        `factor`.
        """
        dexpr = UnitDict()
        for term, exponent in zip(self.terms, self.exponents):
            dexpr[term] = dexpr.get(term, 0.0) + exponent
        return dexpr.filter_value(0.0)

    def __str__(self):
        """
        Returns a string representing the expression defined by `terms`
        and `factor`.
        """
        out = ""
        for term, exponent in self.dexpr.items():
            if exponent == 1:
                out = out + "*" + str(term)
            elif exponent == 0:
                continue
            else:
                out = out + "*" + str(term) + "**" + str(exponent)

        if not out:
            return str(self.factor)

        # Strip leading '*'
        out = out[1:]
        if self.factor != 1:
            out = str(self.factor) + "*" + out
        return out

    def __repr__(self):
        """
        Returns a string represenation of self.
        """

        out = ""
        for term, exponent in self.dexpr.items():
            if exponent == 1.0:
                out = out + "*" + str(term)
            elif exponent == 0.0:
                continue
            else:
                out = out + "*" + str(term) + "**" + str(exponent)

        if not out:
            return str(self.factor) + "*" + self.__class__.__name__ + ".one"

        # Strip leading '*'
        out = out[1:]
        if self.factor != 1.0:
            out = str(self.factor) + "*" + out
        return out

    @property
    def repr(self) -> NamedTuple:
        """
        Returns a namedtuple containing detailed object information.
        """
        return super().__repr__()

    @property
    def base_repr(self):
        """
        Returns a string representing the unit expression in terms
        of base units.
        """
        out = ""
        for term, exponent in zip(self.unit_symbols, self.base_exponents):
            if exponent == 1.0:
                out = out + "*" + term.symbol
            elif exponent == 0.0:
                continue
            else:
                out = out + "*" + term.symbol + "**" + str(exponent)
        out = out[1:]
        if not out:
            out = str(self.base_factor)
        elif self.base_factor != 1:
            out = str(self.base_factor) + "*" + out
        return out

    @property
    def base_expr(self):
        """
        Returns an expression of self in terms of base units.
        """
        dexpr = UnitDict()
        for term, exponent in zip(
            self.unit_type.base_units, self.base_exponents
        ):
            if exponent == 0.0:
                continue
            dexpr[term] = exponent

        return self.__class__(
            terms=dexpr.keys(),
            exponents=dexpr.values(),
            factor=self.base_factor,
            base_exponents=self.base_exponents,
            base_factor=self.base_factor,
        )

    def __eq__(self, other: object) -> bool:
        """
        Returns `True` if:
        * the expressions `self` and `other` match when
          resolved in terms of base units.
        * other is numeric and the resolved expression of `self` represents the
        same number. (All base exponents must be zero).
        """
        if isinstance(other, self.valid_types):
            return (
                self.base_factor == other.base_factor
                and self.base_exponents == other.base_exponents
            )

        if isinstance(other, (int, float)):
            return (
                self.base_exponents == self.base_exponents_zero
                and self.base_factor == other
            )

        return False

    def __ne__(self, other: object) -> bool:
        """
        Returns `True` if:
        * the expressions `self` and `other` do not match when
          resolved in terms of base units.
        * other is numeric and the resolved expression of `self` represents a
        different number. (All base exponents must be zero).
        """
        if isinstance(other, self.valid_types):
            return (
                self.base_factor != other.base_factor
                or self.base_exponents != other.base_exponents
            )

        if isinstance(other, (int, float)):
            return (
                self.base_exponents != self.base_exponents_zero
                or self.base_factor != other
            )

        return True

    def __req__(self, other: object) -> bool:
        """
        Returns `True` if:
        * the expressions `self` and `other` match when
          resolved in terms of base units.
        * other is numeric and the resolved expression of `self` represents the
        same number.
        """
        return self.__eq__(other)

    def __abs__(self) -> UnitExprBase:
        """
        Returns a unit expression representing the absolute value of `self`.
        """
        return self.__class__(
            terms=self.terms,
            exponents=self.exponents,
            factor=abs(self.factor),
            base_exponents=self.base_exponents,
            base_factor=abs(self.base_factor),
        )

    def __add__(self, other) -> UnitExprBase:
        """
        Returns the result of adding the unit expression `self` and `other`.
        """
        if (
            isinstance(other, self.valid_types)
            and self.base_exponents == other.base_exponents
        ):
            if self.base_factor == 0 or not self.terms:
                return (
                    other if isinstance(other, UnitExprBase) else other * 1.0
                )

            base_factor = self.base_factor + other.base_factor
            factor = (
                self.factor
                + other.factor * other.base_factor / self.base_factor
            )

            return self.__class__(
                terms=self.terms,
                exponents=self.exponents,
                factor=factor,
                base_exponents=self.base_exponents,
                base_factor=base_factor,
            )

        if (
            isinstance(other, (float, int))
            and self.base_exponents == self.base_exponents_zero
        ):
            base_factor = self.base_factor + other

            if self.base_factor == 0 or not self.terms:
                return self.one * base_factor

            factor = self.factor + other / self.base_factor

            return self.__class__(
                self.terms,
                self.exponents,
                factor,
                self.base_exponents,
                base_factor,
            )

        raise OperationNotSupported(self, other, "+")

    def __radd__(self, other) -> UnitExprBase:
        """
        Returns the result of adding `other` and the unit expression `self`.
        """
        if (
            isinstance(other, self.valid_types)
            and self.base_exponents == other.base_exponents
        ):

            if other.base_factor == 0 or not other.terms:
                return self

            base_factor = other.base_factor + self.base_factor
            factor = (
                other.factor
                + self.factor * self.base_factor / other.base_factor
            )

            return self.__class__(
                terms=other.terms,
                exponents=other.exponents,
                factor=factor,
                base_exponents=other.base_exponents,
                base_factor=base_factor,
            )

        if (
            isinstance(other, (float, int))
            and self.base_exponents == self.base_exponents_zero
        ):
            if other == 0:
                return self

            if self.base_factor == 0 or not self.terms:
                return self.one * other

            base_factor = other + self.base_factor

            factor = self.factor + other / self.base_factor

            return self.__class__(
                self.terms,
                self.exponents,
                factor,
                self.base_exponents,
                base_factor,
            )

        raise OperationNotSupported(other, self, "+")

    def __sub__(self, other):
        """
        Returns the result of subtracting `other` from `self`.
        """
        if (
            isinstance(other, self.valid_types)
            and self.base_exponents == other.base_exponents
        ):
            if self.base_factor == 0 or not self.terms:
                return -other

            base_factor = self.base_factor - other.base_factor

            factor = (
                self.factor
                - other.factor * other.base_factor / self.base_factor
            )

            return self.__class__(
                terms=self.terms,
                exponents=self.exponents,
                factor=factor,
                base_exponents=self.base_exponents,
                base_factor=base_factor,
            )

        if (
            isinstance(other, (float, int))
            and self.base_exponents == self.base_exponents_zero
        ):
            base_factor = self.base_factor - other

            if self.base_factor == 0 or not self.terms:
                return self.one * base_factor

            factor = self.factor - other / self.base_factor

            return self.__class__(
                self.terms,
                self.exponents,
                factor,
                self.base_exponents,
                base_factor,
            )

        raise OperationNotSupported(self, other, "-")

    def __rsub__(self, other):
        """
        Returns the result of subtracting `self` from `other`.
        """
        if (
            isinstance(other, self.valid_types)
            and self.base_exponents == other.base_exponents
        ):
            if other.base_factor == 0 or not other.terms:
                return -self

            base_factor = other.base_factor - self.base_factor

            factor = (
                other.factor
                - self.factor * self.base_factor / other.base_factor
            )
            return self.__class__(
                terms=other.terms,
                exponents=other.exponents.exponents,
                factor=factor,
                base_exponents=other.base_exponents,
                base_factor=base_factor,
            )

        if (
            isinstance(other, (float, int))
            and self.base_exponents == self.base_exponents_zero
        ):
            base_factor = other - self.base_factor

            if self.base_factor == 0 or not self.terms:
                return self.one * base_factor

            factor = other / self.base_factor - self.factor

            return self.__class__(
                self.terms,
                self.exponents,
                factor,
                self.base_exponents,
                base_factor,
            )

        raise OperationNotSupported(other, self, "-")

    def __neg__(self) -> UnitExprBase:
        """
        Negation operator.
        """
        return self.__class__(
            self.terms,
            self.exponents,
            factor=-self.factor,
            base_exponents=self.base_exponents,
            base_factor=-self.base_factor,
        )

    def __mul__(self, other) -> "UnitExprBase":
        """
        Returns the result of multiplying `self` with `other`.

        - `self`: Left operand.
        - `other`: Right operand`.
        """
        if isinstance(other, self.valid_types):
            return self.__class__(
                self.terms + other.terms,
                self.exponents + other.exponents,
                self.factor * other.factor,
                tuple(map(add, self.base_exponents, other.base_exponents)),
                self.base_factor * other.base_factor,
            )

        if isinstance(other, (int, float)):
            other = float(other)
            return self.__class__(
                self.terms,
                self.exponents,
                self.factor * other,
                self.base_exponents,
                self.base_factor * other,
            )

        raise OperationNotSupported(self, other, "*")

    def __rmul__(self, other) -> "UnitExprBase":
        """
        Returns the result of multiplying `other` with `self`.

        - `other`: Left operand.
        - `self`: Right operand`.
        """
        if isinstance(other, self.valid_types):
            return self.__class__(
                other.terms + self.terms,
                other.exponents + self.exponents,
                self.factor * other.factor,
                tuple(map(add, self.base_exponents, other.base_exponents)),
                self.base_factor * other.base_factor,
            )

        if isinstance(other, (int, float)):
            other = float(other)
            return self.__class__(
                self.terms,
                self.exponents,
                factor=self.factor * other,
                base_exponents=self.base_exponents,
                base_factor=self.base_factor * other,
            )
        raise OperationNotSupported(self, other, "*")

    def __truediv__(self, other) -> "UnitExprBase":
        """
        Returns the result of: `self` / `other`.
        - `self`: Left operand.
        - `other`: Right operand.
        """
        if isinstance(other, (int, float)):
            return self.__class__(
                self.terms,
                self.exponents,
                self.factor / other,
                self.base_exponents,
                self.base_factor / other,
            )

        if isinstance(other, self.valid_types):
            return self.__class__(
                self.terms + other.terms,
                self.exponents + tuple(map(neg, other.exponents)),
                self.factor / other.factor,
                tuple(map(sub, self.base_exponents, other.base_exponents)),
                self.base_factor / other.base_factor,
            )

        raise OperationNotSupported(self, other, "/")

    def __rtruediv__(self, other):
        """
        Returns the result of: `other` / `self`.
        - `self`: Right operand.
        - `other`: Left operand.
        """
        if isinstance(other, (int, float)):
            return self.__class__(
                self.terms,
                tuple(map(neg, self.exponents)),
                other / self.factor,
                tuple(-exponent for exponent in self.base_exponents),
                other / self.base_factor,
            )

        if isinstance(other, self.valid_types):
            return self.__class__(
                other.terms + self.terms,
                tuple(map(neg, other.exponents)) + self.exponents,
                other.factor / self.factor,
                tuple(map(sub, other.base_exponents, self.base_exponents)),
                other.base_factor / self.base_factor,
            )

        raise OperationNotSupported(other, self, "/")

    def __pow__(self, other: int):
        """
        Returns the result of: self**other.
        """
        if isinstance(other, (int, float)):
            return self.__class__(
                self.terms,
                tuple([exponent * other for exponent in self.exponents]),
                self.factor ** other,
                tuple([exponent * other for exponent in self.base_exponents]),
                self.base_factor ** other,
            )

        raise OperationNotSupported(self, other, "**")