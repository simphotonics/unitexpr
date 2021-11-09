import pytest

from unitexpr.unit import *
from unitexpr.si_units import m, s, kg, c, SiUnit
from scimath.units.length import meter
from scimath.units.time import second
from scimath.units.mass import kilogram

factor = 10.0
SiUnitExpr = SiUnit.expr_type

v = SiUnit('v', 'meter/second', 'speed', expr=10.0*m/s)

# Expressions
v_expr = SiUnitExpr.from_dict({v: 1})
one = SiUnit.expr_type.one
two = 2.0*one


class TestUnitFactor:

    def test_default(self):
        assert m.factor == 1


class TestUnitEqual:
    def test_equal_unit(self):
        assert m == m
        assert m == m*1
        assert m == 1*m*m/m
        assert m.expr == m
        assert m.expr == m*1


class TestUnitStr:
    def test_str(self):
        assert str(m) == 'm'


class TestUnitInfo:
    def test_type(self):
        assert isinstance(c.info, SiUnit.info_type)

    def test_equal(self):
        assert c.info.symbol == 'c'
        assert c.info.sub_exponents == (1.0, -1.0)
        assert c.info.sub_terms == (m, s)


class TestUnitMul:
    def test_times_number(self):
        assert m*1 == SiUnitExpr.from_dict({m: 1})
        assert m*factor == SiUnitExpr.from_dict({m: 1}, factor)

    def test_times_unit(self):
        assert m*s == s*m
        assert m*m == SiUnitExpr.from_dict({m: 2})

    def test_times_derived_unit(self):
        assert m*v == v*(m*1) == v*m

    def test_times_constant(self):
        assert m*c == c*m


class TestUnitAdd:
    def test_add(self, benchmark):
        w = v**2
        w1 = v*v

        def compare():
            return kg*v == v*kg
        benchmark.pedantic(compare, iterations=10000, rounds=10)

        assert m + m == m

    def test_add_symb(self, benchmark):
        v = 10*meter/second
        w = second**-1*meter

        def compare():
            return kilogram*v == v*kilogram

        benchmark.pedantic(compare, iterations=10000, rounds=10)
        assert 1 == 1

    def test_add_incompatible_units(self):
        with pytest.raises(OperationNotSupported):
            impossible_unit = m + s
            impossible_unit == m + s


class TestUnitSubtraction:
    def test_sub(self):
        assert m - m == m

    def test_sub_incompatible_units(self):
        with pytest.raises(OperationNotSupported):
            impossible_unit = m - s
            impossible_unit == m - s


class TestUnitDivision:
    def test_div(self):
        assert v/v == one
        assert v/(v**2) == 1/v
        assert v/c == SiUnitExpr.from_dict({v: 1, c: -1})


class TestUnitPower:
    def test_pow(self):
        assert m**10 == SiUnitExpr.from_dict({m: 10})
