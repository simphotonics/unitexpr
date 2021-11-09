'''
Module providing the classes:

* UnitMeta
* UnitExprMeta
* UnitBase
* UnitExprBase
'''

from operator import add, sub, neg
from typing import Any, Iterable, NamedTuple, Tuple, Type

from .decorators import protect
from .errors import OperationNotSupported
from .unit_dict import UnitDict
from .unit_symbol import UnitSymbol


class UnitMeta(type):
    '''
    Meta class of objects representing physical units.
    '''
    def __new__(
            cls,
            cls_name,
            bases,
            attrs,
            unit_symbols: Iterable[UnitSymbol]):
        attrs['__slots__'] = tuple()
        return super().__new__(cls, cls_name, bases, attrs,)

    def __init__(self, cls_name, bases, attrs,
                 unit_symbols: Iterable[UnitSymbol]):

        # Define the unit expression type.
        expr_type = UnitExprMeta(
            cls_name=cls_name + 'Expr',
            bases=(UnitExprBase,),
            attrs={'__slots__': tuple()},
            unit_symbols=unit_symbols,
            unit_type=self)
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
        self.valid_types = (self, self.expr_type)
        self.info_type = NamedTuple(
            'UnitInfo', symbol=str, name=str, quantity=str,
            terms=Tuple[UnitMeta], exponents=Tuple[float], factor=float,
            base_exponents=Tuple[float], base_factor=float,
            sub_terms=Tuple[str], sub_exponents=Tuple[str], sub_factor=float,
        )
        super().__init__(cls_name, bases, attrs)

    def is_base_unit(self, unit):
        '''
        Returns `True` if `unit` is a base unit and `False` otherwise.
        '''
        return unit in self.base_units

    # The decorator protects all attributes from modification
    # (after they have been initially set).
    # Any attempt at modification will raise an error of type
    # ProtectedAttributeError.
    @protect()
    def __setattr__(self, name: str, value: Any) -> None:
        return super().__setattr__(name, value)


class UnitExprMeta(type):
    '''
    Meta-class of objects representing unit expressions. Initializes
    class attributes.
    '''
    def __new__(
            cls, cls_name, bases, attrs,
            unit_symbols: Iterable[UnitSymbol],
            unit_type: Type,
    ):
        attrs['unit_symbols'] = tuple(unit_symbols)
        attrs['dim'] = len(unit_symbols)
        attrs['base_exponents_zero'] = (0.0, ) * attrs['dim']
        attrs['unit_type'] = unit_type
        return super().__new__(cls, cls_name, bases, attrs)

    def __init__(
            self, cls_name, bases, attrs,
            unit_symbols: Iterable[UnitSymbol],
            unit_type: Type,
    ):
        self.one = self(
            terms=(),
            exponents=(),
            factor=1.0,
            base_exponents=self.base_exponents_zero,
            base_factor=1.0
        )
        self.valid_types = (self, self.unit_type)
        super().__init__(cls_name, bases, attrs)

    @protect()
    def __setattr__(self, name: str, value: Any) -> None:
        return super().__setattr__(name, value)


class UnitExprBase(NamedTuple(
        '_UnitExprBase',
        terms=Tuple[UnitMeta],
        exponents=Tuple[float],
        factor=float,
        base_exponents=Tuple[float],
        base_factor=float,
    ),
):
    '''
    Class representing an expression (multiplication) of
    units and real numbers.
    '''
    __slots__ = ()

    def __new__(
            cls, terms: Tuple[UnitMeta], exponents: Tuple[float],
            factor: float, base_exponents: Tuple[float],
            base_factor: float):
        if cls is UnitExprBase:
            raise TypeError(f'Instantiation of {cls} not allowed.')

        return super().__new__(cls, terms, exponents,
                               factor, base_exponents, base_factor)

    @classmethod
    def from_dict(cls, dexpr: dict, factor: float = 1.0):
        '''
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
        '''
        base_exponents = cls.base_exponents_zero
        base_factor = factor
        for term, exponent in dexpr.items():
            cls.validate_term(term)
            base_exponents = list(map(add, base_exponents, [
                                  x*exponent for x in term.base_exponents]))
            base_factor *= term.base_factor**exponent

        return cls(tuple(dexpr.keys()),
                   tuple(dexpr.values()),
                   factor,
                   tuple(base_exponents),
                   base_factor,
                   )

    def scale(self, factor: float) -> UnitExprMeta:
        '''
        Returns a copy of the unit expression `self` scaled by `factor`.
        '''
        return self.__class__(
            terms=self.terms,
            exponents=self.exponents,
            factor=factor*self.factor,
            base_exponents=self.base_exponents,
            base_factor=factor*self.base_factor
        )

    @classmethod
    def validate_term(cls, term) -> None:
        '''
        Raises a `TypeError` if `term` does not have type `cls.unit_type`.
        '''
        if not isinstance(term, cls.unit_type):
            raise TypeError(
                'Unit expression contains an invalid term: ' +
                f'\'{term}\' of type \'{type(term)}\'. \n ' +
                f'Expected objects of type: {cls}.')

    @property
    def dexpr(self):
        '''
        Return the unit expression in the form of a dictionary with keys
        containing the unit symbols and values containing the
        corresponding exponent.

        Note: The actual expression is scaled with the instance attribute
        `factor`.
        '''
        dexpr = UnitDict()
        for term, exponent in zip(self.terms, self.exponents):
            dexpr[term] = dexpr.get(term, 0.0) + exponent
        return dexpr.filter_value(0.0)

    def __str__(self):
        '''
        Returns a string representing the expression defined by `terms`
        and `factor`.
        '''
        out = ''
        for term, exponent in self.dexpr.items():
            if exponent == 1:
                out = out + '*' + str(term)
            elif exponent == 0:
                continue
            else:
                out = out + '*' + str(term) + '**' + str(exponent)

        if not out:
            return str(self.factor)

        # Strip leading '*'
        out = out[1:]
        if self.factor != 1:
            out = str(self.factor) + '*' + out
        return out

    def __repr__(self):
        '''
        Returns a string represenation of self.
        '''

        out = ''
        for term, exponent in self.dexpr.items():
            if exponent == 1.0:
                out = out + '*' + str(term)
            elif exponent == 0.0:
                continue
            else:
                out = out + '*' + str(term) + '**' + str(exponent)

        if not out:
            return str(self.factor) + '*' + self.__class__.__name__ + '.one'

        # Strip leading '*'
        out = out[1:]
        if self.factor != 1.0:
            out = str(self.factor) + '*' + out
        return out

    @property
    def repr(self) -> NamedTuple:
        '''
        Returns a namedtuple containing detailed object information.
        '''
        return super().__repr__()

    @property
    def base_repr(self):
        '''
        Returns a string representing the unit expression in terms
        of base units.
        '''
        out = ''
        for term, exponent in zip(self.unit_symbols, self.base_exponents):
            if exponent == 1.0:
                out = out + '*' + term.symbol
            elif exponent == 0.0:
                continue
            else:
                out = out + '*' + term.symbol + '**' + str(exponent)
        out = out[1:]
        if not out:
            out = str(self.base_factor)
        elif self.base_factor != 1:
            out = str(self.base_factor) + '*' + out
        return out

    def __eq__(self, other: object) -> bool:
        '''
        Returns `True` if:
        * the expressions `self` and `other` match when
          resolved in terms of base units.
        * other is numeric and the resolved expression of `self` represents the
        same number. (All base exponents must be zero).
        '''
        if isinstance(other, self.__class__.valid_types):
            return self.base_factor == other.base_factor and \
                self.base_exponents == other.base_exponents

        if isinstance(other, (int, float)):
            return self.base_exponents == self.base_exponents_zero and \
                self.base_factor == other

        return False

    def __ne__(self, other: object) -> bool:
        '''
        Returns `True` if:
        * the expressions `self` and `other` do not match when
          resolved in terms of base units.
        * other is numeric and the resolved expression of `self` represents a
        different number. (All base exponents must be zero).
        '''
        if isinstance(other, self.__class__.valid_types):
            return self.base_factor != other.base_factor or \
                self.base_exponents != other.base_exponents

        if isinstance(other, (int, float)):
            return self.base_exponents != self.base_exponents_zero or \
                self.base_factor != other

        return True

    def __req__(self, other: object) -> bool:
        '''
        Returns `True` if:
        * the expressions `self` and `other` match when
          resolved in terms of base units.
        * other is numeric and the resolved expression of `self` represents the
        same number.
        '''
        return self.__eq__(other)

    def __add__(self, other):
        '''
        Returns the result of adding `self` and `other`.
        '''
        if self == other:
            return self

        raise OperationNotSupported(self, other, '+')

    def __radd__(self, other):
        '''
        Returns the result of adding `other` and `self`.
        '''
        try:
            self.__add__(other)
        except OperationNotSupported as error:
            raise error.invert()

    def __sub__(self, other):
        '''
        Returns the result of subtracting `other` from `self`.
        '''
        if self == other:
            return self

        raise OperationNotSupported(self, other, '-')

    def __rsub__(self, other):
        '''
        Returns the result of subtracting `self` from `other`.
        '''
        try:
            self.__sub__(other)
        except OperationNotSupported as error:
            raise error.invert()

    def __mul__(self, other) -> 'UnitExprBase':
        '''
        Returns the result of multiplying `self` with `other`.

        - `self`: Left operand.
        - `other`: Right operand`.
        '''
        if isinstance(other, self.__class__.valid_types):
            return self.__class__(
                self.terms + other.terms,
                self.exponents + other.exponents,
                self.factor * other.factor,
                tuple(map(add,
                          self.base_exponents,
                          other.base_exponents)
                      ),
                self.base_factor * other.base_factor,
            )

        if isinstance(other, (int, float)):
            other = float(other)
            return self.__class__(
                self.terms,
                self.exponents,
                self.factor*other,
                self.base_exponents,
                self.base_factor*other,
            )

        raise OperationNotSupported(self, other, '*')

    def __rmul__(self, other) -> 'UnitExprBase':
        '''
        Returns the result of multiplying `other` with `self`.

        - `other`: Left operand.
        - `self`: Right operand`.
        '''
        if isinstance(other, self.__class__.valid_types):
            return self.__class__(
                other.terms + self.terms,
                other.exponents + self.exponents,
                self.factor * other.factor,
                tuple(map(add,
                          self.base_exponents,
                          other.base_exponents)
                      ),
                self.base_factor * other.base_factor,
            )

        if isinstance(other, (int, float)):
            other = float(other)
            return self.__class__(
                self.terms,
                self.exponents,
                factor=self.factor*other,
                base_exponents=self.base_exponents,
                base_factor=self.base_factor*other,
            )
        raise OperationNotSupported(self, other, '*')

    def __truediv__(self, other) -> 'UnitExprBase':
        '''
        Returns the result of: `self` / `other`.
        - `self`: Left operand.
        - `other`: Right operand.
        '''
        if isinstance(other, (int, float)):
            return self.__class__(
                self.terms,
                self.exponents,
                self.factor/other,
                self.base_exponents,
                self.base_factor/other)

        if isinstance(other, self.__class__.valid_types):
            return self.__class__(
                self.terms + other.terms,
                self.exponents + tuple(map(neg, other.exponents)),
                self.factor / other.factor,
                tuple(map(sub, self.base_exponents,
                          other.base_exponents)),
                self.base_factor/other.base_factor,
            )

        raise OperationNotSupported(self, other, '/')

    def __rtruediv__(self, other):
        '''
        Returns the result of: `other` / `self`.
        - `self`: Right operand.
        - `other`: Left operand.
        '''
        if isinstance(other, (int, float)):
            return self.__class__(
                self.terms,
                tuple(map(neg, self.exponents)),
                other / self.factor,
                tuple(-exponent for exponent in self.base_exponents),
                other / self.base_factor,
            )

        if isinstance(other, self.__class__.valid_types):
            return self.__class__(
                other.terms + self.terms,
                tuple(map(neg, other.exponents)) + self.exponents,
                other.factor / self.factor,
                tuple(map(sub, other.base_exponents,
                          self.base_exponents)),
                other.base_factor/self.base_factor,
            )

        raise OperationNotSupported(other, self, '/')

    def __pow__(self, other: int):
        '''
        Returns the result of: self**other.
        '''
        if isinstance(other, (int, float)):
            return self.__class__(
                self.terms,
                tuple([exponent * other for exponent in self.exponents]),
                self.factor ** other,
                tuple([exponent * other for exponent in self.base_exponents]),
                self.base_factor ** other,
            )

        raise OperationNotSupported(self, other, '**')


class UnitBase(NamedTuple('_UnitBase',
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
    ''' Base class of objects representing physical units.

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
    '''

    __slots__ = ()

    def __new__(cls, symbol: str, name: str, quantity: str, expr: UnitExprMeta):
        if cls == UnitBase:
            raise TypeError(f'Class {cls} must be subclassed.')

        if not isinstance(expr, cls.expr_type):
            raise TypeError(f'Expected expression of type {cls.expr_type}. ' +
                            f'Found {type(expr)}.')

        return super().__new__(
            cls, symbol, name, quantity,
            base_exponents=expr.base_exponents,
            base_factor=expr.base_factor,
            sub_terms=expr.terms,
            sub_exponents=expr.exponents,
            sub_factor=expr.factor,
        )

    def __eq__(self, other: object) -> bool:
        '''
        Returns `True` if:
        * the unit `self` and the unit/unit-expression `other` match when
        resolved in terms of base units.
        * other is numeric and the resolved expression of `self` represents a
        the same number. (All base exponents must be zero).
        '''

        if isinstance(other, self.expr_type):
            return self.base_factor == other.base_factor and \
                self.base_exponents == other.base_exponents

        if isinstance(other, (int, float)):
            return self.base_exponents == self.base_exponents_zero and \
                self.base_factor == other

        return id(self) == id(other)

    def __ne__(self, other: object) -> bool:
        '''
        Returns `True` if:
        * the unit `self` and the unit/unit-expression `other` do not match when
          resolved in terms of base units.
        * other is numeric and the resolved expression of `self` represents a
        different number. (All base exponents must be zero).
        '''
        if isinstance(other, self.expr_type):
            return self.base_factor != other.base_factor or \
                self.base_exponents != other.base_exponents

        if isinstance(other, (int, float)):
            return self.base_exponents != self.base_exponents_zero or \
                self.base_factor != other

        return id(self) != id(other)

    def __hash__(self) -> int:
        return id(self)

    def __repr__(self):
        '''
        Returns a string representation of the unit object.
        '''
        return self.symbol

    def __str__(self):
        '''
        Returns a string representation of the unit object.
        '''
        return self.symbol

    @property
    def info(self) -> NamedTuple:
        '''
        Returns a `NamedTuple` containing detailed object information.
        '''
        return self.__class__.info_type(
            self.symbol, self.name, self.quantity,
            (self,),
            self.exponents, self.factor,
            self.base_exponents, self.base_factor,
            self.sub_terms, self.sub_exponents, self.sub_factor
        )

    @property
    def expr(self) -> UnitExprMeta:
        '''
        Returns an expression representing self in terms of
        `sub_terms`.
        ``` python
        c = SiUnit('c', 'speed of light', 'velocity', expr=299792458*m/s)
        c_expr = c.sub_expr()
        print(c_expr)
        # prints: 299792458.0*m*s**-1
        ```
        '''
        return self.expr_type(
            terms=self.sub_terms,
            exponents=self.sub_exponents,
            factor=self.sub_factor,
            base_exponents=self.base_exponents,
            base_factor=self.base_factor
        )

    @property
    def factor(self) -> float:
        '''
        Returns the (scaling) `factor` of the unit expression.
        Always returns 1.0.
        '''
        return 1.0

    @property
    def terms(self) -> Tuple[str]:
        '''
        Returns the `terms` of the unit expression.
        '''
        return (self,)

    @property
    def exponents(self) -> Tuple[float]:
        '''
        Returns the exponents of the unit expression.
        '''
        return (1.0,)

    @property
    def base_expr(self) -> UnitExprMeta:
        '''
        Returns an expression representing self in terms of base units.
        '''
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
            base_factor=self.base_factor)

    # ---------
    # Operators
    # ---------

    def __add__(self, other):
        '''
        Returns the result of adding `self` and `other`.
        '''
        if self == other:
            return self

        raise OperationNotSupported(self, other, '+')

    def __radd__(self, other):
        '''
        Returns the result of adding `other` and `self`.
        '''
        try:
            self.__add__(other)
        except OperationNotSupported as error:
            raise error.invert()

    def __pos__(self):
        return self

    def __sub__(self, other):
        '''
        Returns the result of subtracting `other` from `self`.
        '''
        if self == other:
            return self

        raise OperationNotSupported(self, other, '-')

    def __rsub__(self, other):
        '''
        Returns the result of subtracting `self` from `other`.
        '''
        try:
            self.__sub__(other)
        except OperationNotSupported as error:
            raise error.invert()

    def __neg__(self) -> UnitExprMeta:
        '''
        Negation operator.
        '''
        return self.expr_type(
            self.terms,
            self.exponents,
            factor=-self.factor,
            base_exponents=self.base_exponents,
            base_factor=-self.base_factor
        )

    def __abs__(self) -> UnitExprMeta:
        '''
        Returns a unit expression representing the absolute value of `self`.
        '''
        return self.expr_type(
            terms=self.terms,
            exponents=self.exponents,
            factor=abs(self.factor),
            base_exponents=self.base_exponents,
            base_factor=abs(self.base_factor)
        )

    def __mul__(self, other) -> UnitExprMeta:
        '''
        Returns the result of multiplying `self` with `other`.

        - `self`: Left operand.
        - `other`: Right operand`.
        '''
        if isinstance(other, self.__class__.valid_types):
            return self.expr_type(
                self.terms + other.terms,
                self.exponents + other.exponents,
                factor=self.factor*other.factor,
                base_exponents=tuple(
                    map(add, self.base_exponents, other.base_exponents)),
                base_factor=self.base_factor * other.base_factor)

        if isinstance(other, (int, float)):
            return self.expr_type(
                self.terms,
                self.exponents,
                factor=other*self.factor,
                base_exponents=self.base_exponents,
                base_factor=other*self.base_factor)

        try:
            return other.__rmul__(self)
        except TypeError as error:
            raise OperationNotSupported(self, other, '*') from error

    def __rmul__(self, other) -> UnitExprMeta:
        '''
        Returns the result of multiplying `other` with `self`.

        - `other`: Left operand.
        - `self`: Right operand`.
        '''
        if isinstance(other, self.__class__.valid_types):
            return self.expr_type(
                other.terms + self.terms, other.exponents + self.exponents,
                factor=other.factor * self.factor,
                base_exponents=tuple(
                    map(add, self.exponents, other.exponents)),
                base_factor=self.base_factor * self.base_factor,)

        if isinstance(other, (int, float)):
            return self.expr_type(
                terms=self.terms,
                exponents=self.exponents,
                factor=other,
                base_exponents=self.base_exponents,
                base_factor=other*self.base_factor)

        raise OperationNotSupported(other, self, '*')

    def __truediv__(self, other) -> UnitExprMeta:
        '''
        Returns the result of: `self` / `other`.
        - `self`: Left operand.
        - `other`: Right operand.
        '''
        if isinstance(other, self.__class__.valid_types):
            return self.expr_type(
                self.terms + other.terms,
                self.exponents + tuple(map(neg, other.exponents)),
                self.factor/other.factor,
                tuple(map(sub, self.base_exponents, other.base_exponents)),
                self.base_factor/other.base_factor,
            )

        if isinstance(other, (int, float)):
            return self.expr_type(
                self.terms,
                self.exponents,
                factor=self.factor/other,
                base_exponents=self.base_exponents,
                base_factor=self.base_factor/other)

        try:
            return other.__rtruediv__(self)
        except TypeError:
            raise OperationNotSupported(self, other, '/')

    def __rtruediv__(self, other) -> UnitExprMeta:
        '''
        Returns the result of: `other` / `self`.
        - `self`: Right operand.
        - `other`: Left operand.
        '''
        if isinstance(other, self.__class__.valid_types):
            return self.expr_type(
                self.terms,
                self.exponents,
                factor=other/self.factor,
                base_exponents=self.base_exponents,
                base_factor=other/self.base_factor)

        if isinstance(other, (int, float)):
            return self.expr_type(
                self.terms,
                self.exponents,
                factor=other/self.factor,
                base_exponents=tuple(map(neg, self.base_exponents)),
                base_factor=other/self.base_factor)

        raise OperationNotSupported(other, self, '/')

    def __pow__(self, other: int) -> UnitExprMeta:
        '''
        Returns the result of: self**other.
        '''
        if isinstance(other, (int, float)):
            other = float(other)
            return self.expr_type(
                self.terms,
                tuple([entry * other for entry in self.exponents]),
                self.factor ** other,
                base_exponents=tuple(
                    [entry * other for entry in self.base_exponents]),
                base_factor=self.base_factor ** other)

        raise OperationNotSupported(self, other, '**')
