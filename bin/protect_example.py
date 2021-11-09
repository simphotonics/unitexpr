from typing import Any, Type
import re

from unitexpr.decorators import protect


# class UnitSymbolMeta(type):
#     '''
#     Meta class used to freeze the class attribute `reg_expr`.
#     ```
#     '''

#     def __setattr__(self, name: str, value: Any) -> None:
#         if name == 'reg_expr':
#             raise AttributeError(
#                 'Attribute <{}> is protected and could not be set.'.format(
#                     value))
#         return super().__setattr__(name, value)


class UnitSymbol():

    # __slots__ = ('symbol', 'name', 'quantity')
    reg_expr = '^[A-Za-z_][A-Za-z0-9_]*'

    @protect()
    def __setattr__(self, name: str, value: Any) -> None:
        return super().__setattr__(name, value)

    def __init__(self, symbol: str, name: str, quantity: str):
        self.validate_symbol(symbol)
        self.symbol = symbol
        self.name = name
        # self.quantity = quantity

    @classmethod
    def validate_symbol(cls: Type['UnitSymbol'], value: str) -> bool:
        '''
        Returns `True` if `value` matches the regular expression:
        '^[A-Za-z_][A-Za-z0-9_]*'
        '''
        if not re.search(cls.reg_expr, value):
            raise ValueError('Invalid symbol found: {}.'.format(
                value.__repr__()))

    def __str__(self):
        return self.symbol

    def __repr__(self):
        return '{}(symbol={}, name={}, quantity={})'.format(
            self.__class__.__name__,
            self.symbol.__repr__(),
            self.name.__repr__(),
            self.quantity.__repr__()
        )


u = UnitSymbol('s', 'second', 'time')
print(u.__dict__)
print(u)

u.name = 'one'
