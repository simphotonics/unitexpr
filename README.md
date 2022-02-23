# Unit Expressions For Python
[![tests](https://github.com/simphotonics/unitexpr/actions/workflows/test.yml/badge.svg)](https://github.com/simphotonics/unitexpr/actions/workflows/test.yml)
[![docs](https://raw.githubusercontent.com/simphotonics/unitexpr/main/images/docs-badge.svg)](https://unitexpr.simphotonics.com)

Attaching units to numerical quantities is a convenient way to check if
an expression is valid or an equation is consistent.
For example, it makes little sense to add a quantity
representing weight and one representing distance, or to
add seconds and pico-seconds.


The package [`unitexpr`][unitexpr] provides classes and meta-classes that
make it trivial to define custom unit systems and [`numpy`][numpy] arrays
with support for physical units.

A search on [pypi][pypi] shows that there are a few packages available
for doing unit analysis. The most notable I found is [`scimath`][scimath],
which supports unit conversion and working with united numpy arrays.
For the purpose of optimization [`scimath`][scimath] computes and stores unit
expressions in terms of base units.

The package [`unitexpr`][unitexpr] stores unit expressions in terms of
base units *and* derived units. The advantage is that unit expressions
retain their form. The cost (in terms of computational time) of keeping
track of derived unit terms is of the order of few microsecond, depending
on the complexity of the unit expression. For more details see
[benchmarks][benchmarks].

For example, the constant `m_e*c/h_bar` (where `m_e` is
the electron mass, `c` is the velocity of light, `h_bar` is the
reduced Planck constant) is displayed as `m_e*c*h_bar**-1.0`. In
terms of SI base units the same constant is given by
the less obvious expression: `2589605074819.227*m**-1.0`.



## Installation

To install the package [`unitexpr`][unitexpr] use the command:
```Console
$ pip install unitexpr
```

## Usage

The following sections demonstrate how to create
[unit expressions](#1-unit-expressions) ,
work with [quantity arrays](#2-quantity-arrays),
define [scalar quantities](#3-scalar-quantities),
and construct [custom unit systems](#custom-unit-systems).


### 1. Unit Expressions

Unit expressions are objects with base class `UnitExprBase`.
Each unit system defines a *unique* unit expression type
that is available as a class attribute
(`.expr_type`). Valid unit expression *terms* for a given unit system are:
*base units*, *derived units*, *unit expressions*, and *real numbers*.

The package includes two predefined unit systems with a comprehensive list of
derived units and physical constants:

* `unitexpr.si_units`: SI Units based on meter, second, kilogram,
Ampere, Kelvin, mol, and candela,
* `unitexpr.sc_units`: Semiconductor Units based on nanometer, picosecond,
electron mass, Ampere, Kelvin, mol, and candela.

``` python
from unitexpr.si_units import m, s, c, SiUnit

# Accessing the unit expression type of the units system:
SiUnitExpr = SiUnit.expr_type
assert type(m/s) == SiUnitExpr

# Examples of unit expressions:
v = 10.0*m/s
w = v + 20.0*v

# When adding or subtracting units and unit expression the term on the left
# side determines the form of the expression. This is best shown in the example
# below.
#
# Note: c is defined as:
# c = SiUnit('c', 'speed of light', 'velocity', expr=299792458*m/s)

# Defining a derived unit:
c_sound = SiUnit('c_sound', 'speed of sound', 'velocity', expr=343*m/s)

v1 = c + c_sound
v2 = c_sound + c

assert v1 == v2

print(v1) # Prints:  1.0000011441248464*c
print(v2) # Prints:  874031.4897959183*c_sound
```

Tip: The methods `proportional_to`
and `scaling_factor` can be used to
determined if a unit or unit expression is a scaled
version of another unit or unit expression:

```Python

from unitexpr.si_units import m, s, SiUnit

# Define a derived unit
cm = SiUnit('cm', name='centimeter', quantity='length', expr=m/100.0)

# Check if units are proportional
assert cm.proportional_to(m) == True
assert cm.proportional_to(s) == False

# Get the scaling factor that converts cm to m.
assert cm.scaling_factor(m) == 100.0

# Get the scaling factor that converts m to cm.
assert m.scaling_factor(cm) == 0.01

# Get the scaling factor that converts m to s.
assert m.scaling_factor(s) == None
```

### 2. Quantity Arrays

To support scientific calculation
the package includes [`qarray`][qarray]
an extension of numpy's `ndarray`.

The entries of a [`qarray`][qarray] represent
the value of a physical *quantity*
that can be expressed in terms of a
numerical value and a unit.  The constructor of [`qarray`][qarray]
accepts the same parameters as the constructor of `ndarray` with
the additional optional parameters `unit` (default value 1.0).
and `info` which can be used to store object documentation.

To construct a [`qarray`][qarray] from an existing array or
a sequence of entries use the class method `qarray.from_input`.

```Python
from math import pi

from unitexpr import qarray
from unitexpr.si_units import m, s, h_bar, m_e, c, SiUnit


q = qarray(shape=(2, 2))
q.fill(10.0)
print("q = ")
print(q)
print()

a = q*m
print("a = q*m = ")
print(a)
print()

b = qarray.from_input(q, unit=s)
b.fill(2.0)

print("b =")
print(b)
print()

print("a / b =")
print(a/b)
print()

print("(a / b)**2 =")
print((a/b) ** 2)
print()

Pi = SiUnit("Pi", "Pi", "circle constant", pi * SiUnit.expr_type.one)

print("Pi*a*9.81*m/s**2 =")
print(Pi * a * 9.81 * m / s ** 2)
```
Running the script above produces the following output:
<details> <summary> Click to show the console output. </summary>

``` Console
(unitexpr) $ python example/qarray_example.py
q =
[[10. 10.]
 [10. 10.]] unit: 1.0

a = q*m =
[[10. 10.]
 [10. 10.]] unit: m

b =
[[2. 2.]
 [2. 2.]] unit: s

a / b =
[[5. 5.]
 [5. 5.]] unit: m*s**-1.0

(a / b)**2 =
[[25. 25.]
 [25. 25.]] unit: m**2.0*s**-2.0

Pi*a*9.81*m/s**2 =
[[98.1 98.1]
 [98.1 98.1]] unit: Pi*m**2.0*s**-2.0
```
</details>


Tip: United arrays can be multiplied with unit expressions.
Any numerical factor will be multiplied with the array using scalar
multiplication. The remaining part of the unit expression will be
multiplied with the unit attribute of the array.

United array can be added to unit expressions as long as the
base units match.

To retain a numerical factor, for example `pi` as term of the
unit expression it must be declared as a unit (see the example
above).

Note: Units and unit expressions with zero magnitude
may `not` be assigned as the unit attribute of qarrays (
normalization will fail with a `DivisionByZero` error).


### 3. Scalar Quantities

The class [`Quantity`][Quantity] represents a `scalar` quantity that
can be expressed using a single numerical value and a unit.
It is a subclass of `qarray`
and has shape (1, 0).

Objects of type [`Quantity`][Quantity] can be used to store
physical parameters:

``` Python
from unitexpr import Quantity
from unitexpr.sc_units import ps, nm

dt = Quantity(5.0, unit=ps, info='Time-integration step size.')
cavity_length = Quantity(1.25e6, unit=nm, info='Optical cavity length.')

# Accessing the quantity value:
print(dt.value)      # Prints: 5.0

print(dt)            # Prints: 5.0 ps
print(dt.__repr__()) # Quantity(5.0, unit=ps, info='Time-integration step size.')

# Quantity expressions:
print(dt*cavity_length) # Prints: 6250000.0 ps*nm


```
The class [`Quantity`][Quantity] implements the numerical operators:
`+, -, *, **, \, abs, neg, pos, <, <=, >, >=`.

Tip: Objects of type [`Quantity`][Quantity] support division and multiplication with
`qarrays`. Quantities can be used together with (compatible) units to form
mathematical expressions.



## Custom Unit Systems

Defining custom unit systems using the package [`unitexpr`][unitexpr]
is a simple task consisting of two steps:
defining [base unit symbols](#1-defining-base-unit-symbols) and
defining the [unit system](#2-defining-a-unit-system)
by sub-classing [`UnitBase`][UnitBase].

### 1. Defining Base Unit Symbols

In order to define a unit system, one must first specify the
base unit symbols. In the context of this package this is done
by constructing a tuple with entries of type
[`UnitSymbol`][UnitSymbol] (an immutable class with
instance attributes: `symbol`, `name`, and `quantity`):

``` Python
from unitexpr import UnitSymbol

# Defining unit symbols
unit_symbols = (
            UnitSymbol(symbol='m',name='meter',quantity='length'),
            UnitSymbol(symbol='s',name='second',quantity='time'),
            UnitSymbol(symbol='kg',name='kilogram',quantity='weight')
        )
```
Note: The attribute `symbol` must be a valid Python identifier.

### 2. Defining a Unit System

A custom unit system can be defined by sub-classing [`UnitBase`][UnitBase]
specifying the meta-class [`UnitMeta`][UnitMeta] and the
custom base unit symbols as class constructor parameters:

```Python
from unitexpr import UnitBase, UnitMeta

# Defining a unit system using the base unit symbols specified above.
# Note the use of the metaclass `UnitMeta`.
class MetricUnit(UnitBase, metaclass=UnitMeta, unit_symbols=unit_symbols):
    pass

# Base units are now available as class attributes.
# For example:
m = MetricUnit.m
s = MetricUnit.s
kg = MetricUnit.kg

assert type(m) == MetricUnit

# Declaring derived units
c = MetricUnit('c', 'speed of light', 'velocity', expr=299792458*m/s)
```
The base units are constructed during the instantiation of the meta-class
and are available as class attributes. In the example above the
base units are `m`, `s`, and `kg`.

Derived units and unit expressions can be constructed using the operations:
- multiplication: `J = MetricUnit('J', 'joule', 'energy', expr=N*m)`
- division: `W = MetricUnit('W', 'watt', 'power', expr=J/s)`
- scalar multiplication: `c = MetricUnit('c', 'speed of light', 'velocity', expr=299792458*m/s)`
- exponentiation: `N = MetricUnit('N', 'newton', 'force', expr=kg*m*s**-2)`.

It is advisable to choose the unit variable name as the unit symbol. For example,
the constant `c` (defined above) represents
the speed of light and its unit symbol was set to 'c'.

Note: Units and unit expressions extend Python's `namedtuple` and as such are immutable.

## Features and bugs

Please file feature requests and bugs at the [issue tracker].
Contributions are welcome.

[issue tracker]: https://github.com/simphotonics/unitexpr/issues

[benchmarks]: benchmarks

[numpy]: https://pypi.org/project/numpy/

[pypi]: https://pypi.org

[pytest]: https://pypi.org/project/pytest/

[scimath]: https://pypi.org/project/scimath

[unitexpr]: https://github.com/simphotonics/unitexpr

[UnitSymbol]: http://unitexpr.simphotonics.com/reference/unitexpr/unit_symbol/#UnitSymbol

[UnitBase]: http://unitexpr.simphotonics.com/reference/unitexpr/unit/#UnitBase

[UnitMeta]: http://unitexpr.simphotonics.com/reference/unitexpr/unit/#UnitMeta

[qarray]: http://unitexpr.simphotonics.com/reference/unitexpr/qarray/#qarray

[Quantity]: http://unitexpr.simphotonics.com/reference/unitexpr/quantity/#Quantity