"""
Problem 1: NVector Class Implementation
This program implements an N-dimensional vector of real numbers with standard vector operations, container behaviors, and comprehensive unit tests.
"""

from typing import Union, Sequence, List, Any

def testif(b: bool, testname: str, msgOK: str = "", msgFailed: str = "") -> bool:
    """
    This is utility function used for testing code logic.
    """
    if b:
        print(f"Success: {testname}; {msgOK}")
    else:
        print(f"Failed: {testname}; {msgFailed}")
    return b

class NVector:
    """
    This represents an N-dimensional vector storing real numbers in an internal list.
    Supports addition, scalar multiplication, indexing, and equality testing.
    """

    def __init__(self, *args: Any) -> None:
        """
        This constructs a NVector to accept either a single sequence (list.tuple) or multiple numerical scalar arguments.
        """
        if len(args) == 1:
            first_arg = args[0]
            if isinstance(first_arg, (list, tuple)):
                self._elements: List[float] = [float(x) for x in first_arg]
            else:
                try:
                    self._elements = [float(x) for x in list(first_arg)]
                except TypeError:
                    raise TypeError("Single argument must be a sequence/iterable of numbers.")
        elif len(args) > 1:
            self._elements = [float(x) for x in args]
        else:
            raise TypeError("NVector requires at least one argument.")

    def __len__(self) -> int:
        """This returns the dimension (number of elements) of the vector."""
        return len(self._elements)

    def __getitem__(self, index: int) -> float:
        """This retrieves element at specified index (supports negative indexing.)"""
        return self._elements[index]

    def __setitem__(self, index: int, value: float) -> None:
        """Sets value at specified index (supports negative indexing.)"""
        self._elements[index] = float(value)

    def __str__(self) -> str:
        """This returns a string representation of NVector in bracketed format."""
        return f"NVector({self._elements})"

    def __repr__(self) -> str:
        """This returns unambiguous technical representative of NVector."""
        return f"NVector({self._elements})"

    def __eq__(self, other: Any) -> bool:
        """Checks element-wise equality with another NVector."""
        if not isinstance(other, NVector):
            return False
        if len(self) != len(other):
            return False
        return self._elements == other._elements

    def __ne__(self, other: Any) -> bool:
        """Checks inequality with another object."""
        return not self.__eq__(other)

    def __add__(self, other: Union['NVector', float, int]) -> 'NVector':
        """
        Adds another Nvector element-wise or add a scalar to all elements.
        """
        if isinstance(other, NVector):
            if len(self) != len(other):
                raise ValueError("Vectors must be of identical length for addition.")
            return NVector([a + b for a, b in zip(self._elements, other._elements)])
        elif isinstance(other, (int, float)):
            return NVector([a + float(other) for a in self._elements])
        else:
            return NotImplemented

    def __radd__(self, other: Union[float, int]) -> 'NVector':
        """Supports reflected addition: scalar + NVector."""
        return self.__add__(other)

    def __mul__(self, other: Union['NVector', float, int]) -> Union['NVector', float]:
        """
        This performs dot product if other is NVector, or scalar multiplication if other is a number.
        """
        if isinstance(other, NVector):
            if len(self) != len(other):
                raise ValueError("Vectors must be of identical length for dot product.")
            return sum(a * b for a, b in zip(self._elements, other._elements))
        elif isinstance(other, (int, float)):
            return NVector([a * float(other) for a in self._elements])
        else:
            return NotImplemented

    def __rmul__(self, other: Union[float, int]) -> 'NVector':
        """Supports reflected  scalar multiplication: scalar * NVector."""
        if isinstance(other, (int, float)):
            return NVector([a * float(other) for a in self._elements])
        return NotImplemented

    @classmethod
    def zeros(cls, n: int) -> 'NVector':
        """Constructs an n-dimensional NVector with all zero elements."""
        if n <= 0:
            raise ValueError("Dimension n must be positive.")
        return cls([0.0] * n)

def main() -> None:
    """Main unit tests execution for NVector class using testif."""
    print("=== Running Problem 1 Unit Tests ===")

    # Constructor & len tests
    v1 = NVector([3, 0, 1, -1])
    testif(len(v1) == 4, "Constructor List & len() Test", "Length is 4", "Length mismatch")

    v2 = NVector(3, 0, 1, -1)
    testif(v1 == v2, "Multi-argument Constructor & __eq__ Test", "Vectors are equal", "Vectors not equal")

    # Indexing tests
    testif(v1[1] == 0.0, "Getitem Positive Index", "v1[1] is 0.0", "v1[1] failed")
    testif(v1[-2] == 1.0, "Getitem Negative Index", "v1[-2] is 1.0", "v1[-2] failed")

    # Setitem test
    v1[2] = 5.0
    testif(v1[2] == 5.0 and v1 == NVector([3, 0, 5, -1]), "Setitem Test", "v1[2] updated to 5.0", "Setitem failed")

    # String test
    testif(str(v1) == "NVector([3.0, 0.0, 5.0, -1.0])", "Str representation", "String matches", "String mismatch")

    # Addition tests
    a = NVector([3, 0, 1, -1])
    b = NVector([1, 2, 3, 4])
    testif(a + b == NVector([4, 2, 4, 3]), "Vector Addition", "a+b correct", "a+b failed")
    testif(a + 10 == NVector([13, 10, 11, 9]), "Vector-Scalar Addition", "a+10 correct", "a+10 failed")
    testif(10 + a == NVector([13, 10, 11, 9]), "Reflected Scalar Addition", "10+a correct", "10+a failed")

    # Multiplication tests
    testif(a * b == 2.0, "Dot Product Multiplication", "a*b is 2.0", "a*b failed")
    testif(a * 2 == NVector([6, 0, 2, -2]), "Scalar Multiplication", "a*2 correct", "a*2 failed")
    testif(3 * a == NVector([9, 0, 3, -3]), "Reflected Scalar Multiplication", "3*a correct", "3*a failed")

    # Zeros class method test
    z = NVector.zeros(3)
    testif(z == NVector([0, 0, 0]), "Zeros Class Method", "3D Zeros created", "Zeros creation failed")

if __name__ == "__main__":
    main()