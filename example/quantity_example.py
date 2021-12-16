from unitexpr import Quantity
from unitexpr.si_units import m, s, c, SiUnit

cm = SiUnit("cm", "centimeter", "length", m / 100.0)
q = Quantity(2.0, m)
p = Quantity(2.0, cm)

print(f"q = {q}")
print()

a = q * m
print(f"a = q*m = {a}")
print()

b = Quantity(2.0, unit=s)

print(f"b = {b}")
print()

print(f"a / b = {a/b}")
print()

print(f"(a / b)**2 = {(a/b)**2}")
print()

m1 = Quantity(20, unit=m, info="Court yard length.")


m2 = m1 * m1

print(m2.__repr__())

print(q + p)


v = Quantity(c.base_factor, m/s, 'speed')
print(v)

v1 = v + c.base_expr

print(v1.__repr__())
