import datetime
import enum
import random

from itertools import product

import consts


class State(enum.IntEnum):
    NONE = 0
    CORONA = 1
    NO_CORONA = 2
    NOT_INFECTIOUS = 3


class Speed(enum.IntEnum):
    SLOW = 1
    FAST = 10


StateToColor = {
    State.NONE: consts.BLACK,
    State.CORONA: consts.PINK,
    State.NO_CORONA: consts.BLUE,
    State.NOT_INFECTIOUS: consts.GRAY
}


class Creature:
    def __init__(self, location, state=State.NO_CORONA, speed=0, generation_number_infection=50):
        self.location = location
        self.state = state
        self.speed = speed
        self.generation_number_infection = generation_number_infection

    def move(self):
        x = self.location[0]
        y = self.location[1]
        speed = self.speed
        neighbourhoods_list = [
            (x - speed, y - speed),
            (x, y - speed),
            (x + speed, y - speed),
            (x - speed, y),
            (x, y),
            (x + speed, y),
            (x - speed, y + speed),
            (x, y + speed),
            (x + speed, y + speed)
        ]
        random_num = random.randint(0, 8)
        prev_location = self.location
        self.location = Creature.wrap_around(neighbourhoods_list[random_num])
        return prev_location, self.location

    @staticmethod
    def _neighbours(cell):
        for c in product(*(range(n - 1, n + 2) for n in cell)):
            if c != cell and all(0 <= n < consts.SIZE for n in c):
                yield c

    def infect(self, matrix, infection_rate, sick_count, threshold):
        """
        x x x
        x o x
        x x x
        """
        if not self.sick:
            return

        for neighbour_locations in Creature._neighbours(self.location):
            neighbour = matrix[neighbour_locations[0]][neighbour_locations[1]]
            if neighbour and not neighbour.sick:
                infection_percentage = infection_rate * 100
                probability = random.randint(0, 100)
                if (
                    probability < infection_percentage and
                    self.generation_number_infection and
                    infection_percentage > threshold
                ):
                    neighbour.state = State.CORONA
                    print("[" + datetime.datetime.now().strftime("%H:%M:%S") +
                          "]:\n\tsick count: " + str(sick_count + 1) +
                          "\n\tgeneration of infection: " + str(self.generation_number_infection))

        if self.generation_number_infection > 0:
            self.generation_number_infection -= 1
            if not self.generation_number_infection:
                self.state = State.NOT_INFECTIOUS

    @property
    def sick(self):
        return self.state == State.CORONA

    @staticmethod
    def wrap_around(next_cell):
        next_cell = list(next_cell)

        if next_cell[0] < 0:
            next_cell[0] += consts.SIZE
        elif next_cell[0] > consts.SIZE - 1:
            next_cell[0] -= consts.SIZE

        if next_cell[1] < 0:
            next_cell[1] += consts.SIZE
        elif next_cell[1] > consts.SIZE - 1:
            next_cell[1] -= consts.SIZE

        return next_cell
