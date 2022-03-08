from unitexpr import quantity
from unitexpr.si_units import m, s, c, SiUnit

cm = SiUnit("cm", "centimeter", "length", m / 100.0)
q = quantity(2.0, m)
p = quantity(2.0, cm)

print(f"q = {q}")
print('')

a = q * m
print(f"a = q*m = {a}")
print()

b = quantity(2.0, unit=s)

print(f"b = {b}")
print()

print(f"a / b = {a/b}")
print()

print(f"(a / b)**2 = {(a/b)**2}")
print()

m1 = quantity(20, unit=m, info="Court yard length.")


m2 = m1 * m1

print(m2.__repr__())

print(q + p)


v = quantity(c.base_factor, m / s, "speed")
print(v)

v1 = v + c.base_expr

print(v1.__repr__())
