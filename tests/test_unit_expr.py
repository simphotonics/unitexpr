# import pytest

from unitexpr.si_units import SiUnit, m, s, c

SiUnitExpr = SiUnit.expr_type

factor = 10.0
v = SiUnit('v', 'meter/second', 'speed', expr=10.0*m/s)

#
# Expressions
v_expr = SiUnitExpr.from_dict({v: 1})
one = SiUnit.expr_type.one
two = SiUnitExpr.from_dict({}, 2)


class TestUnitExprFactor:

    def test_default(self):
        assert SiUnitExpr.from_dict({}).factor == 1

    def test_mul(self):
        assert (one*10).factor == 10
        assert (10*one).factor == 10

    def test_div(self):
        assert (one/10).factor == 1/10
        assert (10/one).factor == 10

    def test_pow(self):
        assert (one**10).factor == 1
        assert (SiUnitExpr.from_dict({}, 10)**10).factor == 10**10


class TestUnitExprEqual:
    def test_equal_string(self):
        assert SiUnitExpr.from_dict({}) != 'A string.'

    def test_equal_numerical(self):
        assert one == 1
        assert two == 2
        assert 1 == one
        assert 2 == two

    def test_equal_unit(self):
        assert m*1 == m
        assert 1*m == m
        assert 1*m == m*1

    def test_equal_derived_unit(self):
        assert 1*v == v*1
        assert (v*1) == v
        assert (1*v) == (v*1)
        assert (1*v) == (v.base_expr)


class TestUnitExprStr:
    def test_str(self):
        assert str(m) == 'm'
        assert str(v) == 'v'
        assert str(v*2) == '2.0*v'
        assert str(v.base_expr) == '10.0*m*s**-1.0'
        assert str(one) == '1.0'


class TestUnitExprMul:
    def test_times_number(self):
        assert v_expr*1 == SiUnitExpr.from_dict({v: 1})
        assert v_expr*factor == SiUnitExpr.from_dict({v: 1}, factor)

    def test_times_unit(self):
        assert v_expr*m == m*v_expr
        assert v_expr*m == SiUnitExpr.from_dict({v: 1, m: 1}) == m*v

    def test_times_derived_unit(self):
        assert (m*1)*v == v*(m*1) == v*m

    def test_times_constant(self):
        assert v_expr*c == c*v_expr
        assert 2*c == c*2 == SiUnitExpr.from_dict({c: 1}, 2)


class TestUnitExprAdd:
    def test_add(self):
        assert v_expr + v_expr == v_expr
        assert v_expr + v == v


class TestUnitExprSub:
    def test_sub(self):
        assert v_expr - v_expr == v_expr
        assert v_expr - v == v


class TestUnitExprDiv:
    def test_div(self):
        assert v_expr/v_expr == one
        assert v_expr*s/m == factor
        assert v/v_expr == one


class TestUnitExprPow:
    def test_pow(self):
        assert one**10 == one
