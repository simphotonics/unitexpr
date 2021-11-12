from decimal import DivisionByZero
import pytest

from unitexpr.unit import *
from unitexpr.si_units import m, s, kg, c, SiUnit
from scimath.units.length import meter
from scimath.units.time import second
from scimath.units.mass import kilogram

factor = 10.0
SiUnitExpr = SiUnit.expr_type

v = SiUnit("v", "meter/second", "speed", expr=10.0 * m / s)

# Expressions
v_expr = v * 1.0
one = SiUnit("one", "one", "integer", SiUnit.expr_type.one)
ten = SiUnit("ten", "ten", "integer", 10.0 * SiUnit.expr_type.one)
seven = SiUnit("seven", "seven", "integer", 7 * SiUnit.expr_type.one)
zero = SiUnit("zero", "zero", "integer", one * 0.0)


class TestUnitFactor:
    def test_default(self):
        assert m.factor == 1


class TestUnitEqual:
    def test_equal_unit(self):
        assert m == m
        assert m == m * 1
        assert m == 1 * m * m / m
        assert m.expr == m
        assert m.expr == m * 1
        assert zero == 0.0
        assert zero == one * 0.0


class TestUnitStr:
    def test_str(self):
        assert str(m) == "m"


class TestUnitInfo:
    def test_type(self):
        assert isinstance(c.info, SiUnit.info_type)

    def test_equal(self):
        assert c.info.symbol == "c"
        assert c.info.sub_exponents == (1.0, -1.0)
        assert c.info.sub_terms == (m, s)


class TestUnitMul:
    def test_times_number(self):
        assert m * 1 == SiUnitExpr.from_dict({m: 1})
        assert m * factor == SiUnitExpr.from_dict({m: 1}, factor)

    def test_times_unit(self):
        assert m * s == s * m
        assert m * m == SiUnitExpr.from_dict({m: 2})
        assert m * zero == 0.0 * m

    def test_times_derived_unit(self):
        assert m * v == v * (m * 1) == v * m

    def test_times_constant(self):
        assert m * c == c * m


class TestUnitAdd:
    def test_add_unit(self):
        assert m + m == 2.0 * m
        assert c + c == 2.0 * c

    def test_add_unit_number(self):
        assert ten + ten == 2.0 * ten
        assert ten + seven == 1.7 * ten
        assert seven + ten == 17 / 7 * seven

    def test_add_number(self):
        assert ten + 7 == 1.7 * ten
        assert 7 + ten == 1.7 * ten
        assert ten + 0 == ten
        assert 0 + ten == ten
        assert ten + zero == ten
        assert zero + ten == ten

    def test_add_incompatible_units(self):
        with pytest.raises(OperationNotSupported):
            impossible_unit = m + s
            assert impossible_unit == m + s


class TestUnitSubtraction:
    def test_sub_unit(self):
        assert m - m == 0.0 * m
        assert c - c == 0.0 * c

    def test_sub_unit_number(self):
        assert ten - ten == 0.0 * ten
        assert ten - seven == 0.3 * ten
        assert seven - ten == -3 / 7 * seven
        assert zero - ten == -ten
        assert ten - zero == ten

    def test_sub_number(self):
        assert ten - 7 == 0.3 * ten
        assert 7 - ten == -0.3 * ten
        assert ten - 0 == ten
        assert 0 - ten == -ten

    def test_sub_incompatible_units(self):
        with pytest.raises(OperationNotSupported):
            impossible_unit = m - s
            assert impossible_unit == m - s


class TestUnitDivision:
    def test_div(self):
        assert v / v == one
        assert v / (v ** 2) == 1 / v
        assert v / c == SiUnitExpr.from_dict({v: 1, c: -1})
        assert zero / c == 0.0 / c

    def test_div_unit_number(self):
        assert m / ten == 0.1 * m
        assert ten / m == 10 * m ** -1

    def test_div_zero(self):
        with pytest.raises(ZeroDivisionError):
            assert m / zero == m / 0


class TestUnitPower:
    def test_pow(self):
        assert m ** 10 == SiUnitExpr.from_dict({m: 10})
        assert s ** 10 * s ** -9 == s
        assert zero ** 10 == zero
        assert zero ** 0.5 == zero
