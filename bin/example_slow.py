from units_slow.unit_symbol import *
from units_slow.unit import Unit


unit_symbols = (
  UnitSymbol('m', 'meter', 'length'),
  UnitSymbol('s', 'second', 'time'),
  UnitSymbol('kg', 'kilogram', 'mass')
)

class SiUnit(Unit, unit_symbols = unit_symbols):
  pass

SiUnitExpr = SiUnit.expr_type

kg = SiUnit.kg
m = SiUnit.m
s = SiUnit.s



N = SiUnit('N', 'Newton', 'force',expr =kg*m/(s*s))
joule = SiUnit('J', 'Joule', 'energy',expr=N*m)
watt = SiUnit('W', 'Watt', 'power', expr=joule/s)
pm = SiUnit('pm', 'picometer', 'length', expr=m*1e-12)
c = SiUnit('c', name = 'speed of light', quantity='speed',
                expr=3*10**8*m/s)




# print(joule)
# print(joule.dexpr)
# print(joule.expr)
# print(joule.exponents)
# print(joule.base_expr)

half = (N*N/N/N*watt*s)

print(half)

v = SiUnit('v', 'meter/second', 'speed', expr=2.0*m/s)
v_expr = SiUnitExpr({v:1})

one = (v/m*s)

print('>>>>>>>>')
print('one: {}'.format(one))
print('one.base_exponents: {}'.format(one.base_exponents))
print('one.base_factor: {}'.format(one.base_factor))
print('one.factor: {}'.format(one.factor))
print('one.exponents: {}'.format(one.exponents))
print('one.terms: {}'.format(one.terms))
print('one.__repr__(): {}'.format(one.__repr__()))

print(one == 2.0)

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
