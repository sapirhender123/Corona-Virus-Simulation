import random
import numpy as np
import math
import cv2

import creature
import consts


def show(matrix):
    cv2.namedWindow("output", cv2.WINDOW_NORMAL)  # Create window with freedom of dimensions
    resized = cv2.resize(matrix.astype(np.uint8), (3000, 3000))  # Resize image
    cv2.imshow("output", resized)  # Show image
    cv2.waitKey(10)


def init_matrix():
    # create the matrix
    matrix = np.zeros(shape=(consts.SIZE, consts.SIZE, 3))
    return matrix


def create_creature_locations():
    creature_locations = []
    # create N creatures
    for i in range(consts.N):
        # TODO fix painting the same cell
        x_of_creature = random.randint(0, consts.SIZE - 1)
        y_of_creature = random.randint(0, consts.SIZE - 1)
        creature_locations.append((x_of_creature, y_of_creature))
    return creature_locations


def paint_cell(matrix, location, state):
    matrix[location[0], location[1]] = creature.StateToColor[state]


def init():
    matrix = init_matrix()
    creature_locations = create_creature_locations()
    for pair in creature_locations:
        paint_cell(matrix, pair, creature.State.NO_CORONA)

    # taking a random subgroup of N, it is our D
    corona_list = random.sample(creature_locations, k=math.floor(consts.D * consts.N))
    # painting in pink the corona sick
    for pair in corona_list:
        paint_cell(matrix, pair, creature.State.CORONA)

    # calculate the rest that doesn't have corona ( noCoronaList = listOfPairs - coronaList )
    no_corona_list = list(set(creature_locations).difference(set(corona_list)))

    R = 10

    creature_matrix = [[0 for x in range(200)] for y in range(200)]
    for creature_location in corona_list:
        creature_matrix[creature_location[0]][creature_location[1]] = creature.Creature(
            location=creature_location,
            state=creature.State.CORONA,
            speed=creature.Speed.FAST if random.randint(0, 100) <= R else creature.Speed.SLOW
        )

    for creature_location in no_corona_list:
        creature_matrix[creature_location[0]][creature_location[1]] = creature.Creature(
            location=creature_location,
            state=creature.State.NO_CORONA,
            speed=creature.Speed.FAST if random.randint(0, 100) <= R else creature.Speed.SLOW
        )

    return matrix, creature_matrix


def compare(pair, pair2):
    return (pair[0] == pair2[0]) and (pair[1] == pair2[1])


def is_cell_empty(matrix, next_cell):
    return all(np.equal(matrix[next_cell[0], next_cell[1]], np.asarray(consts.BLACK)))


def run(matrix, creature_matrix):
    while True:
        for i in range(200):
            for j in range(200):
                c = creature_matrix[i][j]
                if not c:
                    continue

                prev, curr = c.move()

                creature_list = [item for sublist in creature_matrix for item in sublist if item]
                sick_list = [c for c in creature_list if c and c.sick]
                infection_rate = 1 - len(sick_list)/len(creature_list)
                c.infect(creature_matrix, infection_rate, len(sick_list))

                if not compare(prev, curr) and is_cell_empty(matrix, curr):
                    paint_cell(matrix, prev, creature.State.NONE)
                    paint_cell(matrix, curr, c.state)

        show(matrix)


def main():
    matrix, creature_list = init()
    run(matrix, creature_list)


if __name__ == "__main__":
    main()
