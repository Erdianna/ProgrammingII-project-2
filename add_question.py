# -*- coding: utf-8 -*-
"""
Created on Sun May  3 22:08:34 2020

@author: Anna
"""

from tkinter import *
import sqlite3
from PIL import ImageTk, Image
from tkinter import filedialog


def connect_to_db():
    global connect
    global cursor
    connect = sqlite3.connect('cardsgame.db')
    cursor = connect.cursor()


class addQuestion:
    def __init__(self, window):
        self.window = window
        self.window.title("Add Question")

        rootdow_height = 470
        rootdow_width = 800
        x_cordinate = int((window.winfo_screenwidth() / 2) - (rootdow_width / 2) - 100)
        y_cordinate = int((window.winfo_screenheight() / 2) - (rootdow_height / 2))
        self.window.geometry(f"{rootdow_width}x{rootdow_height}+{x_cordinate}+{y_cordinate}")

        global entry_add_q
        global entry_answer
        # Add new question
        self.label_q = Label(self.window, text='Add new question')
        self.label_q.grid(row=0, column=0)
        self.entry_q = Entry(self.window, width=70)
        self.entry_q.grid(row=0, column=1)

        self.label_type = Label(self.window, text='Type of question')
        self.label_type.grid(row=1, column=0)

        self.var = StringVar()
        self.radio_open = Radiobutton(self.window, text='Open', variable=self.var, command=self.gui_open, value='open')
        self.radio_open.grid(row=1, column=1)
        self.radio_multiple = Radiobutton(self.window, text='Multiple-choice', variable=self.var,
                                          command=self.gui_multi, value='multiple-choice')
        self.radio_multiple.grid(row=1, column=2)
        self.var.set("open")

        self.label_answer = Label(self.window, text='Correct answer:')
        self.label_answer.grid(row=2, column=0)

        self.entry_answer = Entry(self.window, width=70)
        self.entry_answer.grid(row=2, column=1)

        # binary_pic = ImageTk.PhotoImage(data=pic[0])  # it can display picture based on the binary data
        # # render.resize(100, 200) # (pixels x, pixels y)
        # img = Label(root, image=binary_pic)
        # # img.image = render
        # img.place(x=0, y=0)

        # Save and back button:
        self.save = Button(self.window, text="Save")
        self.save.grid(row=6, column=2, sticky=E + S, ipadx=5)
        # Adding picture button:
        self.pic_button = Button(self.window, text="Add picture", command=self.picture)
        self.pic_button.grid(row=6, column=0)
        # Canvas to place the picture, if added any:
        self.canvas = Canvas(self.window, width=300, height=300)
        self.canvas.grid(row=7, column=1)

    def picture(self):
        filename = filedialog.askopenfilename(title="Select file",
                                              filetypes=(("all files", "*.*"), ("all files", "*.*")))
        img1 = Image.open(filename)
        size = img1.size  # (width, height)
        # let's say i want height to be always 150 -> how the get the rational width?
        x = int((size[0] / size[1]) * 150)  # (width/height)*150
        new_image = img1.resize((x, 150)) # resizing the picture to height of 150 pixels and keeping the original ratio
        new_image.save('temporary.jpg')
        with open('temporary.jpg', 'rb') as file:  # convert digital data to binary format
            binary_pic = file.read()         # this binary_pic is ready to be put in the DB
        # Just displaying picture in tkinter:
        self.img = ImageTk.PhotoImage(new_image, master=self.canvas)
        self.canvas.create_image(20, 20, anchor=NW, image=self.img)
        self.canvas.image = self.img
        binary_pic
    def gui_open(self):
        try:
            self.label_incorrect_1.destroy()
            self.entry_incorrect_1.destroy()
            self.label_incorrect_2.destroy()
            self.entry_incorrect_2.destroy()
            self.label_incorrect_3.destroy()
            self.entry_incorrect_3.destroy()
        except:
            pass

    def gui_multi(self):
        self.label_incorrect_1 = Label(self.window, text='Incorrect answer 1:')
        self.label_incorrect_1.grid(row=3, column=0)
        self.entry_incorrect_1 = Entry(self.window, width=70)
        self.entry_incorrect_1.grid(row=3, column=1)

        self.label_incorrect_2 = Label(self.window, text='Incorrect answer 2:')
        self.label_incorrect_2.grid(row=4, column=0)
        self.entry_incorrect_2 = Entry(self.window, width=70)
        self.entry_incorrect_2.grid(row=4, column=1)

        self.label_incorrect_3 = Label(self.window, text='Incorrect answer 3:')
        self.label_incorrect_3.grid(row=5, column=0)
        self.entry_incorrect_3 = Entry(self.window, width=70)
        self.entry_incorrect_3.grid(row=5, column=1)


if __name__ == "__main__":
    root = Tk()
    add_q = addQuestion(root)
    mainloop()
