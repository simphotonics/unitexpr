import pytest

from numpy import array_equal

from unitexpr.si_units import m, s, SiUnit
from unitexpr import QArray
from unitexpr.errors import OperationNotSupported


cm = SiUnit("cm", "centimeter", "length", expr=1e-2 * m)

a = QArray(shape=(2, 2))
a.fill(10.0)

m1 = QArray(shape=(2, 2), unit=m)
m1.fill(20.0)

s1 = QArray(shape=(2, 2), unit=s)
s1.fill(30.0)


class TestQArray:
    def test_default(self):
        assert a.unit == 1.0
        assert a.unit == m.expr_type.one

    def test_set_unit(self):
        x = a.copy()
        x.unit = 1000 * m / s
        assert x[0, 0] == 1.0e4
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
        assert (m1 + m1).unit == m
        A = QArray((2, 2), unit=m)
        A.fill(1.0)
        B = QArray((2, 2), unit=cm)
        B.fill(10.0)

        C = A + B
        assert C.unit == m
        assert C[0, 0] == 1.1

        D = B + A
        assert D.unit == cm
        assert D[0, 0] == 110

    def test_add_incompat(self):
        with pytest.raises(OperationNotSupported):
            assert m1 + s1

    def test_sub(self):
        assert (s1 - s1).unit == s

        A = QArray((2, 2), unit=m)
        A.fill(1.0)
        B = QArray((2, 2), unit=cm)
        B.fill(10.0)

        C = A - B
        assert C.unit == m
        assert C[0, 0] == 0.9

        D = B - A
        assert D.unit == cm
        assert D[0, 0] == -90

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
        A = QArray.from_input([0, 1, 2], unit=m)
        B = QArray.from_input([0, 100, 2], unit=cm)
        with pytest.raises(OperationNotSupported):
            m1 < s1

        assert array_equal(A < B, QArray.from_input([0, 0, 0]))

    def test_gt(self):
        A = QArray.from_input([0, 1, 2], unit=m)
        B = QArray.from_input([0, 100, 2], unit=cm)
        with pytest.raises(OperationNotSupported):
            m1 > s1

        assert array_equal(A > B, QArray.from_input([0, 0, 1]))

    def test_le(self):
        A = QArray.from_input([0, 1, 2], unit=m)
        B = QArray.from_input([0, 100, 2], unit=cm)
        with pytest.raises(OperationNotSupported):
            m1 <= s1

        assert array_equal(A <= B, QArray.from_input([1, 1, 0]))

    def test_ge(self):
        A = QArray.from_input([0, 1, 2], unit=m)
        B = QArray.from_input([0, 100, 2], unit=cm)
        with pytest.raises(OperationNotSupported):
            m1 >= s1

        assert array_equal(A >= B, QArray.from_input([1, 1, 1]))
