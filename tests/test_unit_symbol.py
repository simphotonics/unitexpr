import pytest

from unitexpr.unit_symbol import UnitSymbol

# Symbols
m = UnitSymbol('m', 'meter', 'length',)
s = UnitSymbol('s', 'second', 'time',)
kg = UnitSymbol('kg', 'kilogram', 'mass',)


class TestUnitSymbol:
    def test_symbol(self):
        assert m.symbol == 'm'

    def test_error(self):
        with pytest.raises(ValueError):
            non_symbol = UnitSymbol('1m', '', '')
