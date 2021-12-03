from unitexpr import Quantity
from unitexpr.si_units import m, s

q = Quantity(2.0, m)
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
