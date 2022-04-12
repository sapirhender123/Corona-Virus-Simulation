import random

import matplotlib.pyplot as plt
import numpy as np
import math
import cv2
import creature
import consts
import tkinter as tk


def show(matrix):
    resized = cv2.resize(matrix.astype(np.uint8), (3000, 3000))  # Resize image
    cv2.imshow("Press ESC to close the program!", resized)  # Show image
    k = cv2.waitKey(10)
    if k == 27:
        return False
    return True


def init_matrix():
    # create the matrix
    matrix = np.zeros(shape=(consts.SIZE, consts.SIZE, 3))
    return matrix


def create_creature_locations():
    creature_locations = []
    # create N creatures
    for i in range(N):
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
    corona_list = random.sample(creature_locations, k=math.floor(D * N))
    # painting in pink the corona sick
    for pair in corona_list:
        paint_cell(matrix, pair, creature.State.CORONA)

    # calculate the rest that doesn't have corona ( noCoronaList = listOfPairs - coronaList )
    no_corona_list = list(set(creature_locations).difference(set(corona_list)))

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
    sick_corona = []
    while True:
        for i in range(200):
            for j in range(200):
                c = creature_matrix[i][j]
                if not c:
                    continue

                prev, curr = c.move()

                creature_list = [item for sublist in creature_matrix for item in sublist if item]
                sick_list = [c for c in creature_list if c and c.sick]
                sick_corona.append(len(sick_list))
                infection_rate = 1 - len(sick_list) / len(creature_list)
                c.infect(creature_matrix, infection_rate, len(sick_list))

                if not compare(prev, curr) and is_cell_empty(matrix, curr):
                    paint_cell(matrix, prev, creature.State.NONE)
                    paint_cell(matrix, curr, c.state)
        # check for esc
        if not show(matrix):
            plt.plot([x for x in range(len(sick_corona))], sick_corona)
            plt.show()
            break


def welcome_screen():
    root = tk.Tk()
    root.title("Corona Virus Simulation Inputs")
    root.geometry("1000x300")
    from PIL import ImageTk, Image

    canv = tk.Canvas(root, width=1000, height=300)

    img = ImageTk.PhotoImage(Image.open("corona.png"))
    canv.create_image(9999, 1111, image=img)

    N_var = tk.StringVar()
    D_var = tk.StringVar()
    R_var = tk.StringVar()
    P_var = tk.StringVar()
    T_var = tk.StringVar()
    X_var = tk.StringVar()

    def submit():
        global N, D, R, P, T, X
        N = int(N_var.get()) if len(N_var.get()) != 0 else 100
        D = float(D_var.get()) if len(D_var.get()) else 50 / 100
        R = float(R_var.get()) if len(R_var.get()) else 10
        P = float(P_var.get()) if len(P_var.get()) else 0.8
        T = float(T_var.get()) if len(T_var.get()) else 0.5
        X = float(X_var.get()) if len(X_var.get()) else 5
        root.destroy()

    title_lable = tk.Label(root, text='Please enter only numbers', font=('calibre', 20, 'bold'))
    N_lable = tk.Label(root, text='Creatures Amount', font=('calibre', 20, 'bold'))
    N_entry = tk.Entry(root, textvariable=N_var, font=('calibre', 20, 'normal'))
    D_lable = tk.Label(root, text='Percentage of sick creatures', font=('calibre', 20, 'bold'))
    D_entry = tk.Entry(root, textvariable=D_var, font=('calibre', 20, 'normal'))
    R_lable = tk.Label(root, text='Percentage of creatures moving fast', font=('calibre', 20, 'bold'))
    R_entry = tk.Entry(root, textvariable=R_var, font=('calibre', 20, 'normal'))
    P_lable = tk.Label(root, text='The chance of infection', font=('calibre', 20, 'bold'))
    P_entry = tk.Entry(root, textvariable=P_var, font=('calibre', 20, 'normal'))
    T_lable = tk.Label(root, text='Threshold', font=('calibre', 20, 'bold'))
    T_entry = tk.Entry(root, textvariable=T_var, font=('calibre', 20, 'normal'))
    X_lable = tk.Label(root, text='Number of generations until recovery', font=('calibre', 20, 'bold'))
    X_entry = tk.Entry(root, textvariable=X_var, font=('calibre', 20, 'normal'))
    sub_btn = tk.Button(root, text='Submit', font=('calibre', 20, 'normal'), command=submit)

    title_lable.grid(row =0, column=2)
    N_lable.grid(row=1, column=1)
    N_entry.grid(row=1, column=3)
    D_lable.grid(row=2, column=1)
    D_entry.grid(row=2, column=3)
    R_lable.grid(row=3, column=1)
    R_entry.grid(row=3, column=3)
    P_lable.grid(row=4, column=1)
    P_entry.grid(row=4, column=3)
    T_lable.grid(row=5, column=1)
    T_entry.grid(row=5, column=3)
    X_lable.grid(row=6, column=1)
    X_entry.grid(row=6, column=3)
    sub_btn.grid(row=7, column=2)

    root.mainloop()


def main():
    welcome_screen()
    print(N, D, R, P, T, X)
    matrix, creature_list = init()
    run(matrix, creature_list)


if __name__ == "__main__":
    main()
