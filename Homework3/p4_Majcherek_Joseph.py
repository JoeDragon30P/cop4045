"""
Problem 4: Non-Interactive Text Editor Operations
"""

import os
import tempfile
from typing import List


def testif(b: bool, testname: str, msgOK: str = "", msgFailed: str = "") -> bool:
    if b:
        print(f"Success: {testname}; {msgOK}")
    else:
        print(f"Failed: {testname}; {msgFailed}")
    return b


def ed_read(filename: str, from_pos: int = 0, to_pos: int = -1) -> str:
    """This reads the content from filename within half-open index interval [from_pos, to_pos)."""
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    length = len(content)
    if to_pos == -1:
        to_pos = length

    if to_pos > length:
        raise IndexError(f"Position to_pos={to_pos} exceeds total file length={length}.")

    return content[from_pos:to_pos]


def ed_find(filename: str, search_str: str) -> List[int]:
    """Finds starting indices of all occurrences of search_str in filename."""
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    indices = []
    idx = content.find(search_str)
    while idx != -1:
        indices.append(idx)
        idx = content.find(search_str, idx + 1)
    return indices


def ed_replace(filename: str, search_str: str, replace_with: str, occurrence: int = -1) -> int:
    """
    Replaces occurrences of search_str with replace_with in filename.
    If occurrence == -1, replaces all; otherwise, replaces only specified index occurrence.
    If occurrence >= 0, replaces only the 0-indexed occurrence
    """
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    occurrences: List[int] = []
    idx = content.find(search_str)
    while idx != -1:
        occurrences.append(idx)
        idx = content.find(search_str, idx + 1)

    if not occurrences:
        return 0

    if occurrence == -1:
        new_content = content.replace(search_str, replace_with)
        replaced_count = len(occurrences)
    elif 0 <= occurrence < len(occurrences):
        target_idx = occurrences[occurrence]
        new_content = content[:target_idx] + replace_with + content[target_idx + len(search_str):]
        replaced_count = 1
    else:
        return 0 # Occurrence index exceeds actual count

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(new_content)

    return replaced_count


def ed_append(filename: str, string: str) -> int:
    """Appends string to filement and returns character count written."""
    with open(filename, 'a', encoding='utf-8') as f:
        f.write(string)
    return len(string)

def test_ed_find() -> None:
    temp_dir = tempfile.gettempdir()
    fn = os.path.join(temp_dir, "test_find_file.txt")
    with open(fn, 'w', encoding='utf-8') as f:
        f.write("01234567890123456789")

    results = ed_find(fn, "345")
    testif(results == [3, 13], "test_ed_find", "Found at correct indices [3, 13]", f"Incorrect: {results}")


def test_ed_replace() -> None:
    temp_dir = tempfile.gettempdir()
    fn = os.path.join(temp_dir, "test_replace_file.txt")
    with open(fn, 'w', encoding='utf-8') as f:
        f.write("01234567890123456789")

    cnt = ed_replace(fn, "345", "ABC", 1)
    read_str = ed_read(fn)
    expected = "0123456789012ABC6789"
    testif(cnt == 1 and read_str == expected, "test_ed_replace occurrence=1", "Specific occurrence replaced", "Replacement failed")


def main() -> None:
    print("FAU ID: Z23348563 - Joseph Majcherek")
    print("=== Running Unit Tests ===")
    test_ed_find()
    test_ed_replace()

    print("\n=== Demonstrating Operations ===")
    temp_dir = tempfile.gettempdir()
    demo_fn = os.path.join(temp_dir, "p4_demo.txt")
    if os.path.exists(demo_fn):
        os.remove(demo_fn)

    ed_append(demo_fn, "0123456789")
    ed_append(demo_fn, "0123456789")

    print("Read [3, 9):", ed_read(demo_fn, 3, 9))
    print("Read from 3 to end:", ed_read(demo_fn, 3))
    print("Find '345':", ed_find(demo_fn, "345"))
    ed_replace(demo_fn, "345", "ABCDE", 1)
    print("Replaced occurrence 1:", ed_read(demo_fn))
    ed_replace(demo_fn, "345", "ABCDE")
    print("Replaced all remaining:", ed_read(demo_fn))

if __name__ == "__main__":
    main()