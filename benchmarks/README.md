# Python  Unit Expressions - Benchmarks

The package [`unitexpr`][unitexpr] provides classes and meta-classes that
make it trivial to define custom unit systems and [`numpy`][numpy] arrays
with unit support.

A search on [pypi][pypi] shows that there are a few packages available
for doing unit analysis. The most notable I found is [`scimath`][scimath],
which supports unit conversion and working with united numpy arrays.

The section below contains benchmarks comparing the performance of
[`unitexpr`][unitexpr] units with those provided by the
package [`scimath`][scimath].

Note: To run the benchmarks one must install the packages:
[`pytest-benchmark`][pytest-benchmark] and [`pytest`][pytest].


## Unit Expressions

To run the benchmarks clone the repository available at
[`unitexpr`][unitexpr], navigate to the package root directory
and use the command:
```Console
$ pytest benchmarks/unit_benchmark.py
```

An excerpt of a sample output (produced on a PC with 32GB RAM memory
and an Intel Core i5-6260U CPU running at 1.80GHz) is displayed below:

```Console
-------------------------------- benchmark: 6 tests -----------------------------------
Name (time in ns)                   Mean              StdDev         Rounds  Iterations
---------------------------------------------------------------------------------------
test_compare_scimath_units      384.6454 (1.0)       49.9329 (1.0)        4       20000
test_compare_unitexpr_units     455.8162 (1.19)      62.7644 (1.26)       4       20000

test_add_scimath_units        3,698.7334 (9.62)     199.3424 (3.99)       4       20000
test_add_unitexpr_units       5,527.3140 (14.37)    666.3501 (13.34)      4       20000

test_mult_scimath_units       4,363.7948 (11.34)    204.8872 (4.10)       4       20000
test_mult_unitexpr_units      5,780.7208 (15.03)    205.6521 (4.12)       4       20000
---------------------------------------------------------------------------------------
```

As the test runs above show [`scimath`][scimath] unit comparisons and unit
operations are calculated slightly faster compared to [`unitexpr`][unitexpr] units.

This result is expected due to the additional computational effort
involved with keeping track of [`unitexpr`][unitexpr] terms as
well as type checking required
during comparison and arithmetic operations.

For the purpose of optimization [`scimath`][scimath] computes and stores unit
expressions in terms of base units. The package
[`unitexpr`][unitexpr] stores unit expressions in terms of
base units *and* derived units.


### United Numpy Arrays

To support scientific calculation
the package also includes a united array.
The class `qarray`
extends numpy's `ndarray` adding the additional
instance attribute `unit` (with default value 1.0).

The section below contains benchmarks comparing the performance of
[`unitexpr`][unitexpr] united numpy arrays with united arrays
provided by the package [`scimath`][scimath].

To run the benchmarks from the root directory of the
 package [`unitexpr`][unitexpr] use the command:
```Console
$ pytest benchmarks/qarray_benchmark.py
```

A sample output (not all columns are shown) produced on a PC with 32GB RAM memory
and an Intel Core i5-6260U CPU running at 1.80GHz is displayed below:

```Console
---------------------------------- benchmark: 4 tests -------------------
Name (time in us)        Mean           StdDev         Rounds  Iterations
-------------------------------------------------------------------------
test_add_qarray       57.8951 (1.0)    13.2057 (4.12)       4         700
test_add_unit_array   79.9009 (1.38)    5.3936 (1.68)       4         700

test_mult_qarray      63.5769 (1.10)    3.2046 (1.0)        4         700
test_mult_unit_array  63.4930 (1.10)    4.6779 (1.46)       4         700
-------------------------------------------------------------------------

```

To produce the benchmarks the following arrays were constructed:
``` python

from numpy import ndarray, array_equal

from unitexpr.si_units import m, s, SiUnit
from unitexpr.qarray import qarray

from scimath.units.length import meter, centimeter
from scimath.units.time import second
from scimath.units.mass import kilogram

from scimath.units.unit_array import UnitArray as UnitArraySci

cm = SiUnit("cm", "centimeter", "length", 1.0e-2 * m)

nx = 200
ny = 200

A = ndarray(shape=(nx, ny))
A.fill(10.0)

M = qarray.from_input(A, unit=m ** 2)

C = qarray(shape=(nx, ny), unit=cm ** 2)
C.fill(1.0e4)

S = qarray.from_input(A, unit=s)

R = qarray(shape=(nx, ny), unit=m ** 2)
R.fill(11)


A1 = UnitArraySci(A)
M1 = UnitArraySci(A, units=meter * meter)
C1 = UnitArraySci(C, units=centimeter * centimeter)
S1 = UnitArraySci(A, units=second)
R1 = UnitArraySci(R, units=meter * meter)
```

The first set of benchmarks was produced by repeatedly calculating the
expressions: `M + C` and `M1 + C1`.

The second set of benchmarks was produced by calculating
`M/(S**2)` and `M1/(S1**2)`.


The results displayed above show that the performance of
`unitexpr` and `scimath` united arrays is similar.

As a rough estimate calculations involving units are of the order of microseconds to
tens of microseconds (depending on the complexitiy of the unit expression).

The fraction of computational time spent on unit operations becomes negligable
when performing calculations on large arrays with more than 50000 elements.



## Features and bugs

Please file feature requests and bugs at the [issue tracker].
Contributions are welcome.

[issue tracker]: https://github.com/simphotonics/unitexpr/issues

[numpy]: https://pypi.org/project/numpy/

[pypi]: https://pypi.org

[pytest]: https://pypi.org/project/pytest/

[pytest-benchmark]: https://pypi.org/project/pytest-benchmark/

[scimath]: https://pypi.org/project/scimath

[unitexpr]: https://github.com/simphotonics/unitexpr