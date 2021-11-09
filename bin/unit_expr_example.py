from unitexpr.si_units import *

SiUnitExpr = SiUnit.expr_type


print(SiUnitExpr.one)

v = SiUnit('v', 'meter/second', 'speed', expr=10.0*m/s)


v_expr = v*1.0

print(v_expr*m)

print(m*v_expr)

print(v_expr*m == m*v_expr == m*v == SiUnitExpr.from_dict({v: 1.0, m: 1.0}))


print(v/v_expr)

print(m == 1*m)

print(v.expr.repr())
print(v_expr.repr())
