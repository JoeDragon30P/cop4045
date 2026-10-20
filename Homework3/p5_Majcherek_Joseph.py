"""
Problem 5: Recursive Functions and Turtle Graphics
"""

import sys
from typing import Dict, Tuple, List, Any

def testif(b: bool, testname: str, msgOK: str = "", msgFailed: str = "") -> bool:
    """Utility testing assertion helper."""
    if b:
        print(f"Success: {testname}; {msgOK}")
    else:
        print(f"Failed: {testname}; {msgFailed}")
    return b

# --- Part A: Recursive Leaf ---
def draw_leaf_straight(level: int, length: float) -> None:
    import turtle
    if level == 0:
        return

    turtle.forward(length)

    # Left Vein Branch
    turtle.left(45)
    draw_leaf_straight(level - 1, length * 0.5)
    turtle.right(45)

    # Right Vein Branch
    turtle.right(45)
    draw_leaf_straight(level - 1, length * 0.5)
    turtle.left(45)

    turtle.backward(length)


def draw_leaf_curved(level: int, length: float) -> None:
    """[Extra Credit] Draws a curved recursive leaf structure."""
    import turtle
    if level == 0:
        return

    turtle.forward(length)

    turtle.left(30)
    draw_leaf_curved(level - 1, length * 0.55)
    turtle.right(15)

    turtle.right(45)
    draw_leaf_curved(level - 1, length * 0.4)
    turtle.left(30)

    turtle.backward(length)


# --- Part B: Base-X Conversion ---
def strB(n: int, base: int = 10) -> str:
    """Recursively converts non-negative integer n into base string representation."""
    digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if n < base:
        return digits[n]
    return strB(n // base, base) + digits[n % base]


# --- Part C: Memoized Binomial Coefficient ---
_cnk_memo: Dict[Tuple[int, int], int] ={}

def Cnk_m(n: int, k: int) -> int:
    """Recursively computes n-choose-k binomial coefficient with manual memoization."""
    if k == 0 or k == n:
        return 1
    if (n, k) in _cnk_memo:
        return _cnk_memo[(n, k)]

    val = Cnk_m(n - 1, k - 1) + Cnk_m(n - 1, k)
    _cnk_memo[(n, k)] = val
    return val

def run_Cnk(n: int, k: int) -> int:
    res = Cnk_m(n, k)
    print(f"C({n}, {k}) = {res}")
    return res

# --- Part D: Recursive Pairs ---
def make_pairs(seq1: List[Any], seq2: List[Any], acc: List[Tuple[Any, Any]] = None) -> List[Tuple[Any, Any]]:
    """Recursively pairs elements from two lists until shorter sequence ends."""
    if acc is None:
        acc = []

    if not seq1 or not seq2:
        return acc

    acc.append((seq1[0], seq2[0]))
    return make_pairs(seq1[1:], seq2[1:], acc)

def render_turtle_leaf() -> None:
    import turtle
    screen = turtle.Screen()
    screen.title("Problem 5 - Recursive Leaf (Joseph Majcherek - Z23348563)")
    turtle.hideturtle()
    turtle.speed(0)
    turtle.tracer(0, 0)
    turtle.penup()
    turtle.goto(0, -180)
    turtle.pendown()
    turtle.left(90) # Face vertically North

    draw_leaf_straight(6, 120)
    turtle.update()
    print("Leaf drawn successfully. Click the window or close it to exit.")
    turtle.mainloop()


def main() -> None:
    print("FAU ID: Z23348563 - Joseph Majcherek")
    print("=== Running Unit Tests ===")

    # Part B Unit Tests
    testif(strB(10, 8) == "12", "strB(10, base=8)", "12", "Failed")
    testif(strB(100, 16) == "64", "strB(100, base=16)", "64", "Failed")
    testif(strB(1234, 16) == "4D2", "strB(1234, base=16)", "4D2", "Failed")
    testif(strB(16, 2) == "10000", "strB(16, base=2)", "10000", "Failed")

    # Part C Unit Tests
    testif(Cnk_m(5, 2) == 10, "Cnk_m(5, 2)", "10", "Failed")
    testif(Cnk_m(10, 5) == 252, "Cnk_m(10, 5)", "252", "Failed")
    testif(Cnk_m(7, 0) == 1, "Cnk_m(7, 0)", "1", "Failed")
    testif(Cnk_m(6, 6) == 1, "Cnk_m(6, 6)", "1", "Failed")

    # Part D Unit Tests
    testif(make_pairs([1, 2, 3], [4, 5, 6]) == [(1, 4), (2, 5), (3, 6)], "make_pairs equal lists", "Matched", "Failed")
    testif(make_pairs([1, 2, 3], [4, 5]) == [(1, 4), (2, 5)], "make_pairs seq2 shorter", "Matched", "Failed")
    testif(make_pairs([1, 2], [4, 5, 6]) == [(1, 4), (2, 5)], "make_pairs seq1 shorter", "Matched", "Failed")
    testif(make_pairs([], [4, 5]) == [], "make_pairs seq1 empty", "[]", "Failed")
    testif(make_pairs([1, 2], []) == [], "make_pairs seq2 empty", "[]", "Failed")

    # Run Cnk demonstration
    print("\n--- Binomial Coefficient Console Run ---")
    run_Cnk(8, 3)
    run_Cnk(12, 4)

    # Check if GUI was opted out
    if "--no-gui" in sys.argv:
        print("\nSkipping GUI window display (--no-gui flag passed).")
        return

    # Safely display Turtle leaf
    print("\nDisplaying Turtle Drawing...")
    try:
        render_turtle_leaf()
    except Exception as e:
        print(f"Could not render GUI: {e}")


if __name__ == "__main__":
    main()