from unitexpr import Quantity
from unitexpr.si_units import m, s

Q1 = Quantity(10.0, m ** 2)
Q2 = Quantity(20.0, s)


class TestAddition:
    def test_add_quantity(self, benchmark):
        def add():
            return Q1 + Q1

        benchmark.pedantic(add, iterations=700, rounds=4)
        assert add().unit == m ** 2
        assert add() == Quantity(20.0, m ** 2)


class TestDiv:
    def test_div_quantity(self, benchmark):
        def expr():
            return Q1 / Q2

        benchmark.pedantic(expr, iterations=700, rounds=4)
        assert expr().unit == m ** 2 / s
        assert expr() == Quantity(0.5, m ** 2 / s)

    def test_div_unit(self, benchmark):
        def expr():
            return Q1 / s

        benchmark.pedantic(expr, iterations=700, rounds=4)
        assert expr().unit == m ** 2 / s
        assert expr() == Quantity(10.0, m ** 2 / s)


class TestMul:
    def test_mul_quantity(self, benchmark):
        def expr():
            return Q1 * Q2

        benchmark.pedantic(expr, iterations=700, rounds=4)
        assert expr().unit == m ** 2 * s
        assert expr() == Quantity(200.0, m ** 2 * s)

    def test_mul_unit(self, benchmark):
        def expr():
            return Q1 * s

        benchmark.pedantic(expr, iterations=700, rounds=4)
        assert expr().unit == m ** 2 * s
        assert expr() == Quantity(10.0, m ** 2 * s)
