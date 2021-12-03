"""
Module providing custom error classes.
"""


class OperationNotSupported(Exception):
    """
    Error raised if an arithmetic operation involving unit expressions
    is not supported.

    Attributes:
        - `left`: Left operand.
        - `right`: Right operand.
        - `operator`: Arithmetic operator used in the expression.
        - `message`: Explanation of the error.
    """

    # pylint: disable=too-many-function-args
    def __init__(self, left, right, operator, addon_message=""):
        self.left = left
        self.right = right
        self.operator = operator
        self.addon_message = addon_message
        super().__init__(self)

    def __str__(self):
        """
        Returns the error message string.
        """
        return (
            "Could not evaluate: "
            + f"{self.left.__repr__()} {self.operator}"
            + f" {self.right.__repr__()} ."
            + self.addon_message
        )

    def __repr__(self):
        """
        Return the error message string.
        """
        return self.__str__(self)

    def invert(self):
        """
        Changes the order of the operands. (left, right) = (right, left)
        """
        (self.left, self.right) = (self.right, self.left)
        return self
