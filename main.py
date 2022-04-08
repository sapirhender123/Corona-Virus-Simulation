import random

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import math
from matplotlib.pyplot import figure

SIZE = 200
N = 100
D = 50 / 100
# D = random.randint(0, 100)/100
R = 0.1
P = 0.8
T = 0.5
X = 5
BLUE = (0, 0, 255)
PINK = (238, 130, 238)


def show(matrix):
    plt.imshow((matrix).astype(np.uint8))
    plt.show()


def initMatrix():
    # create the matrix
    matrix = np.zeros(shape=(SIZE, SIZE, 3))
    fig = matplotlib.pyplot.gcf()
    fig.set_size_inches(12.5, 7.5)
    return matrix


def createCreatures(matrix):
    listOfPairs = []
    # create N creatures
    for i in range(N):
        # TODO fix painting the same cell
        xOfCreature = random.randint(0, 199)
        yOfCreature = random.randint(0, 199)
        listOfPairs.append((xOfCreature, yOfCreature))
    return listOfPairs


def paintCellPink(matrix, pair):
    matrix[pair[0], pair[1]] = PINK


def paintCellBlue(matrix, pair):
    matrix[pair[0], pair[1]] = BLUE


def init():
    with_corona = int(N * D / 100)
    matrix = initMatrix()
    listOfPairs = createCreatures(matrix)
    # taking a random sub-group of N, it is our D
    coronaList = random.sample(listOfPairs, k=math.floor(D * N))
    # painting in pink the corona sick
    for pair in coronaList:
        paintCellPink(matrix, pair)
    # calculate the rest that doesn't have corona ( noCoronaList = listOfPairs - coronaList )
    noCoronaList = list(set(listOfPairs).difference(set(coronaList)))

    # creating the movement for those who don't have corona (the blue points)
    for pair in noCoronaList:
        next_cell = move_cell(pair[0], pair[1])
        # if the next move isn't to stay in place
        if not compare(next_cell, pair):
            # moving the next generation - those who don't have corona
            matrix[pair[0], pair[1]] = (30, 30, 30)  # paint the current cell in black
            next_cell = BLUE

    for pair in noCoronaList:
        next_cell = move_cell(pair[0], pair[1])
        if not compare(next_cell, pair):
            # moving the next generation - those who have corona
            matrix[pair[0], pair[1]] = (30, 30, 30)
            next_cell = PINK

    show(matrix)


def compare(pair, pair2):
    if (pair[0] == pair2[0]) and (pair[1] == pair2[1]):
        return True
    else:
        return False


def move_cell(x, y):
    neigbrhoodsList = [(x - 1, y - 1), (x, y - 1), (x + 1, y - 1), (x - 1, y), (x, y), (x + 1, y), (x - 1, y + 1),
                       (x, y + 1), (x + 1, y + 1)]
    random_num = random.randint(0, 8)
    return neigbrhoodsList[random_num]


def main():
    init()


if __name__ == "__main__":
    main()
