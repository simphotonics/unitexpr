from unitexpr import UnitSymbol, UnitBase, UnitMeta
from unitexpr.si_units import c, h_bar, m_e

# Defining base unit symbols.
unit_symbols = (
    UnitSymbol("m", "meter", "length"),
    UnitSymbol("s", "second", "time"),
    UnitSymbol("kg", "kilogram", "mass"),
)

# Defining a unit system.
class MetricUnit(UnitBase, metaclass=UnitMeta, unit_symbols=unit_symbols):
    pass


# Accessing the unit expression type.
SiUnitExpr = MetricUnit.expr_type

# Accessing base units (and declaring shortcuts for them).
kg = MetricUnit.kg
m = MetricUnit.m
s = MetricUnit.s

# Defining a derived unit.
N = MetricUnit("N", "Newton", "force", expr=kg * m / (s * s))

# Prints an object of type UnitInfo:
print("UnitInfo object for N (Newton):")
print(N.info)
print()

# Prints the derived unit in terms of its sub-terms.
print("Newton in terms of base units:")
print(N.expr)
print()

# Prints an expression of SI units and the same expression in
# terms of SI base units:
print("SI unit expression:")
print(f"m_e*c/h_bar = {m_e*c/h_bar} = {(m_e*c/h_bar).base_repr}")
print()
