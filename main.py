import random
import numpy as np
import math
import cv2

SIZE = 200
N = 100
D = 50 / 100
# D = random.randint(0, 100)/100
R = 0.1
P = 0.8
T = 0.5
X = 5
BLUE = (255, 0, 0)
PINK = (238, 130, 238)
BLACK = (0, 0, 0)


def show(matrix):
    cv2.namedWindow("output", cv2.WINDOW_NORMAL)  # Create window with freedom of dimensions
    resized = cv2.resize(matrix.astype(np.uint8), (3000, 3000))  # Resize image
    cv2.imshow("output", resized)  # Show image
    cv2.waitKey(300)


def init_matrix():
    # create the matrix
    matrix = np.zeros(shape=(SIZE, SIZE, 3))
    return matrix


def create_creatures():
    list_of_pairs = []
    # create N creatures
    for i in range(N):
        # TODO fix painting the same cell
        x_of_creature = random.randint(0, 199)
        y_of_creature = random.randint(0, 199)
        list_of_pairs.append((x_of_creature, y_of_creature))
    return list_of_pairs


def paint_cell_pink(matrix, pair):
    matrix[pair[0], pair[1]] = PINK


def paint_cell_blue(matrix, pair):
    matrix[pair[0], pair[1]] = BLUE


def init():
    while True:
        # with_corona = int(N * D / 100)
        matrix = init_matrix()
        list_of_pairs = create_creatures()
        for pair in list_of_pairs:
            paint_cell_blue(matrix, pair)

        # taking a random subgroup of N, it is our D
        corona_list = random.sample(list_of_pairs, k=math.floor(D * N))
        # painting in pink the corona sick
        for pair in corona_list:
            paint_cell_pink(matrix, pair)

        # calculate the rest that doesn't have corona ( noCoronaList = listOfPairs - coronaList )
        no_corona_list = list(set(list_of_pairs).difference(set(corona_list)))

        # creating the movement for those who don't have corona (the blue points)
        for pair in no_corona_list:
            next_cell = move_cell(pair[0], pair[1])
            # if the next move isn't to stay in place
            if not compare(next_cell, pair):
                # moving the next generation - those who don't have corona
                matrix[pair[0], pair[1]] = BLACK  # paint the current cell in black
                paint_cell_blue(matrix, next_cell)

        for pair in corona_list:
            next_cell = move_cell(pair[0], pair[1])
            if not compare(next_cell, pair):
                # moving the next generation - those who have corona
                matrix[pair[0], pair[1]] = (0, 0, 0)
                # next_cell = PINK

        show(matrix)


def compare(pair, pair2):
    if (pair[0] == pair2[0]) and (pair[1] == pair2[1]):
        return True
    else:
        return False


def move_cell(x, y):
    neighbourhoods_list = [(x - 1, y - 1), (x, y - 1), (x + 1, y - 1), (x - 1, y), (x, y), (x + 1, y), (x - 1, y + 1),
                           (x, y + 1), (x + 1, y + 1)]
    random_num = random.randint(0, 8)
    return neighbourhoods_list[random_num]


def main():
    init()


if __name__ == "__main__":
    main()
