"""
Module providing the classes:

* UnitMeta
* UnitBase
"""

from operator import add, sub, neg
from typing import Any, Iterable, NamedTuple, Tuple, Union


from .decorators import protect
from .errors import OperationNotSupported
from .unit_symbol import UnitSymbol

from ._unitexpr import UnitExprMeta, UnitExprBase


class UnitMeta(type):
    """
    Meta class of objects representing physical units.
    """

    def __new__(
        cls, cls_name, bases, attrs, unit_symbols: Iterable[UnitSymbol]
    ):
        attrs["__slots__"] = tuple()
        return super().__new__(
            cls,
            cls_name,
            bases,
            attrs,
        )

    def __init__(
        self, cls_name, bases, attrs, unit_symbols: Iterable[UnitSymbol]
    ):

        # Define the unit expression type.
        expr_type = UnitExprMeta(
            cls_name=cls_name + "Expr",
            bases=(UnitExprBase,),
            attrs={"__slots__": tuple()},
            unit_symbols=unit_symbols,
            unit_type=self,
        )
        self.expr_type = expr_type

        # Define base units.
        base_dimensions = len(unit_symbols)
        zero = [0.0] * base_dimensions
        base_units = []
        for index, unit_symbol in enumerate(unit_symbols):
            vector = zero.copy()
            vector[index] = 1.0
            base_unit = self(
                unit_symbol.symbol,
                unit_symbol.name,
                unit_symbol.quantity,
                self.expr_type(
                    terms=(unit_symbol.symbol,),
                    exponents=(1.0,),
                    factor=1.0,
                    base_exponents=tuple(vector),
                    base_factor=1.0,
                ),
            )
            base_units.append(base_unit)
            setattr(self, unit_symbol.symbol, base_unit)

        self.base_units = tuple(base_units)
        self.base_exponents_zero = tuple(zero)
        self.valid_types = (self, self.expr_type)
        self.info_type = NamedTuple(
            "UnitInfo",
            symbol=str,
            name=str,
            quantity=str,
            terms=Tuple[UnitMeta],
            exponents=Tuple[float],
            factor=float,
            base_exponents=Tuple[float],
            base_factor=float,
            sub_terms=Tuple[str],
            sub_exponents=Tuple[str],
            sub_factor=float,
        )
        super().__init__(cls_name, bases, attrs)

    def is_base_unit(self, unit):
        """
        Returns `True` if `unit` is a base unit and `False` otherwise.
        """
        return unit in self.base_units

    # The decorator protects all attributes from modification
    # (after they have been initially set).
    # Any attempt at modification will raise an error of type
    # ProtectedAttributeError.
    @protect()
    def __setattr__(self, name: str, value: Any) -> None:
        return super().__setattr__(name, value)


class UnitBase(
    NamedTuple(
        "_UnitBase",
        symbol=str,
        name=str,
        quantity=str,
        base_exponents=Tuple[float],
        base_factor=float,
        sub_terms=Tuple[UnitMeta],
        sub_exponents=Tuple[float],
        sub_factor=float,
    ),
):
    """Base class of objects representing physical units.

    To generate unit systems subclass `UnitBase` providing the base unit
    symbols. The base units will be available as class attributes (see
    example below).

    ``` python
    # Defining unit symbols
    unit_symbols = (
        UnitSymbol(symbol='m','name'='meter',quantity='length'),
        UnitSymbol(symbol='s','name'='second',quantity='time'),
    )
    # Sub-classing the base class `UnitBase`
    class MetricUnit(UnitBase, metaclass=UnitMeta,
          unit_symbols=unit_symbols):
        pass
    # Base units are available as class attributes.
    m = MetricUnit.m
    s = MetricUnit.s
    # Declaring derived units
    c = MetricUnit('c', 'speed of light', 'velocity', expr=299792458*m/s)
    ```
    """

    __slots__ = ()

    def __new__(
        cls, symbol: str, name: str, quantity: str, expr: UnitExprBase
    ):
        if cls == UnitBase:
            raise TypeError(f"Class {cls} must be subclassed.")

        if not isinstance(expr, cls.expr_type):
            raise TypeError(
                f"Expected expression of type {cls.expr_type}. "
                + f"Found {type(expr)}."
            )

        return super().__new__(
            cls,
            symbol,
            name,
            quantity,
            base_exponents=expr.base_exponents,
            base_factor=expr.base_factor,
            sub_terms=expr.terms,
            sub_exponents=expr.exponents,
            sub_factor=expr.factor,
        )

    def __eq__(self, other: object) -> bool:
        """
        Returns `True` if:
        * the unit `self` and the unit/unit-expression `other` match when
        resolved in terms of base units.
        * other is numeric and the resolved expression of `self` represents a
        the same number. (All base exponents must be zero).
        """
        if isinstance(other, self.expr_type):
            return (
                self.base_factor == other.base_factor
                and self.base_exponents == other.base_exponents
            )

        if isinstance(other, (int, float)):
            return (
                self.base_exponents == self.base_exponents_zero
                and self.base_factor == other
            )

        return self is other

    def __ne__(self, other: object) -> bool:
        """
        Returns `True` if:
        * the unit `self` and the unit/unit-expression `other`
          do not match when resolved in terms of base units.
        * other is numeric and the resolved expression of `self` represents a
        different number. (All base exponents must be zero).
        """
        if isinstance(other, self.expr_type):
            return (
                self.base_factor != other.base_factor
                or self.base_exponents != other.base_exponents
            )

        if isinstance(other, (int, float)):
            return (
                self.base_exponents != self.base_exponents_zero
                or self.base_factor != other
            )

        return self is other

    def __hash__(self) -> int:
        return id(self)

    def __repr__(self):
        """
        Returns a string representation of the unit object.
        """
        return self.symbol

    def __str__(self):
        """
        Returns a string representation of the unit object.
        """
        return self.symbol

    @property
    def info(self) -> NamedTuple:
        """
        Returns a `NamedTuple` containing detailed object information.
        """
        return self.info_type(
            self.symbol,
            self.name,
            self.quantity,
            (self,),
            self.exponents,
            self.factor,
            self.base_exponents,
            self.base_factor,
            self.sub_terms,
            self.sub_exponents,
            self.sub_factor,
        )

    @property
    def expr(self) -> UnitExprBase:
        """
        Returns an expression representing `self` in terms of
        `sub_terms`.
        ``` python
        J = SiUnit('J', 'Joule', 'energy', expr=N*m)
        print(J.expr)  # prints: N*m
        ```
        """
        return self.expr_type(
            terms=self.sub_terms,
            exponents=self.sub_exponents,
            factor=self.sub_factor,
            base_exponents=self.base_exponents,
            base_factor=self.base_factor,
        )

    @property
    def self_expr(self) -> UnitExprBase:
        """
        Returns an expression representing `self` in terms of `self`.
        An alternative method of converting a unit to a unit expression is
        multiplication by 1.0.
        ``` python
        J = SiUnit('J', 'Joule', 'energy', expr=N*m)
        assert J.self_expr == J
        assert J.self_expr == 1.0*J
        assert type(J.self_expr) == SiUnit.expr_type

        print(J_expr) # Prints: J
        ```
        """
        return self.expr_type(
            terms=(self,),
            exponents=(1.0,),
            factor=1.0,
            base_exponents=self.base_exponents,
            base_factor=self.base_factor,
        )

    @property
    def factor(self) -> float:
        """
        Returns the (scaling) `factor` of the unit expression.
        Always returns 1.0.
        """
        return 1.0

    @property
    def terms(self) -> Tuple[str]:
        """
        Returns the `terms` of the unit expression.
        """
        return (self,)

    @property
    def exponents(self) -> Tuple[float]:
        """
        Returns the exponents of the unit expression.
        """
        return (1.0,)

    @property
    def base_expr(self) -> UnitExprBase:
        """
        Returns an expression representing self in terms of base units.
        """
        dexpr = {}
        for term, exponent in zip(self.base_units, self.base_exponents):
            if exponent == 0.0:
                continue
            dexpr[term] = exponent
        return self.expr_type(
            dexpr.keys(),
            dexpr.values(),
            factor=self.base_factor,
            base_exponents=self.base_exponents,
            base_factor=self.base_factor,
        )

    # ---------
    # Operators
    # ---------
    def __add__(self, other) -> UnitExprBase:
        """
        Returns the result of adding `self` and `other`.

        Note: The form of the expression is determined by the left operand
        unless the the left operand has `base_factor` zero.
        """
        if (
            isinstance(other, self.valid_types)
            and self.base_exponents == other.base_exponents
        ):
            if self.base_factor == 0:
                return (
                    other
                    if isinstance(other, UnitExprBase)
                    else other.self_expr
                )

            base_factor = self.base_factor + other.base_factor
            factor = base_factor / self.base_factor  # self.factor == 1.0

            return self.expr_type(
                self.terms,
                self.exponents,
                factor,
                self.base_exponents,
                base_factor,
            )

        if (
            isinstance(other, (float, int))
            and self.base_exponents == self.base_exponents_zero
        ):
            base_factor = self.base_factor + other

            if self.base_factor == 0:
                return self.expr_type.one * base_factor

            factor = base_factor / self.base_factor  # self.factor == 1.0

            return self.expr_type(
                self.terms,
                self.exponents,
                factor,
                self.base_exponents,
                base_factor,
            )

        raise OperationNotSupported(self, other, "+")

    def __radd__(self, other):
        """
        Returns the result of adding `other` and `self`.

        Note: The form of the expression is determined by the
        left operand unless the the left operand has
        `base_factor` zero.
        """
        if (
            isinstance(other, self.valid_types)
            and self.base_exponents == other.base_exponents
        ):
            if other.base_factor == 0 or not other.terms:
                return self.self_expr

            base_factor = other.base_factor + self.base_factor
            factor = base_factor / other.base_factor * other.factor

            return self.expr_type(
                other.terms,
                other.exponents,
                factor,
                other.base_exponents,
                base_factor,
            )

        if (
            isinstance(other, (float, int))
            and self.base_exponents == self.base_exponents_zero
        ):
            if other == 0:
                return self.self_expr

            if self.base_factor == 0:
                return self.one * other

            base_factor = other + self.base_factor
            factor = base_factor / self.base_factor  # self.factor == 1.0

            return self.expr_type(
                self.terms,
                self.exponents,
                factor,
                self.base_exponents,
                base_factor,
            )

        raise OperationNotSupported(other, self, "+")

    def __pos__(self):
        return self

    def __sub__(self, other):
        """
        Returns the result of subtracting `other` from `self`.
        """
        if (
            isinstance(other, self.valid_types)
            and self.base_exponents == other.base_exponents
        ):
            if self.base_factor == 0:
                return -other

            base_factor = self.base_factor - other.base_factor
            factor = base_factor / self.base_factor  # self.factor == 1.0

            return self.expr_type(
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
                return self.expr_type.one * base_factor

            factor = base_factor / self.base_factor  # self.factor == 1.0

            return self.expr_type(
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

            factor = base_factor / other.base_factor * other.factor

            return self.expr_type(
                other.terms,
                other.exponents.exponents,
                factor,
                other.base_exponents,
                base_factor,
            )

        if (
            isinstance(other, (float, int))
            and self.base_exponents == self.base_exponents_zero
        ):
            base_factor = other - self.base_factor

            if self.base_factor == 0 or not self.terms:
                return self.one * base_factor

            factor = base_factor / self.base_factor

            return self.expr_type(
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
        return self.expr_type(
            self.terms,
            self.exponents,
            factor=-self.factor,
            base_exponents=self.base_exponents,
            base_factor=-self.base_factor,
        )

    def __abs__(self) -> UnitExprBase:
        """
        Returns a unit expression representing the absolute value of `self`.
        """
        return self.expr_type(
            terms=self.terms,
            exponents=self.exponents,
            factor=abs(self.factor),
            base_exponents=self.base_exponents,
            base_factor=abs(self.base_factor),
        )

    def __mul__(self, other) -> UnitExprBase:
        """
        Returns the result of multiplying `self` with `other`.

        - `self`: Left operand.
        - `other`: Right operand`.
        """
        if isinstance(other, self.valid_types):
            return self.expr_type(
                self.terms + other.terms,
                self.exponents + other.exponents,
                factor=self.factor * other.factor,
                base_exponents=tuple(
                    map(add, self.base_exponents, other.base_exponents)
                ),
                base_factor=self.base_factor * other.base_factor,
            )

        if isinstance(other, (int, float)):
            return self.expr_type(
                self.terms,
                self.exponents,
                factor=other * self.factor,
                base_exponents=self.base_exponents,
                base_factor=other * self.base_factor,
            )

        try:
            return other.__rmul__(self)
        except TypeError as error:
            raise OperationNotSupported(self, other, "*") from error

    def __rmul__(self, other) -> UnitExprBase:
        """
        Returns the result of multiplying `other` with `self`.

        - `other`: Left operand.
        - `self`: Right operand`.
        """
        if isinstance(other, self.valid_types):
            return self.expr_type(
                other.terms + self.terms,
                other.exponents + self.exponents,
                factor=other.factor * self.factor,
                base_exponents=tuple(
                    map(add, self.exponents, other.exponents)
                ),
                base_factor=self.base_factor * self.base_factor,
            )

        if isinstance(other, (int, float)):
            return self.expr_type(
                terms=self.terms,
                exponents=self.exponents,
                factor=other,
                base_exponents=self.base_exponents,
                base_factor=other * self.base_factor,
            )

        raise OperationNotSupported(other, self, "*")

    def __truediv__(self, other) -> UnitExprBase:
        """
        Returns the result of: `self` / `other`.
        - `self`: Left operand.
        - `other`: Right operand.
        """
        if isinstance(other, self.valid_types):
            return self.expr_type(
                self.terms + other.terms,
                self.exponents + tuple(map(neg, other.exponents)),
                self.factor / other.factor,
                tuple(map(sub, self.base_exponents, other.base_exponents)),
                self.base_factor / other.base_factor,
            )

        if isinstance(other, (int, float)):
            return self.expr_type(
                self.terms,
                self.exponents,
                factor=self.factor / other,
                base_exponents=self.base_exponents,
                base_factor=self.base_factor / other,
            )

        try:
            return other.__rtruediv__(self)
        except TypeError:
            raise OperationNotSupported(self, other, "/")

    def __rtruediv__(self, other) -> UnitExprBase:
        """
        Returns the result of: `other` / `self`.
        - `self`: Right operand.
        - `other`: Left operand.
        """
        if isinstance(other, self.valid_types):
            return self.expr_type(
                self.terms,
                self.exponents,
                factor=other / self.factor,
                base_exponents=self.base_exponents,
                base_factor=other / self.base_factor,
            )

        if isinstance(other, (int, float)):
            return self.expr_type(
                self.terms,
                self.exponents,
                factor=other / self.factor,
                base_exponents=tuple(map(neg, self.base_exponents)),
                base_factor=other / self.base_factor,
            )

        raise OperationNotSupported(other, self, "/")

    def scaling_factor(self, other) -> Union[float, None]:
        """
        Returns the scaling factor that converts the unit
        `self` to the unit expression or unit `other`.

        Returns `None` if `self` cannot be converted to `other`
        by multiplication with a number of type `int` or `float`.
        """
        if isinstance(other, self.valid_types):
            if other.base_exponents != self.base_exponents:
                return None
            return other.base_factor / self.base_factor

        if isinstance(other, (int, float)):
            if self.base_exponents != self.base_exponents_zero:
                return None
            return other / self.base_factor

        return None

    def __pow__(self, other: int) -> UnitExprBase:
        """
        Returns the result of: self**other.
        """
        if isinstance(other, (int, float)):
            other = float(other)
            return self.expr_type(
                self.terms,
                tuple([entry * other for entry in self.exponents]),
                self.factor ** other,
                base_exponents=tuple(
                    [entry * other for entry in self.base_exponents]
                ),
                base_factor=self.base_factor ** other,
            )

        raise OperationNotSupported(self, other, "**")
