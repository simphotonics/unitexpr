from math import pi

from unitexpr.qarray import QArray
from unitexpr.si_units import m, s, h_bar, m_e, c, SiUnit


q = QArray(shape=(2, 2))
q.fill(10.0)
print("q = ")
print(q)
print()

a = q * m
print("a = q*m = ")
print(a)
print()

b = QArray(shape=(2, 2), unit=s)
b.fill(2.0)

print("b =")
print(b)
print()

print("a / b =")
print(a / b)
print()

print("(a / b)**2 =")
print((a / b) ** 2)
print()

Pi = SiUnit("Pi", "Pi", "number", pi * SiUnit.expr_type.one)

print("Pi*a*9.81*m/s**2 =")
print(Pi * a * 9.81 * m / s ** 2)
