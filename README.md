# Unit Expressions For Python
[![Python](https://github.com/simphotonics/generic_validation/actions/workflows/python.yml/badge.svg)](https://github.com/simphotonics/generic_validation/actions/workflows/python.yml)
[![Python](https://simphotonics.com/images/docs-badge.svg)](https://generic-validation.simphotonics.com)

Attaching units to numerical quantities is a convenient way to check if
an expression is valid or an equation is consistent.
For example, it makes little sense to add a quantity
representing weight and one representing distance, or to
add seconds and pico-seconds.

The package [`unitexpr`][unitexpr] provides classes and meta-classes that
make it trivial to define custom unit systems and united [`numpy`][numpy] arrays.

A search on [pypi][pypi] shows that there are a few packages available
for doing unit analysis. The most notable I found is [`scimath`][scimath],
which supports unit conversion and working with united numpy arrays.
For the purpose of optimization [`scimath`][scimath] computes and stores unit
expressions in terms of base units.

The package [`unitexpr`][unitexpr] stores unit expressions in terms of
base units *and* derived units. The advantage is that unit expressions
retain their form. For example, the constant `m_e*c/h_bar` (where `m_e` is
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

The sections below demonstrates how to sub-class [`UnitBase`][UnitBase]
to define unit systems and united numpy arrays.

### Unit Symbols

In order to define a unit system, one must first specify the
base units. In the context of this package this is done using
the immutable class `UnitSymbol` which has
the instance attributes `symbol`, `name`, and `quantity`.
``` Python
# Defining unit symbols
unit_symbols = (
            UnitSymbol(symbol='m','name'='meter',quantity='length'),
            UnitSymbol(symbol='s','name'='second',quantity='time'),
            UnitSymbol(symbol='kg','name'='kilogram',quantity='weight')
        )
```
The attribute `symbol` must be a valid Python identifier. It is
advisable to choose the unit variable name as the symbol. For example,
in the section below, the constant `c` represents the speed of light and
the unit symbol is 'c'.

### Defining a Unit System

A custom unit system can be defined by sub-classing [`UnitBase`][UnitBase]:

```Python
# Defining a unit system using the base unit symbol specified above.
class MetricUnit(UnitBase, metaclass=UnitMeta, unit_symbols=unit_symbols):
    pass

# Base units are available as class attributes. For example:
m = MetricUnit.m
s = MetricUnit.s
kg = MetricUnit.kg

assert type(m) == MetricUnit

# Declaring derived units
c = MetricUnit('c', 'speed of light', 'velocity', expr=299792458*m/s)
```
The class definition requires an iterable with entries of type `UnitSymbol`
which are used to specify the base units.

The base units are constructed during the instantiation of the meta-class
and are available as class attributes.

Derived units and unit expressions can be constructed using the operations:
- multiplication: `J = MetricUnit('J', 'joule', 'energy', expr=N*m)`
- division: `W = SiUnit('W', 'watt', 'power', expr=J/s)`
- scalar multiplication: `c = MetricUnit('c', 'speed of light', 'velocity', expr=299792458*m/s)`
- exponentiation: `N = MetricUnit('N', 'newton', 'force', expr=kg*m*s**-2)`

The operations above follow the mathematical conventions, however
unit *addition* and *subtraction* operations are defined such that:
`c == c + c` and `c == c - c`. To perform arithmetic operations using units
it is recommended to use united arrays.

Note: Units and unit expressions extend Python's `namedtuple` and as such are immutable.


### United Numpy Arrays

To support scientific calculation
the package also includes a united array.
The class `UnitArray`
extends numpy's `ndarray` adding the additional
instance attribute `unit` (with default value 1.0).

```Python
from math import pi

from units.unit_array import UnitArray
from units.si_units import m, s, h_bar, m_e, c, SiUnit


a = UnitArray(shape=(2, 2), unit=m)
a.fill(10.0)

print('a = \n {} \n'.format(a))

b = UnitArray(shape=(2, 2), unit=s)
b.fill(2.0)

print('b = \n {} \n'.format(b))

d = a / b

print('a / b = \n {} \n'.format(d))

print('(a / b)**2 = \n {} \n'.format(d**2))

Pi = SiUnit('Pi', 'Pi', 'number', pi*SiUnit.one)

print('m_e*c/h_bar = {} = {}\n'.format(m_e*c/h_bar, (m_e*c/h_bar).base_repr()))

print('Pi*a*9.81*m/s**2 = \n {} \n '.format(Pi*a*9.81*m/s**2))
```
Running the script above produces the following output:
``` Console
(units) $ python bin/unit_array_example.py
a =
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

m_e*c/h_bar = m_e*c*h_bar**-1.0 = 2589605074819.227*m**-1.0

Pi*a*9.81*m/s**2 =
 [[98.1 98.1]
 [98.1 98.1]] unit: Pi*m**2.0*s**-2.0
```

Tip: United arrays can be multiplied with unit expressions.
Any numerical factor will be multiplied with the array using scalar
multiplication. The remaining part of the unit expression will be
multiplied with the unit attribute of the array.

To retain a numerical factor, for example `pi` as term of the
unit expression it must be decared as a unit (see the example
below).

``` Python
from math import pi
from units.unit_array import UnitArray
from units.si_units import *


a = UnitArray(shape=(2,2), unit = kg)
a.fill(10.0)
expr = 9.81*m/s**2
print(a*expr)

# Prints:
# [[98.1 98.1]
#  [98.1 98.1]] unit: kg*m*s**-2.0

Pi = SiUnit(symbol = 'Pi', name = 'Pi',quantity = 'number', expr=math.pi*SiUnit.expr_type.one)

print(Pi*a*expr)
# Prints:
# [[98.1 98.1]
#  [98.1 98.1]] unit: Pi*kg*m*s**-2.0

```


## Features and bugs

Please file feature requests and bugs at the [issue tracker].
Contributions are welcome.

[issue tracker]: https://github.com/simphotonics/unitexpr/issues

[numpy]: https://pypi.org/project/numpy/

[pypi]: https:://pypi.org

[pytest]: https://pypi.org/project/pytest/

[scimath]: https://pypi.org/project/scimath

[unitexpr]: https://github.com/simphotonics/unitexpr