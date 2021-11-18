"""
Si Unit System based on meter, second, kilogram, Ampere, Kelvin, mole, candela.
"""

from math import pi

from .unit import UnitBase, UnitMeta
from .unit_symbol import UnitSymbol

unit_symbols = (
    UnitSymbol("m", "meter", "length"),
    UnitSymbol("s", "second", "time"),
    UnitSymbol("kg", "kilogram", "mass"),
    UnitSymbol("A", "ampere", "electric current"),
    UnitSymbol("K", "kelvin", "temperature"),
    UnitSymbol("mol", "mole", "amount of substance"),
    UnitSymbol("cd", "candela", "luminous intensity"),
)


class SiUnit(UnitBase, metaclass=UnitMeta, unit_symbols=unit_symbols):
    """
    Class representing SI unitexpr. The fundamental units are available as:
    `SiUnit.m`, `SiUnit.s`, `SiUnit.kg`, `SiUnit.A`, `SiUnit.K`, `SiUnit.mol`
    and `SiUnit.cd`.
    """

    __slots__ = ()


# Base units
m = SiUnit.m
"""
Base unit: Meter
"""
s = SiUnit.s
kg = SiUnit.kg
A = SiUnit.A
K = SiUnit.K
mol = SiUnit.mol
cd = SiUnit.cd


# Derived units
au = SiUnit("au", "astronomical unit", "length", expr=149597870700 * m)
sr = SiUnit("sr", "steradian", "solid angle", expr=SiUnit.expr_type.one)
N = SiUnit("N", "newton", "force", expr=kg * m * s ** -2)
J = SiUnit("J", "joule", "energy", expr=N * m)
eV = SiUnit("eV", "electronvolt", "energy", expr=1.602176634e-19 * J)
W = SiUnit("W", "watt", "power", expr=J / s)
C = SiUnit("C", "coulomb", "charge", expr=A * s)
V = SiUnit("V", "volt", "electric potential difference", expr=J / C)
F = SiUnit("F", "farad", "capacitance", expr=C / V)
ohm = SiUnit("ohm", "ohm", "resistance", expr=V / A)
Pa = SiUnit("Pa", "pascal", "pressure", expr=N * m ** -2)
S = SiUnit("S", "siemens", "electrical conductance", 1 / ohm)
Wb = SiUnit("Wb", "weber", "magnetic flux", expr=V * s)
T = SiUnit("T", "tesla", "magnetic flux density", expr=Wb * m ** -2)
H = SiUnit("H", "henry", "inductance", expr=Wb / A)
lm = SiUnit("lm", "lumen", "luminous flux", expr=cd / sr)
Bq = SiUnit("Bq", "bequerel", "radioactivity (decays per second)", expr=1 / s)
lx = SiUnit("lx", "lux", "illuminance", expr=lm * m ** -2)
Gy = SiUnit("Gy", "gray", "absorbed dose of ionizing radiation", expr=J / kg)

# Constants with exact value
delta_nu_Cs = SiUnit(
    "delta_nu_cs",
    "hyperfine transition of frequency of Cs",
    "frequency",
    expr=91926377 / s,
)

c = SiUnit("c", "speed of light", "velocity", expr=299792458 * m / s)
h = SiUnit("h", "Planck constant", "angular momentum", 6.62607015e-34 * J * s)
h_bar = SiUnit(
    "h_bar", "Reduced Planck constant", "angular momentum", h / (2 * pi)
)
e = SiUnit("e", "elementary charge", "charge", expr=1.606176634e-19 * C)
k = SiUnit(
    "k", "Boltzmann constant", "energy/Kelvin", expr=1.380649e-23 * J / K
)

m_e = SiUnit("m_e", "electron mass", "weigth", expr=9.1093837015e-31 * kg)

N_a = SiUnit(
    "N_a",
    "Avogadro constant",
    "number of molecules per mole",
    expr=6.02214076e-23 / mol,
)

K_cd = SiUnit(
    "K_cd",
    "luminous efficacy",
    "luminous efficacy of 540 THz radiation",
    expr=683 * lm / W,
)
