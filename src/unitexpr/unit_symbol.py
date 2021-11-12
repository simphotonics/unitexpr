"""
Provides `UnitSymbol` an immutable class representing base unit symbols.
"""

from typing import NamedTuple
import re


class UnitSymbol(
    NamedTuple("_UnitSymbol", symbol=str, name=str, quantity=str),
):
    """
    Immutable class inheriting from `NamedTuple` representing a
    base unit symbol with fields:
    * symbol: The symbol displayed in unit expressions. Should be a valid
      Python identifier.
    * name: The unit name.
    * quantity: The physical quantity represented by the unit.

    ``` python
    m = UnitSymbol('m', 'meter', 'length')
    s = UnitSymbol(symbol='s', name='second', quantity='time')
    ```
    """

    __slots__ = ()
    __reg_expr = "^[A-Za-z_][A-Za-z0-9_]*"

    def __new__(cls, symbol: str, name: str, quantity: str):
        if not UnitSymbol.is_valid_symbol(symbol):
            raise ValueError(
                f"Symbol {type(symbol)}:{symbol} is not a valid identifier."
            )

        return super().__new__(cls, symbol, name, quantity)

    @classmethod
    def is_valid_symbol(cls, value: str) -> bool:
        """
        Returns `True` if `value` matches the regular expression:
        '^[A-Za-z_][A-Za-z0-9_]*'
        """
        if not isinstance(value, str):
            return False

        if re.fullmatch(UnitSymbol.__reg_expr, value) is None:
            return False

        return True
