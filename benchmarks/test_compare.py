import pytest
import operator

from numpy import ndarray, array, zeros
from numpy.core.numeric import array_equal


def array_is_zero(input):
    '''Returns `True` if all entries are zero.
    '''
    for element in input:
        if element != 0.0:
            return False
    return True


def array_equalII(left, right):
    ''' Returns `True` if numpy arrays of matching shape contain
        equal elements. Note: Shape-matching is not inforced.
    '''
    for left_element, right_element in zip(left, right):
        if left_element != right_element:
            return False
    return True


a = (1, 2, 3, 4, 5.0, 6, 7.0)
b = (101, 102, 103, 104, 105.0, 106.0, 107.0)

zero = (0, 0, 0, 0, 0, 0, 0)
A = array(a)
B = array(b)


class TestUnitAdd:

    def test_compare_tuple(self, benchmark):
        def compare():
            a == b
        benchmark.pedantic(compare, iterations=1000, rounds=1000)
        assert 1 == 1

    def test_compare_array(self, benchmark):
        def compare():
            tuple(A) == tuple(B)
        benchmark.pedantic(compare, iterations=1000, rounds=1000)
        assert 1 == 1

    def test_compare_array_local(self, benchmark):
        def compare():
            array_equal(A, B)
        benchmark.pedantic(compare, iterations=1000, rounds=1000)
        assert 1 == 1

    def test_compare_array_localII(self, benchmark):
        def compare():
            array_equalII(A, B)
        benchmark.pedantic(compare, iterations=1000, rounds=1000)
        assert 1 == 1

    def test_is_zero(self, benchmark):
        def compare():
            array_is_zero(A)
        benchmark.pedantic(compare, iterations=1000, rounds=1000)
        assert 1 == 1

    def test_compare_zero(self, benchmark):
        def compare():
          a == zero
        benchmark.pedantic(compare, iterations=1000, rounds=1000)
        assert 1 == 1
