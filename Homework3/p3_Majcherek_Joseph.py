"""
Problem 3: Extended Predator-Prey Simulation with Human Dynamics
"""

import random
import matplotlib.pyplot as plt
from typing import Tuple, List, Optional, Any


class Island:
    """Represents a 2D grid world inhabited by Animals."""

    def __init__(self, n: int, prey_count: int = 0, predator_count: int = 0, human_count: int = 0) -> None:
        self.grid_size: int = n
        self.grid: List[List[Any]] = [[0] * n for _ in range(n)]
        self.init_animals(prey_count, predator_count, human_count)

    def init_animals(self, prey_count: int, predator_count: int, human_count: int) -> None:
        """Places initial animals randomly across open grid spaces."""
        for species_class, count in [(Prey, prey_count), (Predator, predator_count), (Human, human_count)]:
            c = 0
            while c < count:
                x = random.randint(0, self.grid_size - 1)
                y = random.randint(0, self.grid_size - 1)
                if not self.animal(x, y):
                    new_animal = species_class(island=self, x=x, y=y)
                    self.register(new_animal)
                    c += 1

    def clear_all_moved_flags(self) -> None:
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                if self.grid[x][y]:
                    self.grid[x][y].clear_moved_flag()

    def size(self) -> int:
        return self.grid_size

    def register(self, animal: Any) -> None:
        self.grid[animal.x][animal.y] = animal

    def remove(self, animal: Any) -> None:
        self.grid[animal.x][animal.y] = 0

    def animal(self, x: int, y: int) -> Any:
        if 0 <= x < self.grid_size and 0 <= y < self.grid_size:
            return self.grid[x][y]
        return -1

    def __str__(self) -> str:
        s = ""
        for j in range(self.grid_size - 1, -1, -1):
            for i in range(self.grid_size):
                if not self.grid[i][j]:
                    s += ". "
                else:
                    s += f"{str(self.grid[i][j])} "
            s += "\n"
        return s
    
    def count_prey(self) -> int:
        return sum(1 for x in range(self.grid_size) for y in range(self.grid_size) if isinstance(self.grid[x][y], Prey))

    def count_predators(self) -> int:
        return sum(1 for x in range(self.grid_size) for y in range(self.grid_size) if isinstance(self.grid[x][y], Predator))

    def count_humans(self) -> int:
        return sum(1 for x in range(self.grid_size) for y in range(self.grid_size) if isinstance(self.grid[x][y], Human))


class Animal:
    """Base class for island entities."""

    breed_time: int = 0

    def __init__(self, island: Island, x: int = 0, y: int = 0, s: str = "A") -> None:
        self.island: Island = island
        self.name: str = s
        self.x: int = x
        self.y: int = y
        self.moved: bool = False
        self.breed_clock: int = self.breed_time

    def __str__(self) -> str:
        return self.name

    def check_grid(self, type_looking_for: Any = int) -> Any:
        offset = [(-1, 1), (0, 1), (1, 1), (-1, 0), (1, 0), (-1, -1), (0, -1), (1, -1)]
        for dx, dy in offset:
            x, y = self.x + dx, self.y + dy
            if 0 <= x < self.island.size() and 0 <= y < self.island.size():
                target = self.island.animal(x, y)
                if type_looking_for == int and target == 0:
                    return (x, y)
                elif type_looking_for != int and isinstance(target, type_looking_for):
                    return (x, y)
        return 0

    def move(self) -> None:
        if not self.moved:
            location = self.check_grid(int)
            if location:
                self.island.remove(self)
                self.x, self.y = location
                self.island.register(self)
                self.moved = True

    def breed(self) -> None:
        if self.breed_clock <= 0:
            location = self.check_grid(int)
            if location:
                self.breed_clock = self.breed_time
                new_animal = self.__class__(self.island, x=location[0], y=location[1])
                self.island.register(new_animal)

    def clear_moved_flag(self) -> None:
        self.moved = False


class Prey(Animal):
    def __init__(self, island: Island, x: int = 0, y: int = 0, s: str = "O") -> None:
        super().__init__(island, x, y, s)

    def clock_tick(self) -> None:
        self.breed_clock -= 1

class Predator(Animal):
    starve_time: int = 0

    def __init__(self, island: Island, x: int = 0, y: int = 0, s: str = "X") -> None:
        super().__init__(island, x, y, s)
        self.starve_clock: int = self.starve_time

    def clock_tick(self) -> None:
        self.breed_clock -= 1
        self.starve_clock -= 1
        if self.starve_clock <= 0:
            self.island.remove(self)

    def eat(self) -> None:
        if not self.moved:
            location = self.check_grid(Prey)
            if location:
                self.island.remove(self.island.animal(location[0], location[1]))
                self.island.remove(self)
                self.x, self.y = location
                self.island.register(self)
                self.starve_clock = self.starve_time
                self.moved = True


class Human(Animal):
    """
    Human class inheriting from Animal. Hunts Predators, starves, and breeds
    """

    hunt_time: int = 1
    starve_time: int = 0

    def __init__(self, island: Island, x: int = 0, y: int = 0, s: str = "H") -> None:
        super().__init__(island, x, y, s)
        self.starve_clock: int = self.starve_time
        self.hunt_clock: int = self.hunt_time

    def clock_tick(self) -> None:
        self.breed_clock -= 1
        self.starve_clock -= 1
        self.hunt_clock -= 1
        if self.starve_clock <= 0:
            self.island.remove(self)

    def hunt(self) -> None:
        """Hunts Predators periodically based on hunt_time."""
        if not self.moved and self.hunt_clock <= 0:
            location = self.check_grid(Predator)
            if location:
                self.island.remove(self.island.animal(location[0], location[1]))
                self.island.remove(self)
                self.x, self.y = location
                self.island.register(self)
                self.starve_clock = self.starve_time
                self.hunt_clock = self.hunt_time
                self.moved = True


def main(predator_breed_time: int = 6, predator_starve_time: int = 3, initial_predators: int = 10,
         prey_breed_time: int = 3, initial_prey: int = 50,
         human_breed_time: int = 8, human_starve_time: int = 5, human_hunt_time: int = 2, initial_humans: int = 5,
         size: int = 12, ticks: int = 300) -> None:
    """Simulation driver containing Humans, Predators, and Prey."""
    Predator.breed_time = predator_breed_time
    Predator.starve_time = predator_starve_time
    Prey.breed_time = prey_breed_time
    Human.breed_time = human_breed_time
    Human.starve_time = human_starve_time
    Human.hunt_time = human_hunt_time

    predator_list, prey_list, human_list = [], [], []

    isle = Island(size, initial_prey, initial_predators, initial_humans)
    print("Initial Island Grid State:")
    print(isle)

    for i in range(ticks):
        isle.clear_all_moved_flags()
        for x in range(size):
            for y in range(size):
                animal = isle.animal(x, y)
                if animal:
                    if isinstance(animal, Human):
                        animal.hunt()
                    elif isinstance(animal, Predator):
                        animal.eat()
                    animal.move()
                    animal.breed()
                    animal.clock_tick()

        prey_cnt = isle.count_prey()
        pred_cnt = isle.count_predators()
        hum_cnt = isle.count_humans()

        prey_list.append(prey_cnt)
        predator_list.append(pred_cnt)
        human_list.append(hum_cnt)

        # Check population extinction / convergence stop conditions
        if (prey_cnt == 0 and pred_cnt == 0) or (i > 10 and prey_list[-10:] == prey_list[-1:] and predator_list[-10:] == predator_list[-1:] and human_list[-10:] == human_list[-1:]):
            print(f"Simulation ended early at tick {i} due to stability/extinction.")
            break

    print("\nFinal Island Grid State:")
    print(isle)

    plt.plot(prey_list, label="Prey")
    plt.plot(predator_list, label="Predators")
    plt.plot(human_list, label="Humans")
    plt.title("Island Species Population Dynamics")
    plt.xlabel("Clock Ticks")
    plt.ylabel("Population")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()