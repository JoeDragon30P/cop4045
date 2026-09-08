def find_dup_str(s, n):
    """
    Determines if s contains a non-overlapping duplicated substring of length n.
    Uses string slicing and avoids the str() function.
    """
    if n <= 0 or n > len(s) // 2:
        return ""

    length = len(s)
    for i in range(length - n + 1):
        sub = s[i : i + n]
        # look for non-overlapping occurrences further down the string
        for j in range(i + n, length - n + 1):
            if s[j : j + n] == sub:
                return sub

    return ""

def find_max_dup(s):
    """
    Finds the longest non-overlapping duplicated substring in s.
    Makes calls to find_dup_str as required.
    """
    max_sub = ""
    # Search from max possible length down to 1
    for length in range(len(s) // 2, 0, -1):
        res = find_dup_str(s, length)
        if res != "":
            return res
    return max_sub

def main():
    # Test for part (a)
    test_str = input("Enter string: ")
    len_str = input("Enter length: ")
    if test_str and len_str:
        n = int(len_str)
        print("Duplicated substring of length", n, ":", find_dup_str(test_str, n))

    # Test for part (b)
    s_max = input("Enter string for max dup: ")
    if s_max:
        print("Longest duplicated substring:", find_max_dup(s_max))

if __name__ == "__main__":
    main()