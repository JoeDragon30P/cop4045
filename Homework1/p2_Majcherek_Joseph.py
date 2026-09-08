def find_Pythagorean(n):
    """
    Find all Pythagorean triples (a, b, c) where 0 < a, b, c <= n.
    """
    triples = []
    for a in range(1, n + 1):
        for b in range(1, n + 1):
            for c in range(1, n + 1):
                if a**2 + b**2 == c**2:
                    triples.append((a, b, c))
    return triples

def main():
    n_str = input("Enter integer n: ")
    if n_str:
        n = int(n_str)
        results = find_Pythagorean(n)
        print(f"Pythagorean triples up to {n}:")
        for triple in results:
            print(triple)

if __name__ == "__main__":
    main()