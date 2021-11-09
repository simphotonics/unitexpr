from unitexpr.unit_symbol import *
from unitexpr.unit import UnitBase, UnitMeta


unit_symbols = (
    UnitSymbol('m', 'meter', 'length'),
    UnitSymbol('s', 'second', 'time'),
    UnitSymbol('kg', 'kilogram', 'mass')
)


class SiUnit(UnitBase, metaclass=UnitMeta, unit_symbols=unit_symbols):
    pass


SiUnitExpr = SiUnit.expr_type

kg = SiUnit.kg
m = SiUnit.m
s = SiUnit.s

N = SiUnit('N', 'Newton', 'force', expr=kg*m/(s*s))

v = SiUnit('v', 'meter/second', 'speed', expr=73*m/s*kg/kg*s**-10)

print(v.info)
print(v.sub_expr)
print(v.sub_terms)
print(v.terms)

exit()

joule = SiUnit('J', 'Joule', 'energy', expr=N*m)
watt = SiUnit('W', 'Watt', 'power', expr=joule/s)
pm = SiUnit('pm', 'picometer', 'length', expr=m*1e-12)
c = SiUnit('c', name='speed of light', quantity='speed',
           expr=3*10**8*m/s)


half = (N*N/N/N*watt*s)

print(half)

v_expr = v*1.0

one = (m/s/v)

print('>>>>>>>>')
print('one: {}'.format(one))
print('one.base_exponents: {}'.format(one.base_exponents))
print('one.base_factor: {}'.format(one.base_factor))
print('one.factor: {}'.format(one.factor))
print('one.__repr__(): {}'.format(one.__repr__()))

print(one == 1.0)

print(type(one))
print(one != one)

exit()

# print(half.base_exponents)

# print(half.factor)
# print(half.__repr__())

print(half.__repr__())


exit()

print('m:')
print(m)
print(m.exponents)
print(m.base_exponents)
print(m.dexpr)
print(m.terms)

print('')
print('Newton')

print(N)
print(N.exponents)
print(N.expr)
print(N.dexpr)


print('')
print('Joule')

print(joule)
print(joule.exponents)
print(joule.base_exponents)
print(joule.dexpr)

exit()
print(((1*s)/(s*1)))
print(m/m)
print(N*joule)
print(joule)
print(joule.terms)

print(watt)
print((watt/joule))

print(pm)

print(2.0*watt)

print('Printing s')
print(s)

print('Printing c:')
print(c)
print(c.factor)
