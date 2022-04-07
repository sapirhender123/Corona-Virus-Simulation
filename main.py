import random
import matplotlib.pyplot as plt
import numpy as np
import math

SIZE = 200
N = 30
D = random.randint(0, 100)/100
R = 0.1
P = 0.8
T = 0.5
X = 5

def init():
    matrix = np.zeros(shape=(SIZE, SIZE, 3))
    with_corona = int(N*D/100)
    listOfPairs = []
    # N creatures

    for i in range(N):
        # TODO fix painting the same cell
        x = random.randint(0, 199)
        y = random.randint(0, 199)
        listOfPairs.append((x,y))
        matrix[x,y] = (0,0,255)
    coronaList = random.sample(listOfPairs, k = math.floor(D*N))
    # white - have corona
    for pair in coronaList:
        matrix[pair[0], pair[1]] = (238, 130, 238)

    for pair in listOfPairs:
        # if the next move is to stay in place
        if move_cell(pair) != pair:
            matrix[pair[0], pair[1]] = (30, 30, 30)


    plt.imshow(matrix)
    plt.show()

def move_cell(x,y):
    neigbrhoodsList = [(x-1,y-1), (x,y-1), (x+1, y-1), (x-1,y),(x,y), (x+1,y), (x-1,y+1),(x,y+1), (x+1,y+1)]
    random_num = random.randint(0,8)
    return neigbrhoodsList[random_num]

def main():
    init()

if __name__ == "__main__":
    main()