from math import pi

from unitexpr.unit_array import UnitArray
from unitexpr.si_units import m, s, h_bar, m_e, c, SiUnit


a = UnitArray(shape=(2, 2), unit=m)
a.fill(10.0)

print('a = \n {} \n'.format(a))

b = UnitArray(shape=(2, 2), unit=s)
b.fill(2.0)

print('b = \n {} \n'.format(b))

d = a / b

print('a / b = \n {} \n'.format(d))

print('(a / b)**2 = \n {} \n'.format(d**2))

Pi = SiUnit('Pi', 'Pi', 'number', pi*SiUnit.expr_type.one)

print('m_e*c/h_bar = {} = {}\n'.format(m_e*c/h_bar, (m_e*c/h_bar).base_repr()))

print('Pi*a*9.81*m/s**2 = \n {} \n '.format(Pi*a*9.81*m/s**2))
