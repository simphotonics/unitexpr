import pytest
from numpy import array_equal
from unitexpr import qarray, Quantity
from unitexpr.errors import OperationNotSupported
from unitexpr.si_units import SiUnit, m, s

cm = SiUnit("cm", "centimeter", "length", expr=1e-2 * m)

a = Quantity(10)

m1 = Quantity(20, unit=m, info="Court yard length.")
s1 = Quantity(30, unit=s)

Q = qarray.from_input([1.0, 1.0], m)


class TestQuantity:
    def test_default(self):
        assert a.unit == 1.0
        assert a.unit == m.expr_type.one

    def test_info(self):
        assert m1.info == "Court yard length."

    def test_value(self):
        assert m1.value == 20
        assert s1.value == 30

    def test_str(self):
        assert m1.__str__() == "20 * m"
        assert Quantity(20.0, unit=SiUnit.expr_type.one).__str__() == "20.0"

    def test_repr(self):
        assert (
            m1.__repr__() == "Quantity(20, unit=m, info='Court yard length.')"
        )
        assert Quantity(1.0, unit=1.0).__repr__() == "Quantity(1.0, unit=1.0)"

    def test_mul(self):
        assert (m1 * s1).unit == m * s
        assert (m1 * s).unit == m * s

    def test_mul_unit(self):
        assert (m1 * s).unit == m * s
        assert (m1 * 10.0 / s) == Quantity(200.0, m / s)

    def test_rmul(self):
        assert (3.0 * m1).unit == m
        assert 3.0 * m1 == Quantity(60.0, m)

    def test_rmul_unit(self):
        assert (m * s1).unit == m * s
        assert m * s1 == Quantity(30.0, m * s)

    def test_add(self):
        unit = getattr(m1 + m1, "unit", "Hello ->")

        assert unit == m
        A = Quantity(1.0, unit=m)
        B = Quantity(10, unit=cm)
        C = A + B
        assert C.unit == m
        assert C.value == 1.1

        D = B + A
        assert D.unit == cm
        assert D.value == 110

    def test_add_unit(self):
        assert m1 + 35.0 * m == Quantity(m1.value + 35.0, m)

    def test_add_incompat(self):
        with pytest.raises(OperationNotSupported):
            assert m1 + s1

    def test_sub(self):
        assert (s1 - s1).unit == s
        A = Quantity(1.0, unit=m)
        B = Quantity(10, unit=cm)
        C = A - B
        assert C.unit == m
        assert C.value == 0.9

        D = B - A
        assert D.unit == cm
        assert D.value == -90

    def test_sub_unit(self):
        assert m1 - 35.0 * m == Quantity(m1.value - 35.0, m)

    def test_sub_incompat(self):
        with pytest.raises(OperationNotSupported):
            assert m1 - s1

    def test_truediv(self):
        assert (m1 / s).unit == m / s
        assert m1 / s1 == Quantity(m1.value / s1.value, m1.unit / s1.unit)

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
        assert B < A

        assert A < 1.1 * m

    def test_gt(self):
        with pytest.raises(OperationNotSupported):
            m1 > s1
        A = Quantity(1.0, unit=m)
        B = Quantity(10, unit=cm)
        assert A > B

        assert A > 0.8 * m

    def test_le(self):
        with pytest.raises(OperationNotSupported):
            m1 <= s1
        A = Quantity(1.0, unit=m)
        B = Quantity(10, unit=cm)
        assert B < A

        assert A <= 1.0 * m

    def test_ge(self):
        with pytest.raises(OperationNotSupported):
            m1 >= s1
        A = Quantity(1.0, unit=m)
        B = Quantity(10, unit=cm)
        assert A >= B

        assert A >= 100 * cm


class TestArrayOperators:
    def test_mul(self):
        result = Q * m1
        assert result.unit == m ** 2
        assert array_equal(result, [20.0, 20.0])

    def test_rmul(self):
        result = s1 * Q
        assert result.unit == s * m
        assert array_equal(result, [30.0, 30.0])

    def test_div(self):
        result = Q / s1
        assert result.unit == m / s
        assert array_equal(result, [1.0 / 30, 1.0 / 30])

    def test_rdiv(self):
        result = s1 / Q
        assert result.unit == s / m
        assert array_equal(result, [30.0, 30.0])
