# Unit Expressions - Benchmark

The package [`unitexpr`][unitexpr] provides classes and meta-classes that
make it trivial to define custom unit systems and united [`numpy`][numpy] arrays.

A search on [pypi][pypi] shows that there are a few packages available
for doing unit analysis. The most notable I found is [`scimath`][scimath],
which supports unit conversion and working with united numpy arrays.

The section below contains benchmarks comparing the performance of
[`unitexpr`][unitexpr] units with those provided by the
package [`scimath`][scimath].

Note: To run the benchmarks one must install the packages:
[`pytest-benchmark`][pytest-benchmark] and [`pytest`][pytest].


## Unit Expressions

To run the benchmarks from the root directory of the package
[`unitexpr`][unitexpr] use the command:
```Console
$ pytest benchmarks/unit_benchmark.py
```

An excerpt of a sample output (produced on a PC with 32GB RAM memory
and an Intel Core i5-6260U CPU running at 1.80GHz) is displayed below:

```Console
----------------------------- benchmark: 6 tests ------------------------------------------
Name (time in ns)                   Mean              StdDev             Rounds  Iterations
-------------------------------------------------------------------------------------------
test_compare_scimath_units      378.0144 (1.0)       26.0803 (1.0)            4       20000
test_compare_unitexpr_units     474.4168 (1.26)      77.8908 (2.99)           4       20000

test_add_scimath_units        3,737.2815 (9.89)     449.5742 (17.24)          4       20000
test_add_unitexpr_units       5,411.9090 (14.32)    678.7292 (26.02)          4       20000

test_mult_scimath_units       4,308.2672 (11.40)    209.4878 (8.03)           4       20000
test_mult_unitexpr_units      5,813.6167 (15.38)    278.0202 (10.66)          4       20000
-------------------------------------------------------------------------------------------
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
The class `UnitArray`
extends numpy's `ndarray` adding the additional
instance attribute `unit` (with default value 1.0).

The section below contains benchmarks comparing the performance of
[`unitexpr`][unitexpr] united numpy arrays with united arrays
provided by the package [`scimath`][scimath].

To run the benchmarks from the root directory of the
 package [`unitexpr`][unitexpr] use the command:
```Console
$ pytest benchmarks/unit_array_benchmark.py
```

A sample output (not all columns are shown) produced on a PC with 32GB RAM memory
and an Intel Core i5-6260U CPU running at 1.80GHz is displayed below:

```Console
--------------------------- benchmark: 4 tests -----------------------------------
Name (time in us)             Mean             StdDev           Rounds  Iterations
----------------------------------------------------------------------------------
test_mult_scimath_units    69.5785 (1.00)     11.1675 (1.23)         2         500
test_mult_unitexpr_units   69.3301 (1.0)      10.0463 (1.11)         2         500

test_add_unitexpr_units    76.7611 (1.11)      9.0428 (1.0)          2         500
test_add_scimath_units     94.3358 (1.36)     16.3649 (1.81)         2         500
----------------------------------------------------------------------------------
```

To produce the benchmarks the following arrays were constructed:
``` python

from numpy import ndarray, array_equal

from unitexpr.si_units import m, s, SiUnit
from unitexpr.unit_array import UnitArray

from scimath.units.length import meter, centimeter
from scimath.units.time import second
from scimath.units.mass import kilogram

from scimath.units.unit_array import UnitArray as UnitArraySci

cm = SiUnit("cm", "centimeter", "length", 1.0e-2 * m)

nx = 200
ny = 200

A = ndarray(shape=(nx, ny))
A.fill(10.0)

M = UnitArray(shape=(nx, ny), unit=m ** 2)
M.fill(10.0)

C = UnitArray(shape=(nx, ny), unit=cm ** 2)
C.fill(1.0e4)

S = UnitArray(shape=(nx, ny), unit=s)
S.fill(10.0)

R = UnitArray(shape=(nx, ny), unit=m ** 2)
R.fill(11)
```

The first set of benchmarks was produced by repeatedly calculating the
expressions: `M + C` and `M1 + C1`.

The second set of benchmarks was produced by calculating
`M/(S**2)` and `M1/(S1**2)`.


The results displayed above show that performance of
`unitexpr` and `scimath` united arrays is very similar.

As a rough estimate calculations involving units are of the order of microseconds to
tens of microseconds (depending on the complexitiy of the unit expression).

The fraction of computational time spent on unit operations becomes negligable
when performing calculations on large arrays with more than 10000 elements.



## Features and bugs

Please file feature requests and bugs at the [issue tracker].
Contributions are welcome.

[issue tracker]: https://github.com/simphotonics/unitexpr/issues

[numpy]: https://pypi.org/project/numpy/

[pypi]: https:://pypi.org

[pytest]: https://pypi.org/project/pytest/

[pytest-benchmark]: https://pypi.org/project/pytest-benchmark/

[scimath]: https://pypi.org/project/scimath

[unitexpr]: https://github.com/simphotonics/unitexpr