from numpy import array_equal, ndarray

from scimath.units.length import centimeter, meter
from scimath.units.time import second
from scimath.units.unit_array import UnitArray as UnitArraySci

from unitexpr.qarray import QArray
from unitexpr.si_units import SiUnit, m, s

cm = SiUnit("cm", "centimeter", "length", 1.0e-2 * m)

nx = 200
ny = 200

A = ndarray(shape=(nx, ny))
A.fill(10.0)

M = QArray.from_input(A, unit=m ** 2)

C = QArray(shape=(nx, ny), unit=cm ** 2)
C.fill(1.0e4)

S = QArray.from_input(A, unit=s)

R = QArray(shape=(nx, ny), unit=m ** 2)
R.fill(11)


A1 = UnitArraySci(A)
M1 = UnitArraySci(A, units=meter * meter)
C1 = UnitArraySci(C, units=centimeter * centimeter)
S1 = UnitArraySci(A, units=second)
R1 = UnitArraySci(R, units=meter * meter)


class TestAddition:
    def test_add_qarray(self, benchmark):
        def add():
            return M + C

        benchmark.pedantic(add, iterations=700, rounds=4)
        assert add().unit == m ** 2
        assert array_equal(add(), R)

    def test_add_unit_array(self, benchmark):
        def add():
            return M1 + C1

        benchmark.pedantic(add, iterations=700, rounds=4)
        assert add().units == meter ** 2
        assert array_equal(add(), R1)


class TestMul:
    def test_mult_qarray(self, benchmark):
        def expr():
            return M / S ** 2

        benchmark.pedantic(expr, iterations=700, rounds=4)
        assert expr().unit == m ** 2 * s ** -2

    def test_mult_unit_array(self, benchmark):
        def expr():
            return M1 / (S1 ** 2)

        benchmark.pedantic(expr, iterations=700, rounds=4)
        assert expr().units == meter ** 2 / second ** 2
