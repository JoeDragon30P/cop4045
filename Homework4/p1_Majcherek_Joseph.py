"""
Problem 1: The Linear Congruential generator (Iterator & Generator)
"""

class RndSeq:
    """Iterator class that generates n pseudo-random numbers from seed x0."""

    def __init__(self, x0, n):
        self.m = 2 ** 32
        self.a = 22695477
        self.c = 1
        self.current = x0
        self.n = n
        self.count = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.n >= 0 and self.count >= self.n:
            raise StopIteration
        self.current = (self.a * self.current + self.c) % self.m
        self.count += 1
        return self.current

def rnd_gen(x0, n):
    """Generator yielding n pseudo-random numbers (or infinite if n < 0)."""
    m = 2 ** 32
    a = 22695477
    c = 1
    current = x0
    count = 0

    while n < 0 or count < n:
        current = (a * current + c) % m
        count += 1
        yield current


def main():
    print("Student: Joseph Majcherek")
    # Demonstrate class and generator with seed 2 and 10 numbers
    class_nums = [num for num in RndSeq(2, 10)]
    gen_nums = list(rnd_gen(2, 10))

    print("RndSeq(2, 10) :", class_nums)
    print("rnd_gen(2, 10):", gen_nums)


if __name__ == "__main__":
    main()