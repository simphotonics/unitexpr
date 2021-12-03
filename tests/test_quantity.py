import pytest

from numpy import array_equal

from unitexpr.si_units import m, s, SiUnit
from unitexpr import Quantity
from unitexpr.errors import OperationNotSupported


cm = SiUnit("cm", "centimeter", "length", expr=1e-2 * m)

a = Quantity(10)

m1 = Quantity(20, unit=m, info="Court yard length.")
s1 = Quantity(30, unit=s)


class TestQuantity:
    def test_default(self):
        assert a.unit == 1.0
        assert a.unit == m.expr_type.one

    def test_info(self):
        assert m1.info == "Court yard length."

    def test_value(self):
        assert m1.value == 20
        assert s1.value == 30

    def test_set_unit(self):
        x = a.copy()
        x.unit = 1000 * m / s
        assert x[0] == 1.0e4
        assert x.unit.factor == 1.0

    def test_mul(self):
        assert (m1 * s1).unit == m * s

    def test_mul_unit(self):
        assert (m1 * s).unit == m * s

    def test_rmul(self):
        assert (3.0 * m1).unit == m

    def test_rmul_unit(self):
        assert (m * s1).unit == m * s

    def test_add(self):
        unit = getattr(m1 + m1, "unit", "Hello ->")

        assert unit == m
        A = Quantity(1.0, unit=m)
        B = Quantity(10, unit=cm)
        C = A + B
        assert C.unit == m
        assert C[0] == 1.1

        D = B + A
        assert D.unit == cm
        assert D[0] == 110

    def test_add_incompat(self):
        with pytest.raises(OperationNotSupported):
            assert m1 + s1

    def test_sub(self):
        assert (s1 - s1).unit == s
        A = Quantity(1.0, unit=m)
        B = Quantity(10, unit=cm)
        C = A - B
        assert C.unit == m
        assert C[0] == 0.9

        D = B - A
        assert D.unit == cm
        assert D[0] == -90

    def test_sub_incompat(self):
        with pytest.raises(OperationNotSupported):
            assert m1 - s1

    def test_truediv(self):
        assert (m1 / s).unit == m / s

    def test_pow(self):
        assert (s1 ** 2).unit == s ** 2

    def test_abs(self):
        assert (abs(s1).unit) == s

    def test_neg(self):
        assert (-s1).unit == s

    def test_pos(self):
        assert (+s1).unit == s

    def test_lt(self):
        with pytest.raises(OperationNotSupported):
            m1 < s1
        A = Quantity(1.0, unit=m)
        B = Quantity(10, unit=cm)
        assert array_equal(A < B, [0])

    def test_gt(self):
        with pytest.raises(OperationNotSupported):
            m1 > s1
        A = Quantity(1.0, unit=m)
        B = Quantity(10, unit=cm)
        assert array_equal(A > B, [1])

    def test_le(self):
        with pytest.raises(OperationNotSupported):
            m1 <= s1
        A = Quantity(1.0, unit=m)
        B = Quantity(10, unit=cm)
        assert array_equal(A <= B, [0])

    def test_ge(self):
        with pytest.raises(OperationNotSupported):
            m1 >= s1
        A = Quantity(1.0, unit=m)
        B = Quantity(10, unit=cm)
        assert array_equal(A >= B, [1])
