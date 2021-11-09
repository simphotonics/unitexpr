import pytest

from unitexpr.unit_dict import *


d = {'zero': 0, 'one': 1, 'two': 2}
u = UnitDict(d)
v = ImmutableUnitDict(d)


class TestUnitDict:

    def test_empty(self):
        assert {} == UnitDict()

    def test_mul(self):
        assert u*2 == {'zero': 0, 'one': 2, 'two': 4}

    def test_rmul(self):
        assert 2*u == {'zero': 0, 'one': 2, 'two': 4}

    def test_add(self):
        assert u + u == {'one': 2, 'two': 4}

    def test_sub(self):
        assert u - u == {}

    def test_get_item(self):
        assert u['one'] == 1

    def test_neg(self):
        assert -u == {'zero': 0, 'one': -1, 'two': -2}

    def test_filter_value(self):
        assert u.filter_value(2) == {'zero': 0, 'one': 1}


class TestImmutableUnitDict:

    def test_empty(self):
        assert {} == ImmutableUnitDict()

    def test_mul(self):
        assert v*2 == {'zero': 0, 'one': 2, 'two': 4}

    def test_rmul(self):
        assert 2*v == {'zero': 0, 'one': 2, 'two': 4}

    def test_add(self):
        assert v + v == {'one': 2, 'two': 4}

    def test_sub(self):
        assert v - v == {}

    def test_get_item(self):
        assert v['one'] == 1

    def test_neg(self):
        assert -v == {'zero': 0, 'one': -1, 'two': -2}

    def test_filter_value(self):
        assert v.filter_value(2) == {'zero': 0, 'one': 1}

    def test_setitem(self):
        with pytest.raises(TypeError):
            v['one'] = 1.0

    def test_delitem(self):
        with pytest.raises(TypeError):
            del v['one']

    def test_clear(self):
        with pytest.raises(TypeError):
            v.clear()

    def test_update(self):
        with pytest.raises(TypeError):
            v.update(d)

    def test_update(self):
        with pytest.raises(TypeError):
            v.setdefault('one', 1.0)

    def test_pop(self):
        with pytest.raises(TypeError):
            v.pop()

    def test_popitem(self):
        with pytest.raises(TypeError):
            v.popitem()
