import math
import random

import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import Label, messagebox

import creature
import consts

root = tk.Tk()
background_image_index = 0

N_var = tk.StringVar()
D_var = tk.StringVar()
R_var = tk.StringVar()
P_var = tk.StringVar()
T_var = tk.StringVar()
X_var = tk.StringVar()

state = {
    'N': 400,
    'D': 2 / 100,
    'R': 2,
    'X': 1,
    'T': 1,
}


def show(matrix):
    resized = cv2.resize(matrix.astype(np.uint8), (1024, 1024))  # Resize image
    cv2.imshow("Press ESC to close the program!", resized)  # Show image
    k = cv2.waitKey(10)
    return k != 27


def init_matrix():
    return np.zeros(shape=(consts.SIZE, consts.SIZE, 3))


def create_creature_locations():
    creature_locations = []
    # create N creatures
    for _ in range(state['N']):
        # TODO fix painting the same cell
        x_of_creature = random.randint(0, consts.SIZE - 1)
        y_of_creature = random.randint(0, consts.SIZE - 1)
        creature_locations.append((x_of_creature, y_of_creature))
    return creature_locations


def paint_cell(matrix, location, cell_state):
    matrix[location[0], location[1]] = creature.StateToColor[cell_state]


def init():
    matrix = init_matrix()
    creature_locations = create_creature_locations()
    for pair in creature_locations:
        paint_cell(matrix, pair, creature.State.NO_CORONA)

    # taking a random subgroup of N, it is our D
    corona_list = random.sample(creature_locations, k=math.floor(state['D'] * state['N']))
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
            speed=creature.Speed.FAST if random.randint(0, 100) <= state['R'] else creature.Speed.SLOW,
            generation_number_infection=state['X'],
        )

    for creature_location in no_corona_list:
        creature_matrix[creature_location[0]][creature_location[1]] = creature.Creature(
            location=creature_location,
            state=creature.State.NO_CORONA,
            speed=creature.Speed.FAST if random.randint(0, 100) <= state['R'] else creature.Speed.SLOW,
            generation_number_infection=state['X'],
        )

    return matrix, creature_matrix


def compare(pair, pair2):
    return (pair[0] == pair2[0]) and (pair[1] == pair2[1])


# NOTE: check if the cell is empty in order that two creatures won't be in the same cell in the same generation.
def is_cell_empty(matrix, next_cell):
    return all(np.equal(matrix[next_cell[0], next_cell[1]], np.asarray(consts.BLACK)))


def run(matrix, creature_matrix):
    sick_corona = []
    while True:
        for i in range(consts.SIZE):
            for j in range(consts.SIZE):
                c = creature_matrix[i][j]
                if not c:
                    continue

                prev, curr = c.move()

                creature_list = [item for sublist in creature_matrix for item in sublist if item]
                sick_list = [c for c in creature_list if c and c.sick]
                sick_corona.append(len(sick_list))
                infection_rate = 1 - len(sick_list) / len(creature_list)
                c.infect(creature_matrix, infection_rate, len(sick_list), state['T'])

                if not compare(prev, curr) and is_cell_empty(matrix, curr):
                    paint_cell(matrix, prev, creature.State.NONE)
                    paint_cell(matrix, curr, c.state)

        if not show(matrix):
            plt.plot([x for x in range(len(sick_corona))], sick_corona)
            plt.title("Number of patients as a function of the time")
            plt.xlabel("Time")
            plt.ylabel("Number of patients")
            plt.show()
            break


def on_resize(event, l, bgimg):
    # resize the background image to the size of label
    image = bgimg.resize((event.width, event.height))
    # update the image of the label

    l.image = ImageTk.PhotoImage(image)
    l.config(image=l.image)


def loadImg(image_name):
    root.geometry('1200x500')
    bgimg = Image.open(image_name)  # load the background image

    bk_label = tk.Label(root)
    bk_label.place(x=0, y=0, relwidth=1, relheight=1)  # make label l to fit the parent window always

    # on_resize will be executed whenever label l is resized
    bk_label.bind('<Configure>', lambda event: on_resize(event, bk_label, bgimg))


def get_label_vals():
    N_str = N_var.get()
    D_str = D_var.get()
    R_str = R_var.get()
    T_str = T_var.get()
    X_str = X_var.get()
    return N_str, D_str, R_str, T_str, X_str


def next():
    global background_image_index

    N_str, D_str, R_str, T_str, X_str = get_label_vals()
    should_swap_image = not any([len(x) != 0 for x in [N_str, D_str, R_str, T_str, X_str]])
    if should_swap_image:
        loadImg(consts.BACKGROUND_IMAGES[background_image_index])
        create_labels()
        background_image_index = (background_image_index + 1) % len(consts.BACKGROUND_IMAGES)
    root.after(3000, next)


def create_labels():
    def submit():
        global state

        try:
            N_str, D_str, R_str, T_str, X_str = get_label_vals()
            global state
            state = {
                'N': int(N_str) if len(N_str) != 0 else 400,
                'D': float(D_str) if len(D_str) else 50 / 100,
                'R': float(R_str) if len(R_str) else 5,
                'T': float(T_str) if len(T_str) else 2,
                'X': float(X_str) if len(X_str) else 50,
            }

            root.destroy()
        except Exception:
            tk.messagebox.showerror(title="Error", message="Please insert a number")

    title_label = tk.Label(root, text='Welcome to our corona simulation!', bg="white", font=('calibre', 20, 'bold'))
    N_label = tk.Label(root, text='Number of creatures', fg="green", bg="white", font=('calibre', 15, 'bold'))
    N_entry = tk.Entry(root, textvariable=N_var, font=('calibre', 15, 'normal'))
    D_label = tk.Label(root, text='Initial percentage of sick creatures', fg="pink", bg = "white",font=('calibre', 15, 'bold'))
    D_entry = tk.Entry(root, textvariable=D_var, font=('calibre', 15, 'normal'))
    R_label = tk.Label(root, text='Percentage of the fast creatures', fg="orange", bg="white", font=('calibre', 15, 'bold'))
    R_entry = tk.Entry(root, textvariable=R_var, font=('calibre', 15, 'normal'))
    T_label = tk.Label(root, text='Threshold', fg="cyan",bg = "white", font=('calibre', 15, 'bold'))
    T_entry = tk.Entry(root, textvariable=T_var, font=('calibre', 15, 'normal'))
    X_label = tk.Label(root, text='Number of generations until recovery', fg="magenta", bg="white", font=('calibre', 15, 'bold'))
    X_entry = tk.Entry(root, textvariable=X_var, font=('calibre', 15, 'normal'))
    sub_btn = tk.Button(root, text='Submit', fg="red", font=('calibre', 15, 'normal'), command=submit)

    title_label.grid(row=0, column=1)
    N_label.grid(row=3, column=1)
    N_entry.grid(row=3, column=2)
    D_label.grid(row=4, column=1)
    D_entry.grid(row=4, column=2)
    R_label.grid(row=5, column=1)
    R_entry.grid(row=5, column=2)
    T_label.grid(row=7, column=1)
    T_entry.grid(row=7, column=2)
    X_label.grid(row=8, column=1)
    X_entry.grid(row=8, column=2)
    sub_btn.grid(row=9, column=2)


def welcome_screen():
    next()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()


def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()


def main():
    welcome_screen()

    matrix, creature_list = init()
    run(matrix, creature_list)


if __name__ == "__main__":
    main()
