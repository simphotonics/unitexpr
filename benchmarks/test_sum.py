from typing import Iterable
import pytest
import operator

from numpy import ndarray, array, zeros
from numpy.core.numeric import array_equal


a = (1, 2, 3, 4, 5.0, 6, 7.0)
b = (101.0, 102.0, 103.0, 104.0, 105.0, 106.0, 107.0)

A = array(a)
B = array(b)


class TestUnitAdd:
    def test_add(self, benchmark):

        def add():
            t = tuple(x + y*1000 for x, y in zip(a, b))

        benchmark.pedantic(add, iterations=1000, rounds=1000)
        assert 1 == 1

    def test_add_map(self, benchmark):

        def add():
            t = tuple(map(sum, zip(a, b)))

        benchmark.pedantic(add, iterations=1000, rounds=1000)
        assert 1 == 1

    def test_add_array(self, benchmark):

        def add():
            t = A+1000*B

        benchmark.pedantic(add, iterations=1000, rounds=1000)
        assert 1 == 1

    def test_add_loop(self, benchmark):

        def add():
            t = tuple([a[i] + b[i]
                      for i in range(len(a))])

        benchmark.pedantic(add, iterations=1000, rounds=1000)
        assert 1 == 1

    def test_add_tuple(self, benchmark):
        def add():

            derivation = tuple(
                map(operator.add, a, map((1000.0).__mul__, b)))

        benchmark.pedantic(add, iterations=1000, rounds=1000)
        assert 1 == 1

    def test_add_mult_tuple(self, benchmark):

        factor = 1000
        def my_mult(x,y):
            return x + y

        def add():
            derivation = tuple(
                map(my_mult, a, b))

        benchmark.pedantic(add, iterations=1000, rounds=1000)
        assert 1 == 1
