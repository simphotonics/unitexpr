from numpy import ndarray, array_equal

from unitexpr.si_units import m, s, SiUnit
from unitexpr.unit_array import UnitArray

from scimath.units.length import meter, centimeter
from scimath.units.time import second
from scimath.units.mass import kilogram

from scimath.units.unit_array import UnitArray as UnitArraySci

cm = SiUnit("cm", "centimeter", "length", 1.0e-2 * m)

nx = 200
ny = 200

A = ndarray(shape=(nx, ny))
A.fill(10.0)

M = UnitArray(shape=(nx, ny), unit=m ** 2)
M.fill(10.0)

C = UnitArray(shape=(nx, ny), unit=cm ** 2)
C.fill(1.0e4)

S = UnitArray(shape=(nx, ny), unit=s)
S.fill(10.0)

R = UnitArray(shape=(nx, ny), unit=m ** 2)
R.fill(11)


A1 = UnitArraySci(A)
M1 = UnitArraySci(A, units=meter * meter)
C1 = UnitArraySci(C, units=centimeter * centimeter)
S1 = UnitArraySci(A, units=second)

R1 = UnitArraySci(R, units=meter * meter)


class TestAddition:
    def test_add_unitexpr_units(self, benchmark):
        def add():
            return M + C

        benchmark.pedantic(add, iterations=500, rounds=2)
        assert add().unit == m ** 2
        assert array_equal(add(), R)

    def test_add_scimath_units(self, benchmark):
        def add():
            return M1 + C1

        benchmark.pedantic(add, iterations=500, rounds=2)
        assert add().units == meter ** 2
        assert array_equal(add(), R1)


class TestMul:
    def test_mult_unitexpr_units(self, benchmark):
        def expr():
            return M / S ** 2

        benchmark.pedantic(expr, iterations=500, rounds=2)
        assert expr().unit == m ** 2 * s ** -2

    def test_mult_scimath_units(self, benchmark):
        def expr():
            return M1 / (S1 ** 2)

        benchmark.pedantic(expr, iterations=500, rounds=2)
        assert expr().units == meter ** 2 / second ** 2
