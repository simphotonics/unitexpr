import pytest

from unitexpr.unit import *
from unitexpr.si_units import m, s, kg, N, SiUnit
from scimath.units.length import meter
from scimath.units.time import second
from scimath.units.mass import kilogram


v = SiUnit("v", "meter/second", "speed", expr=10.0 * m / s)

# Expressions
v_expr = v * 1.0
one = SiUnit("one", "one", "integer", SiUnit.expr_type.one)
ten = SiUnit("ten", "ten", "integer", 10.0 * SiUnit.expr_type.one)
seven = SiUnit("seven", "seven", "integer", 7 * SiUnit.expr_type.one)
zero = SiUnit("zero", "zero", "integer", one * 0.0)

v_scimath = meter / second
N_scimath = kilogram * meter / (second * second)


class TestAddition:
    def test_add_unitexpr_units(self, benchmark):
        def add():
            return m / s + m / s

        benchmark.pedantic(add, iterations=20000, rounds=4)
        assert add() == v / 5.0

    def test_add_scimath_units(self, benchmark):
        def add():
            return meter / second + meter / second

        benchmark.pedantic(add, iterations=20000, rounds=4)
        assert add() == 2.0 * meter / second


class TestComparison:
    def test_compare_unitexpr_units(self, benchmark):
        def compare():
            return v == N

        benchmark.pedantic(compare, iterations=20000, rounds=4)
        assert v == v

    def test_compare_scimath_units(self, benchmark):
        def compare():
            return v_scimath == N_scimath

        benchmark.pedantic(compare, iterations=20000, rounds=4)
        assert v_scimath == v_scimath


class TestMul:
    def test_mult_unitexpr_units(self, benchmark):
        def expr():
            return kg * m * s ** -2

        benchmark.pedantic(expr, iterations=20000, rounds=4)
        assert expr() == N

    def test_mult_scimath_units(self, benchmark):
        def expr():
            return kilogram * meter * second ** -2

        benchmark.pedantic(expr, iterations=20000, rounds=4)
        assert expr() == N_scimath
