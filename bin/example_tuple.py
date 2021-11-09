from unitexpr.unit_symbol import *
from unitexpr.unit import Unit


unit_symbols = (
    UnitSymbol('m', 'meter', 'length'),
    UnitSymbol('s', 'second', 'time'),
    UnitSymbol('kg', 'kilogram', 'mass')
)


class SiUnit(Unit, unit_symbols=unit_symbols):
    pass


SiUnitExpr = SiUnit.expr_type

kg = SiUnit.kg
m = SiUnit.m
s = SiUnit.s

SiUnit.hello = 'kg'

v = SiUnit('v', 'meter/second', 'speed', expr=10*m/s)


print('{} {} {}'.format(v.base_exponents, (v*1).base_exponents,
                        (1*v).base_exponents))

print('{} {} {}'.format(v.base_factor, (v*1).base_factor,
                        (1*v).base_factor))


v_expr = 10*(1.0*v)


w_expr = SiUnitExpr({v: 1}, 10.0)

print(w_expr.__repr__())
print(v_expr.__repr__())

print(w_expr == v_expr)


# w = SiUnit('w', 'meter/second', 'speed', expr = 1.0*v)
# print(w.base_expr)


N = SiUnit('N', 'Newton', 'force', expr=kg*m*s**-2)
joule = SiUnit('J', 'Joule', 'energy', expr=N*m)
watt = SiUnit('W', 'Watt', 'power', expr=joule/s)
pm = SiUnit('pm', 'picometer', 'length', expr=m*1e-12)
c = SiUnit('c', name='speed of light', quantity='speed', expr=2.99e8*m/s)


half = (N*N/N/N*watt*s)
