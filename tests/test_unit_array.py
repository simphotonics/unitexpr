import pytest

from unitexpr.si_units import m, s
from unitexpr.unit_array import UnitArray
from unitexpr.errors import OperationNotSupported

a = UnitArray(shape=(2, 2))
a.fill(10.0)

m1 = UnitArray(shape=(2, 2), unit=m)
m1.fill(20.0)

s1 = UnitArray(shape=(2, 2), unit=s)
s1.fill(30.0)


class TestUnitArray:

    def test_default(self):
        assert a.unit == 1.0
        assert a.unit == m.expr_type.one

    def test_mul(self):
        assert (m1*s1).unit == m*s

    def test_mul_unit(self):
        assert(m1*s).unit == m*s

    def test_rmul(self):
        assert (3.0*m1).unit == m

    def test_rmul_unit(self):
        assert(m*s1).unit == m*s

    def test_add(self):
        assert (m1 + m1).unit == m

    def test_add_incompat(self):
        with pytest.raises(OperationNotSupported):
            assert m1 + s1

    def test_sub(self):
        assert(s1 - s1).unit == s

    def test_sub_incompat(self):
        with pytest.raises(OperationNotSupported):
            assert m1 - s1

    def test_truediv(self):
        assert (m1/s).unit == m/s

    def test_pow(self):
        assert(s1**2).unit == s**2

    def test_abs(self):
        assert(abs(s1).unit) == s

    def test_neg(self):
        assert(-s1).unit == s

    def test_pos(self):
        assert(+s1).unit == s
