"""
Units, unit expressions and united numpy arrays.

The package `unitexpr` provides the modules:

- unit: Module containing the base classes `UnitBase` and `UnitMeta`.
- unit_symbol: Provides the class `UnitSymbol` used to specify
  base unit symbols.
- qarray: A sub-class of a `numpy` n-dimensional array whose entries
  represent a quantity with an associated unit.
- si_units: Predefined units representing the SI Unit System.
- sc_units: Predefined units based on (nm, ps, m_e, K, cd, ). Semiconductor
            Units.


"""

from .unit import UnitBase, UnitMeta
from .unit_symbol import UnitSymbol
from .qarray import qarray
from .quantity import quantity
