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

The sections below demonstrate how to sub-class [`UnitBase`][UnitBase]
to define unit systems and united numpy arrays.

### 1. Defining Base Units

In order to define a unit system, one must first specify the
base units. In the context of this package this is done using
the immutable class [`UnitSymbol`][UnitSymbol] which has
the following instance attributes: `symbol`, `name`, and `quantity`.
``` Python
from unitexpr import UnitSymbol

# Defining unit symbols
unit_symbols = (
            UnitSymbol(symbol='m','name'='meter',quantity='length'),
            UnitSymbol(symbol='s','name'='second',quantity='time'),
            UnitSymbol(symbol='kg','name'='kilogram',quantity='weight')
        )
```
Note: The attribute `symbol` must be a valid Python identifier.

### 2. Defining a Unit System

A custom unit system can be defined by sub-classing [`UnitBase`][UnitBase]
and specifying the meta-class [`UnitMeta`][UnitMeta], and the
custom base unit symbols in the class constructor.

```Python
from unitexpr import UnitBase, UnitMeta

# Defining a unit system using the base unit symbols specified above.
# Note the use of the metaclass `UnitMeta`.
class MetricUnit(UnitBase, metaclass=UnitMeta, unit_symbols=unit_symbols):
    pass

# Base units are available as class attributes.
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
- division: `W = SiUnit('W', 'watt', 'power', expr=J/s)`
- scalar multiplication: `c = MetricUnit('c', 'speed of light', 'velocity', expr=299792458*m/s)`
- exponentiation: `N = MetricUnit('N', 'newton', 'force', expr=kg*m*s**-2)`.

It is advisable to choose the unit variable name as the unit symbol. For example,
the constant `c` (defined above) represents
the speed of light and its unit symbol was set to 'c'.

Note: Units and unit expressions extend Python's `namedtuple` and as such are immutable.

### 3. Unit Expressions

Unit expressions are objects with base class `UnitExprBase`.
Each unit system defines a unique unit expression type
that is available as a class attribute
(`.expr_type`). Valid unit expression terms for a given unit system are:
base units, derived units, unit expressions, and numbers of type float and int.

``` python
# Accessing the unit expression type of the units system defined above:
MetricUnitExpr = MetricUnit.expr_type
assert type(m/s) == MetricUnitExpr

# Examples of unit expressions:
v = 10.0*m/s
w = v + 20.0*v
```

When adding or subtracting units and unit expression the term on the left
side determines the form of the expression. This is best shown in the example
below.
``` python

# Define units:
c_light = MetricUnit('c_light', 'speed of light', 'velocity', expr=299792458*m/s)
c_sound = MetricUnit('c_sound', 'speed of sound', 'velocity', expr=343*m/s)

v1 = c_light + c_sound
v2 = c_sound + c_light

assert v1 == v2

print(v1) # Prints:  1.0000011441248464*c_light
print(v2) # Prints:  874031.4897959183*c_sound
```


### 4. Quantity Arrays

To support scientific calculation
the package includes [`QArray`][QArray]
an extension of numpy's `ndarray`.

The entries of a [`QArray`][QArray] represent
physical *quantities* that can be expressed in terms of a
number and a unit.  The constructor of [`QArray`][QArray]
accepts the same parameters as the constructor of `ndarray` with
the additional optional parameter `unit` (default value 1.0).

To construct a [`QArray`][QArray] from an existing array or
a sequence of entries use the class method `QArray.from_input`.


```Python
from math import pi

from unitexpr.qarray import QArray
from unitexpr.si_units import m, s, h_bar, m_e, c, SiUnit


q = QArray(shape=(2, 2))
q.fill(10.0)
print("q = ")
print(q)
print()

a = q*m
print("a = q*m = ")
print(a)
print()

b = QArray.from_input(q, unit=s)
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

To retain a numerical factor, for example `pi` as term of the
unit expression it must be decared as a unit (see the example
above).

Note: Units and unit expressions with zero magnitude
may `not` be used with united arrays.
The instance attribute `unit` is a `@property`. In its set method the
array is multiplied with the unit expression `factor` and for consistency the
unit is divided by the same factor. For units with zero magnitude this
raises an exception of type `DivisionByZeroError`.

### 5. Scalar Quantities

The class [`Quantity`][Quantity] represents a `scalar` quantity that
can be expressed using a single numerical value and a unit.

It is equivalent to a [`QArray`][QArray] with `shape: (1, )` but its
constructor is more concise and includes the additional parameter
`info` which can be used to store object documentation.

``` Python

from unitexpr import Quantity
from unitexpr.sc_units import ps, nm

dt = Quantity(5.0, unit=ps, info='Time-integration step size.')
cavity_length = Quantity(1.25e6, unit =nm, info='Optical cavity length.')

# Accessing the quantity value:
print(dt.value)  # Prints: 5.0

print(dt.item()) # Prints: 5.0

print(dt[0])     # Prints: 5.0
```

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

[QArray]: http://unitexpr.simphotonics.com/reference/unitexpr/qarray/#QArray

[Quantity]: http://unitexpr.simphotonics.com/reference/unitexpr/quantity/#Quantity