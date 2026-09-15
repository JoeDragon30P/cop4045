"""Problem 3: Social Network Operations.

Manages network links using nested dictionaries, lists, and tuples, complete
with CSV persistence and unit test extra credit
"""

from typing import Dict, Tuple, List, Set
import csv
import sys

def add_user(sn: Dict[str, Tuple[str, List[str]]], username: str, fullname: str) -> bool:
    """Add a new user to the social network with an empty friend list."""
    try:
        if username in sn:
            return False
        sn[username] = (fullname, [])
        return True
    except Exception as err:
        print(f"[ERROR] Failed in add_user: {err}")
        raise


def add_friend(sn: Dict[str, Tuple[str, List[str]]], user1: str, user2: str) -> bool:
    """Establish a mutual friend relationship between user1 and user2."""
    try:
        if user1 not in sn or user2 not in sn or user1 == user2:
            return False

        fname1, flist1 = sn[user1]
        fname2, flist2 = sn[user2]

        if user2 not in flist1:
            flist1.append(user2)
        if user1 not in flist2:
            flist2.append(user1)

        return True
    except Exception as err:
        print(f"[ERROR] Failed in add_friend: {err}")
        raise

def get_friends(sn: Dict[str, Tuple[str, List[str]]], user1: str, distance: int) -> List[str]:
    """Retrieve all friends within a specified link distance using BFS traversal."""
    try:
        if user1 not in sn or distance < 1:
            return []

        visited = {user1}
        current_layer = {user1}

        for _ in range(distance):
            next_layer = set()
            for curr in current_layer:
                _, friends = sn[curr]
                for f in friends:
                    if f not in visited:
                        visited.add(f)
                        next_layer.add(f)
            current_layer = next_layer
            if not current_layer:
                break

        visited.remove(user1)
        return list(visited)
    
    except Exception as err:
        print(f"[ERROR] Failed in get_friends: {err}")
        raise

def save_network(filename: str, sn: Dict[str, Tuple[str, List[str]]]) -> None:
    """Save social network structure into a CSV file."""
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as outfile:
            writer = csv.writer(outfile)
            for uname, (fname, flist) in sn.items():
                writer.writerow([uname, fname, ",".join(flist)])
    except Exception as err:
        print(f"[ERROR] Could not save network to '{filename}': {err}")
        raise

def load_network(filename: str) -> Dict[str, Tuple[str, List[str]]]:
    """Load social network structure from a CSV file."""
    try:
        sn = {}
        with open(filename, 'r', encoding='utf-8') as infile:
            reader = csv.reader(infile)
            for row in reader:
                if not row:
                    continue
                uname = row[0]
                fname = row[1]
                flist = row[2].split(",") if len(row) > 2 and row[2] else []
                sn[uname] = (fname, flist)
        return sn
    except Exception as err:
        print(f"[ERROR] Could not load network from '{filename}': {err}")
        raise

def test_extra_credit() -> None:
    """Extra Credit Test Suite (Module 2 testif emulation)."""
    print("\n--- Running Extre Credit Tests ---")

    def testif(cond: bool, test_name: str) -> None:
        status = "PASSED" if cond else "FAILED"
        print(f"Test [{test_name}]: {status}")

    net = {}
    testif(add_user(net, "alice", "Alice Smith"), "Add Alice")
    testif(add_user(net, "maria", "Maria Cortez"), "Add Maria")
    testif(not add_user(net, "alice", "Duplicate Alice"), "Reject Duplicate Alice")

    testif(add_friend(net, "alice", "maria"), "Link Alice-Maria")
    testif("maria" in net["alice"][1] and "alice" in net["maria"][1], "Verify Mutual Link")

    f_dist1 = get_friends(net, "alice", 1)
    testif(f_dist1 == ["maria"], "Distance 1 Friends")

import os
import tempfile

def main() -> None:
    """Main function to demonstrate social network functionality."""
    network = {
        'alice': ('Alice Smith', ['maria']),
        'maria': ('Maria Cortez', ['alice', 'joe', 'david']),
        'joe': ('Joseph Adams', ['maria', 'eve']),
        'eve': ('Evelyn Cooper', ['joe']),
        'david': ('David Benson', ['maria'])
    }

    print("Initial Alice Friends (Dist 1):", get_friends(network, "alice", 1))
    print("Initial Alice Friends (Dist 2):", get_friends(network, "alice", 2))

    # Test saving & loading network
    csv_file = os.path.join(tempfile.gettempdir(), "social_network.csv")
    save_network(csv_file, network)
    reloaded_net = load_network(csv_file)

    print("Reloaded Network Match:", reloaded_net == network)

    # Execute extra credit
    test_extra_credit()

if __name__ == "__main__":
    main()