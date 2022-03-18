## 0.1.6
- Added property `base` to class `qarray`.

## 0.1.5
- Removed the class `Quantity` and replaced it by a
  function with name `quantity`.
- Units and unit expressions can now be combined with qarrays
to create new expressions.

## 0.1.4

Replaced class `Quantity` with a subclass of `qarray`.
Amended docs and tests.

## 0.1.3

Amended method `__str__` in class `Quantity`.
Unitless quantities are now formatted like the
corresponding numerical value.

## 0.1.2

* Amended docs and hyperlinks.

## 0.1.1

* Fixed error in class `Quantity` method `__normalize`.
* Added support for mixing quantities and units in expressions.
* Extended tests.

## 0.1.0

Corrected logical error in class `Unit` property `base_expr`.

## 0.0.9

Amended docs.

## 0.0.8

* Renamed class `QArray` -> `qarray`.
* Class `Quantity` is now a scalar and does not subclass `qarray`.
* Restructured docs.

## 0.0.7

Added package [lockattrs] to config option `install_requires`.

## 0.0.6

Class `Quantity` now has a property named `value`.

## 0.0.5

Added class `Quantity`. Refactored `QArray` operators.

## 0.0.4

Amended link.

## 0.0.3

Amended format of links on pypi.

## 0.0.2

Amended docs.

## 0.0.1

Initial commit.


[lockattrs]: https://pypi.org/project/lockattrs/