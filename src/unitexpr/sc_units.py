'''
Semiconductor Unit System based on nanometer, picosecond, electron mass, Ampere,
Kelvin, mol, and candela.
'''

from .unit_symbol import UnitSymbol
from .unit import UnitBase

unit_symbols = (
    UnitSymbol('nm', 'nano-meter', 'length'),
    UnitSymbol('ps', 'pico-second', 'time'),
    UnitSymbol('m_e', 'electron rest mass', 'mass'),
    UnitSymbol('A', 'ampere', 'electric current'),
    UnitSymbol('K', 'kelvin', 'temperature'),
    UnitSymbol('mol', 'mole', 'amount of substance'),
    UnitSymbol('cd', 'candela', 'luminous intensity')
)


class ScUnit(UnitBase, unit_symbols=unit_symbols):
    '''
    Class representing Semiconductor unitexpr. The fundamental units are available as:
    `ScUnit.nm`, `ScUnit.ps`, `ScUnit.m_e`, `ScUnit.A`, `ScUnit.K`, `ScUnit.mol`
    and `ScUnit.cd`.
    '''


# Base units
nm = ScUnit.nm
ps = ScUnit.ps
m_e = ScUnit.m_e
A = ScUnit.A
K = ScUnit.K
mol = ScUnit.mol
cd = ScUnit.cd

# Derived units
# sr = ScUnit('sr', 'steradian', 'solid angle', expr=ScUnit.expr_type.one)
# eV = ScUnit('eV', 'electronvolt', 'energy', expr=1.602176634e-19*J)
# e = ScUnit('e', 'electron charge', 'charge', expr=A*s)
# V = ScUnit('V', 'volt', 'electric potential difference', expr=J/C)
# F = ScUnit('F', 'farad', 'capacitance', expr=C/V)
# ohm = ScUnit('ohm', 'ohm', 'resistance', expr=V/A)
# S = ScUnit('S', 'siemens', 'electrical conductance', 1/ohm)
# Wb = ScUnit('Wb', 'weber', 'magnetic flux', expr=V*s)
# T = ScUnit('T', 'tesla', 'magnetic flux density', expr=Wb*m**-2)
# H = ScUnit('H', 'henry', 'inductance', expr=Wb/A)
# lm = ScUnit('lm', 'lumen', 'luminous flux', expr=cd/sr)
# Bq = ScUnit('Bq', 'bequerel', 'radioactivity (decays per second)', expr=1.0e12/ps)
# lx = ScUnit('lx', 'lux', 'illuminance', expr=lm*m**-2)


# Constants with exact value
# delta_nu_Cs = ScUnit(
#     'delta_nu_cs', 'hyperfine transition of frequency of Cs', 'frequency',
#     expr=91926377*1.0e-12 / ps)

# c = ScUnit('c', 'speed of light', 'velocity', expr=299792458e3*nm/ps)
# h = ScUnit('h', 'Planck constant', 'angular momentum', 6.62607015e-34*J*s)
# h_bar = ScUnit('h_bar', 'Reduced Planck constant',
#                'angular momentum', h/(2*pi))
# e = ScUnit('e', 'elementary charge', 'charge', expr=1.606176634e-19*C)
# k = ScUnit('k', 'Boltzmann constant',
#            'energy/Kelvin', expr=1.380649e-23*J/K)

# m_e = ScUnit('m_e', 'electron mass', 'weigth', expr=9.1093837015e-31*kg)

# N_a = ScUnit('N_a', 'Avogadro constant', 'number of molecules per mole',
#              expr=6.02214076e-23/mol)

# K_cd = ScUnit('K_cd', 'luminous efficacy',
#               'luminous efficacy of 540 THz radiation', expr=683*lm/W)
