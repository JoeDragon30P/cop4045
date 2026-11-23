"""
problem 2: Functional programming with Generators, Itertools, Map, Filter, and Reduce
"""

import itertools
import functools
from p1_Majcherek_Joseph import rnd_gen


def gen_rndtup(m):
    """Part a: Infinite generator of (a, b) tuples with 0 <= a <= b < m."""
    gen = rnd_gen(1, -1)
    while True:
        a = next(gen) % m
        b = next(gen) % m
        if a <= b:
            yield (a, b)


def main():
    print("Student: Joseph Majcherek")

    # Part a: sample output of gen_rndtup(10)
    print("\nPart a) First 5 tuples from gen_rndtup(10):")
    print(list(itertools.islice(gen_rndtup(10), 5)))

    # Part b: first 8 tuples from gen_rndtup(10) with a + b >= 6 using filerfalse & islice
    print("\nPart b) First 8 tuples with a + b >= 6 (filterfalse + islice):")
    filtered_b = itertools.filterfalse(lambda t: t[0] + t[1] < 6, gen_rndtup(10))
    res_b = list(itertools.islice(filtered_b, 8))
    print(res_b)

    # Part c: for loop with generator expressions and zip for 0 <= a <= b <= 100
    print("\nPart c) First 8 tuples with 0 <= a <= b <= 100 (zip + generator expression):")
    gen_a = (x % 101 for x in rnd_gen(1, -1))
    gen_b = (y % 101 for y in rnd_gen(2, -1))
    pairs_c = ((a, b) for a, b in zip(gen_a, gen_b) if a <= b)
    for tup in itertools.islice(pairs_c, 8):
        print(tup, end=" ")
    print()

    # Part d: first 10 random numbers between 0 and 100 divisible by 13
    print("\nPart d) First 10 random numbers in [0, 100] divisible by 13:")
    nums_0_100 = map(lambda x: x % 101, rnd_gen(1, -1))
    div_13 = filter(lambda n: n % 13 == 0, nums_0_100)
    res_d = list(itertools.islice(div_13, 10))
    print(res_d)

    # Part e: component-wise sum of first 10 tuples from gen_rndtup(10) with a + b >= 5
    print("\nPart e) Component-wise sum of first 10 tuples with a + b >= 5:")
    valid_e = filter(lambda t: t[0] + t[1] >= 5, gen_rndtup(10))
    first_10_e = list(itertools.islice(map(lambda t: t, valid_e), 10))
    total_e = functools.reduce(lambda acc, t: (acc[0] + t[0], acc[1] + t[1]), first_10_e, (0, 0))
    print("Tuples:", first_10_e)
    print("Component-wise sum:", total_e)


if __name__ == "__main__":
    main()