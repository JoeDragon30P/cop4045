"""Problem 2: List and Dictionary Comprehensions.

Demonstrates Python comprehensions for filtering, mapping, anagram matching,
and string transformation operations.
"""

from typing import List, Tuple, Dict

def part_a() -> List[Tuple[int, int, int, int]]:
    """List comprehension: Tuples (a,b,c,d) where 1 <= a,b,c,d <= 10 and a^2 + b^2 = c^2 + d^2."""
    return [
        (a, b, c, d)
        for a in range(1, 11)
        for b in range(1, 11)
        for c in range(1, 11)
        for d in range(1, 11)
        if len({a, b, c, d}) == 4 and (a**2 + b**2 == c**2 + d**2)
    ]

def part_b(words: List[str]) -> List[Tuple[str, int]]:
    """List comprehension: Map lowercase string and length for words shorter than 5 chars."""
    return [(w.lower(), len(w)) for w in words if len(w) < 5]

def part_c(names: List[str]) -> List[str]:
    """List comprehension: Format 'First Mid Last' into 'First M. Last'."""
    return [
        f"{parts[0]} {parts[1][0]}. {parts[2]}"
        for parts in [name.split() for name in names]
        if len(parts) == 3
    ]

def part_d(lst1: List[str], lst2: List[str]) -> List[Tuple[str, str]]:
    """List comprehension: Case-insensitive anagram matching between two lists."""
    return [
        (w1, w2)
        for w1 in lst1
        for w2 in lst2
        if sorted(w1.lower()) == sorted(w2.lower())
    ]

def part_e(words: List[str]) -> Dict[str, int]:
    """Dictionary comprehension: Map each distinct string to its length."""
    return {w: len(w) for w in words}

def part_f(text: str) -> Dict[int, str]:
    """Dictionary comprehension: Map index -> vowel for all vowels in text."""
    vowels = "aeiouAEIOU"
    return {idx: char for idx, char in enumerate(text) if char in vowels}

def main() -> None:
    """Run and display results for parts a through f."""
    print("--- Part A: Quadruples (a,b,c,d) with equal sum of squares ---")
    quads = part_a()
    print(f"Total matching quadruples: {len(quads)}")
    print(f"Sample (first 5): {quads[:5]}\n")

    print("--- Part B: Lowercase & Length Filter (< 5 chars) ---")
    sample_b = ['One', 'SEVEN', 'three', 'two', 'Ten']
    print(part_b(sample_b), "\n")

    print("--- Part C: Name Abbreviation ---")
    sample_c = ['Christopher Ashton Kutcher', 'Elizabeth Stamatina Fey']
    print(part_c(sample_c), "\n")

    print("--- Part D: Anagram Pairs ---")
    l1 = ["Spam", "Trams", "Elbows", "Tops", "Astral"]
    l2 = ["Bowels", "Sample", "Altars", "Stop", "Course", "Smart"]
    print(part_d(l1, l2), "\n")

    print("--- Part E: Word Length Map ---")
    sample_e = ['one', 'two', 'three']
    print(part_e(sample_e), "\n")

    print("--- Part F: Vowel Index Map ---")
    sample_f = "Hello world"
    print(part_f(sample_f))

if __name__ == "__main__":
    main()
