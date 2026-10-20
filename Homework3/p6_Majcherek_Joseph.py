"""
Problem 6: Storage System Hierarchy with Polymorphism & Unit Testing
"""

from __future__ import annotations

import sys
import unittest
from abc import ABC, abstractmethod
from typing import List, Optional, Tuple

class Entry(ABC):
    """Base class for any item stored in the file system."""

    def __init__(self, name: str, parent: Optional["Folder"] = None) -> None:
        """This initializes an entry.
        
        Args:
            name: The name identifier of the entry.
            parent: Optional Folder in which this entry is contrained.
        """
        if not name or ("/" in name and name != "/"):
            raise ValueError(f"Invalid entry name: {name!r}")
        self.name: str = name
        self._parent: Optional["Folder"] = None
        if parent is not None:
            parent.add(self)

    def parent(self) -> Optional["Folder"]:
        """Returns the parent Folder object."""
        return self._parent

    @abstractmethod
    def size(self) -> int:
        """Abstract method returning the size in bytes."""
        pass

    def absolute_path(self) -> List["Entry"]:
        """Recursively bulids a list representing the path from current Entry up to Root.
        Returns:
            List[Entry]: [current_entry, parent, ..., root_entry]
        """
        if self._parent is None:
            return [self]
        return [self] + self._parent.absolute_path()

    def path_str(self) -> str:
        """Helper to return path as standard POSIX-like string."""
        path_nodes = self.absolute_path()[::-1]
        if len(path_nodes) == 1 and path_nodes[0].name == "/":
            return "/"
        names = [n.name for n in path_nodes if n.name != "/"]
        return "/" + "/".join(names)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name!r}, size={self.size()})"

    
class File(Entry):
    """Leaf node representing an individual file."""

    def __init__(self, name: str, bytes_used: int = 0, parent: Optional["Folder"] = None) -> None:
        """
        Initializes a File.

        Args:
            name: File name.
            bytes_used: Non-negative integer size in bytes.
            parent: Parent folder reference.
        """
        if bytes_used < 0:
            raise ValueError("bytes_used must be non-negative.")
        self.bytes_used: int = bytes_used
        super().__init__(name, parent)

    def size(self) -> int:
        """Returns the size of the file in bytes."""
        return self.bytes_used


class Folder(Entry):
    """Composite node representing a directory containing child entries."""

    def __init__(self, name: str, parent: Optional["Folder"] = None) -> None:
        """Initializes an empty Folder."""
        self._children: List[Entry] = []
        super().__init__(name, parent)

    def add(self, entry: Entry) -> Entry:
        """
        Adds a child entry to this folder and updates its parent reference.
        Enforces cycle prevention and unique naming constraints.
        """
        if entry.parent() is not None and entry.parent() is not self:
            raise ValueError(f"Entry {entry.name!r} already has a parent.")

        # Cycle detection: ensure self is not a descendant of entry
        node: Optional[Entry] = self
        while node is not None:
            if node is entry:
                raise ValueError("Cannot create a cycle in folder hierarchy.")
            node = node.parent()

        # Name collision prevention
        if any(c.name == entry.name for c in self._children):
            raise ValueError(f"Duplicate entry name {entry.name!r} in folder {self.name!r}.")

        entry._parent = self
        self._children.append(entry)
        return entry

    def remove(self, entry: Entry) -> None:
        """Removes a child entry from this folder."""
        self._children.remove(entry)
        entry._parent = None

    def size(self) -> int:
        """Polymorphically aggregates sizes of all contained children."""
        return sum(child.size() for child in self._children)

    def children(self) -> Tuple[Entry, ...]:
        """Returns an immutable tuple with all child entries."""
        return tuple(self._children)


def find_large_files(entry: Entry, minimum_size: int) -> List[File]:
    """
    Recursively finds all File objects whose sizes are at least minimum_size starting from entry.
    
    Args:
        entry: Root search node (either File or Folder).
        minimum_size: Nonnegative size threshold.
    Returns:
        List of matching File instances.
    """
    large_files: List[File] = []

    if isinstance(entry, File):
        if entry.size() >= minimum_size:
            large_files.append(entry)
    elif isinstance(entry, Folder):
        for child in entry.children():
            large_files.extend(find_large_files(child, minimum_size))

    return large_files


def walk_tree(entry: Entry, depth: int = 0) -> None:
    """Helper method to visual-print the directory hierarchy."""
    kind = "DIR " if isinstance(entry, Folder) else "FILE"
    indent = "  " * depth
    print(f"{indent}{kind} {entry.name:<18} {entry.size():>8} B   {entry.path_str()}")
    if isinstance(entry, Folder):
        for child in entry.children():
            walk_tree(child, depth + 1)

# Unit Tests Suite
class FileSystemTests(unittest.TestCase):
    """Unit tests verifying composite behaviors, polymorphism, and edge cases."""

    def setUp(self) -> None:
        # Create a 3-level folder structure: root -> docs -> sub
        self.root = Folder("/")
        self.docs = Folder("docs", self.root)
        self.sub = Folder("sub", self.docs)

        self.a = File("a.txt", 100, self.docs)
        self.b = File("b.bin", 5000, self.sub)
        self.c = File("c.log", 20, self.root)

    def test_size_polymorphic(self) -> None:
        self.assertEqual(self.a.size(), 100)
        self.assertEqual(self.sub.size(), 5000)
        self.assertEqual(self.docs.size(), 5100)
        self.assertEqual(self.root.size(), 5120)

    def test_absolute_path_list(self) -> None:
        # Expected contract: List from current -> parent -> root
        path_b = self.b.absolute_path()
        names = [e.name for e in path_b]
        self.assertEqual(names, ["b.bin", "sub", "docs", "/"])

    def test_find_large_files(self) -> None:
        # >= threshold
        self.assertCountEqual(find_large_files(self.root, 50), [self.a, self.b])
        self.assertEqual(find_large_files(self.root, 100), [self.a, self.b])
        self.assertEqual(find_large_files(self.root, 5000), [self.b])
        self.assertEqual(find_large_files(self.root, 5001), [])
        self.assertEqual(find_large_files(self.a, 50), [self.a])
        self.assertEqual(find_large_files(self.a, 200), [])

    def test_empty_folder(self) -> None:
        empty = Folder("empty", self.root)
        self.assertEqual(empty.size(), 0)
        self.assertEqual(find_large_files(empty, 0), [])

    def test_validation_and_errors(self) -> None:
        with self.assertRaises(ValueError):
            File("invalid.bin", -10)
        with self.assertRaises(ValueError):
            Folder("invalid/name")
        with self.assertRaises(ValueError):
            File("a.txt", 50, self.docs) # duplicate name check
        with self.assertRaises(ValueError):
            self.sub.add(self.docs)      # cycle prevention
        with self.assertRaises(TypeError):
            Entry("abstract")            # abstract base class instantiation

    def test_remove(self) -> None:
        self.docs.remove(self.sub)
        self.assertEqual(self.root.size(), 120)
        self.assertIsNone(self.sub.parent())
        self.assertEqual([e.name for e in self.sub.absolute_path()], ["sub"])


# Main Demonstration Function
def main() -> None:
    """Demonstrates requirements (f) and (g) and runs the test suite."""
    print("=" * 65)
    print("FAU ID: Z23348563 - Joseph Majcherek")
    print("Problem 6: Storage System Hierarchy with Polymorphism & Agent Help")
    print("=" * 65)

    # 1. Construct 3-level folder hierarchy (Requirement f)
    root = Folder("root")
    academics = Folder("academics", root)
    cop4045 = Folder("cop4045", academics)

    f_syllabus = File("syllabus.pdf", 250, academics)
    f_hw1 = File("hw1_code.py", 1200, cop4045)
    f_project = File("final_project.zip", 8500, cop4045)

    print("\n--- Folder Hierarchy Structure ---")
    walk_tree(root)

    # Demonstrate polymorphic size() on outer folder
    print(f"\nOuter Folder '{root.name}' Total Size: {root.size()} bytes (250 + 1200 + 8500)")

    # 2. Test find_large_files as two thresholds (Requirement f)
    thresh_1 = 1000
    thresh_2 = 5000
    print(f"\nFiles >= {thresh_1} bytes:")
    for f in find_large_files(root, thresh_1):
        print(f"  * {f.name} ({f.size()} bytes) at {f.path_str()}")

    print(f"\nFiles >= {thresh_2} bytes:")
    for f in find_large_files(root, thresh_2):
        print(f"  * {f.name} ({f.size()} bytes) at {f.path_str()}")

    # 3. Demonstrate absolute_path() (Requirement g)
    print("\n--- Absolute Path Demonstration ---")
    path_nodes = f_project.absolute_path()
    print("f_project.absolute_path() Object Sequence (current -> root):")
    print("  " + " -> ".join([f"[{node.name}]" for node in path_nodes]))

    # 4. Run Unittest Suite (Requirement e)
    print("\n=== Executing Unittest Suite ===")
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(FileSystemTests)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)


if __name__ == "__main__":
    main()