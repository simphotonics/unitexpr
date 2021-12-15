"""
Module providing the classes:

* UnitMeta
* UnitBase
"""
from __future__ import annotations

from typing import Any, Iterable, NamedTuple, Tuple

from lockattrs import protect

from ._unitexpr import UnitExprBase, UnitExprMeta, UnitExprMixin
from .unit_symbol import UnitSymbol


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
            (UnitExprMixin, *bases),
            attrs,
        )

    def __init__(
        self, cls_name, bases, attrs, unit_symbols: Iterable[UnitSymbol]
    ):

        # Define the unit expression type.
        expr_type = UnitExprMeta(
            cls_name=cls_name + "Expr",
            bases=(UnitExprMixin, UnitExprBase),
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
    )
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

        return self is not other

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
            tuple(dexpr.keys()),
            tuple(dexpr.values()),
            factor=self.base_factor,
            base_exponents=self.base_exponents,
            base_factor=self.base_factor,
        )

    # ---------
    # Operators
    # ---------
