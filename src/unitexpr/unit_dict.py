"""
Dictionary intended to be used with numeric value types.
Adds support for arithmetic operators.
"""
from __future__ import annotations


class UnitDict(dict):
    """
    Extends `dict` adding support for the arithmetic
    operators `+`, `-`, scalar multiplication.

    * The value type must implement the operators above.
    * Strips keys with value zero.
    """

    # def __init__(self, *args, **kwargs):
    #    super().__init__(float, *args, **kwargs)

    def __sub__(self: UnitDict, other: UnitDict) -> UnitDict:
        """
        Subtracts the values of entries with the same key andipyt
        returns the resulting
        dictionary. Keys with value zero are deleted.

        Note: Returns a new object.
        """
        obj = dict(self)
        for term in other:
            tmp = obj[term] = obj.get(term, 0.0) - other[term]
            if not tmp:
                del obj[term]
        return self.__class__(obj)

    def copy(self) -> UnitDict:
        """
        Returns a new `UnitDict` object containing the same entries as `self`.
        """
        return self.__class__(self)

    def __add__(self: UnitDict, other: UnitDict) -> UnitDict:
        """
        Adds the values of entries with the same key and returns the resulting
        dictionary. Keys with value zero are deleted.

        Note: Returns a new object.
        """
        obj = UnitDict(self)
        for term in other:
            tmp = obj[term] = obj.get(term, 0.0) + other[term]
            if not tmp:
                del obj[term]
        return obj

    def __mul__(self: UnitDict, other: float) -> UnitDict:
        """
        Multiplies the value of each entry with `other` and returns the
        resulting dictionary.

        Note: Returns a new object.
        """
        if other == 0.0:
            return UnitDict()

        obj = UnitDict(self)
        for key in obj:
            obj[key] *= other
        return obj

    def __rmul__(self, other: float) -> UnitDict:
        """
        Multiplies `other` with the value of each entry and returns the
        resulting dictionary.

        Note: Returns a new object.
        """
        return self.__mul__(other)

    def __repr__(self) -> str:
        """
        Returns a string representation of self.
        """
        return self.__class__.__name__ + f"({super().__repr__()})"

    def __neg__(self) -> UnitDict:
        """
        Negates the dictionary values and returns the resulting
        dictionary.

        Note: Returns a new object.
        """
        obj = UnitDict(self)
        for key in obj:
            obj[key] *= -1
        return obj

    def filter_value(self, value) -> UnitDict:
        """
        Remove all entries with matching `value` and returns the resulting
        dictionary.

        Note: Returns a new object.
        """
        obj = UnitDict(self)
        for key in self.keys():
            if obj[key] == value:
                del obj[key]
        return obj


class ImmutableUnitDict(UnitDict):
    """
    Immutable class that extends `UnitDict` with support for the arithmetic
    operators `+`, `-`, scalar multiplication, and
    `**`.

    Note: The value type must implement the operators above.
    """

    def __add__(self: ImmutableUnitDict, other: UnitDict) -> ImmutableUnitDict:
        """
        Adds the values of entries with the same key and returns the resulting
        dictionary. Keys with value zero are deleted.

        Note: Returns a new object.
        """
        obj = dict(self)
        for term in other:
            tmp = obj[term] = obj.get(term, 0.0) + other[term]
            if not tmp:
                del obj[term]
        return ImmutableUnitDict(obj)

    def __sub__(self: ImmutableUnitDict, other: UnitDict) -> UnitDict:
        """
        Subtracts the values of entries with the same key and
        returns the resulting
        dictionary. Keys with value zero are deleted.

        Note: Returns a new object.
        """
        obj = dict(self)
        for term in other:
            tmp = obj[term] = obj.get(term, 0.0) - other[term]
            if not tmp:
                del obj[term]
        return ImmutableUnitDict(obj)

    def __rmul__(self, other: float) -> UnitDict:
        """
        Multiplies `other` with the value of each entry and returns the
        resulting dictionary.

        Note: Returns a new object.
        """
        return self.__mul__(other)

    def __mul__(self, other: float) -> ImmutableUnitDict:
        """
        Multiplies the value of each entry with `other` and returns the
        resulting dictionary.

        Note: Returns a new object.
        """
        if other == 0.0:
            return ImmutableUnitDict()

        obj = dict(self)
        for key in obj:
            obj[key] *= other
        return ImmutableUnitDict(obj)

    def __neg__(self) -> ImmutableUnitDict:
        obj = dict(self)
        for key in obj:
            obj[key] *= -1
        return ImmutableUnitDict(obj)

    def filter_value(self, value) -> ImmutableUnitDict:
        """
        Removes all entries with matching `value` and returns the resulting
        dictionary.

        Note: Returns a new object.
        """
        obj = dict(self)
        for key in self:
            if obj[key] == value:
                del obj[key]
        return ImmutableUnitDict(obj)

    def __setitem__(self, key, value) -> None:
        """
        Not supported. Immutable object.
        """
        raise TypeError(
            f"'{self.__class__.__name__}' object does not "
            + "support item assignment."
        )

    def __delitem__(self, value) -> None:
        """
        Not supported. Immutable object.
        """
        raise TypeError(
            f"'{self.__class__.__name__}' object does not "
            + "support item deletion."
        )

    def clear(self) -> None:
        """
        Not supported. Immutable object.
        """
        raise TypeError(
            f"'{self.__class__.__name__}' object " + "cannot be cleared."
        )

    def update(self, *args, **kwargs) -> None:
        """
        Not supported. Immutable object.
        """
        raise TypeError(
            f"'{self.__class__.__name__}' object " + "cannot be updated."
        )

    def setdefault(self, key, default) -> None:
        """
        Not supported. Immutable object.
        """
        raise TypeError(
            f"'{self.__class__.__name__}' object does not "
            + "support default values."
        )

    def pop(self) -> None:
        """
        Not supported. Immutable object.
        """
        raise TypeError(
            f"'{self.__class__.__name__}' object does not " + "support `pop`."
        )

    def popitem(self) -> None:
        """
        Not supported. Immutable object.
        """
        raise TypeError(
            f"'{self.__class__.__name__}' object does not "
            + "support `popitem`."
        )
