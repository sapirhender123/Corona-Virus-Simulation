from tkinter import *
from PIL import ImageTk, Image
root = Tk()

canv = Canvas(root, width=80, height=80, bg='white')
canv.grid(row=2, column=3)

img = ImageTk.PhotoImage(Image.open("corona.png"))  # PIL solution
canv.create_image(20, 20, anchor=NW, image=img)

mainloop()