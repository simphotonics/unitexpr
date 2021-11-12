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
------------------------- benchmark: 6 tests -------------------------------------------------
Name (time in ns)                     Mean              StdDev              Rounds  Iterations
----------------------------------------------------------------------------------------------
test_compare_scimath_units       203.8330 (1.0)       23.0057 (1.0)          4       20000
test_compare_unitexpr_units      394.0667 (1.93)      39.9519 (1.74)         4       20000

test_add_scimath_units         3,777.9920 (18.53)    163.5955 (7.11)         4       20000
test_add_unitexpr_units        5,620.7861 (27.58)    209.8420 (9.12)         4       20000

test_mult_scimath_units        4,401.2288 (21.59)    191.2286 (8.31)         4       20000
test_mult_unitexpr_units       6,056.7404 (29.71)    394.6591 (17.15)        4       20000
----------------------------------------------------------------------------------------------
```

As the test runs above show [`scimath`][scimath] unit comparisons and unit
operations are calculated faster compared to [`unitexpr`][unitexpr] units.

This result is expected due to the additional computational effort
involved with keeping track of [`unitexpr`][unitexpr] terms as
well as type checking required
during comparison and arithmetic operations.

For the purpose of optimization [`scimath`][scimath] computes and stores unit
expressions in terms of base units. The package
[`unitexpr`][unitexpr] stores unit expressions in terms of
base units *and* derived units.

The advantage is that unit expressions
retain their form. For example, the constant `m_e*c/h_bar` (where `m_e` is
the electron mass, `c` is the velocity of light, `h_bar` is the
reduced Planck constant) is displayed as `m_e*c*h_bar**-1.0`. In
terms of SI base units the same constant is given by
the less obvious expression: `2589605074819.227*m**-1.0`.

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

An excerpt of a sample output (produced on a PC with 32GB RAM memory
and an Intel Core i5-6260U CPU running at 1.80GHz) is displayed below:

```Console
--------------------------------------------- benchmark: 4 tests --------------------
Name (time in us)              Mean             StdDev             Rounds  Iterations
-------------------------------------------------------------------------------------
test_add_unitexpr          816.8583 (1.0)       9.2904 (1.0)            2      500
test_add_scimath_units   1,420.2525 (1.74)     13.9224 (1.50)           2      500

test_mult_unitexpr       1,558.9613 (1.91)     19.3059 (2.08)           2      500
test_mult_scimath_units  1,612.5352 (1.97)     41.6187 (4.48)           2      500
-------------------------------------------------------------------------------------
```

To produce the benchmarks the following arrays were constructed:
``` python
from numpy import ndarray

from unitexpr.si_units import m, s
from unitexpr.unit_array import UnitArray

from scimath.units.length import meter
from scimath.units.time import second
from scimath.units.unit_array import UnitArray as UnitArraySci

M = UnitArray(shape=(1000, 1000), unit=m**2)
M.fill(10.0)

S = UnitArray(shape=(1000, 1000), unit=s)
S.fill(10.0)

A = ndarray(shape=(1000,1000))
A.fill(10.0)

M1 = UnitArraySci(A, units=meter*meter)
S1 = UnitArraySci(A, units=second)
```

The first set of benchmarks was produced by repeatedly calculating the
expressions: `M + M` and `M1 + M1`.

The second set of benchmarks was produced by calculating
`M/(S**2)` and `M1/(S1**2)`.


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