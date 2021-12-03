from numpy import array_equal
from unitexpr import Quantity
from unitexpr.si_units import m, s

Q1 = Quantity(1.0, m ** 2)
Q2 = Quantity(1.0, s)


class TestAddition:
    def test_add_quantity(self, benchmark):
        def add():
            return Q1 + Q1

        benchmark.pedantic(add, iterations=700, rounds=4)
        assert add().unit == m ** 2
        assert array_equal(add(), [2.0])


class TestMul:
    def test_mul_quantity(self, benchmark):
        def expr():
            return Q1 / (Q2 ** 2)

        benchmark.pedantic(expr, iterations=700, rounds=4)
        assert expr().unit == m ** 2 / s ** 2

    def test_mul_quantity_unit(self, benchmark):
        def expr():
            return Q1 / s ** 2

        benchmark.pedantic(expr, iterations=700, rounds=4)
        assert expr().unit == m ** 2 / s ** 2
