import pytest

from numpy import ndarray, array_equal

from unitexpr.si_units import m, s
from unitexpr.unit_array import UnitArray

from scimath.units.length import meter
from scimath.units.time import second
from scimath.units.mass import kilogram

from scimath.units.unit_array import UnitArray as UnitArraySci


A = ndarray(shape=(1000,1000))
A.fill(10.0)

M = UnitArray(shape=(1000, 1000), unit=m**2)
M.fill(10.0)

S = UnitArray(shape=(1000, 1000), unit=s)
S.fill(10.0)


A1 = UnitArraySci(A)
M1 = UnitArraySci(A, units=meter*meter)
S1 = UnitArraySci(A, units=second)

class TestAddition:
    def test_add_unitexpr(self, benchmark):
        def add():
            return M + M

        benchmark.pedantic(add, iterations=500, rounds=2)
        assert add().unit == m**2
        assert array_equal(add(),2.0*M)

    def test_add_scimath_units(self, benchmark):
        def add():
            return M1 + M1

        benchmark.pedantic(add, iterations=500, rounds=2)
        assert add().units == meter**2
        assert array_equal(add(),2.0*M1)


class TestMul:
    def test_mult_unitexpr(self, benchmark):
        def expr():
            return M/S**2

        benchmark.pedantic(expr, iterations=500, rounds=2)
        assert expr().unit == m**2*s**-2

    def test_mult_scimath_units(self, benchmark):
        def expr():
            return M1/(S1**2)

        benchmark.pedantic(expr, iterations=500, rounds=2)
        assert expr().units == meter**2/second**2
