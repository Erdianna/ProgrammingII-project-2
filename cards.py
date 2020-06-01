# -*- coding: utf-8 -*-
"""
Created on Sun May  3 00:41:34 2020

@author: Anna
"""

import random
from manager import *
from one_card import *
from PIL import ImageTk


class Cards:
    def __init__(self, window):
        self.window = window
        self.window.title("Cards Game")
        rootdow_height = 500
        rootdow_width = 800
        x_cordinate = int((window.winfo_screenwidth() / 2) - (rootdow_width / 2))
        y_cordinate = int((window.winfo_screenheight() / 2) - (rootdow_height / 2))
        self.window.geometry(f"{rootdow_width}x{rootdow_height}+{x_cordinate}+{y_cordinate}")
        
        
        menubar = Menu(self.window)
        file = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file)
        self.window.config(menu=menubar)

        self.tab = []
        self.data = []

        # Adding the choices within the file menu:
        file.add_command(label="New Game", command=self.new_game)
        file.add_command(label="Manager", command=self.open_manager)
        file.add_separator()
        file.add_command(label="Exit", command=self.window.destroy)

        no_of_cards = 30
        self.floors = [i for i in range(1, no_of_cards + 1)]
        self.buttons = {}
        x = 0
        y = 0
        global f
        for floor in self.floors:
            if (y % 6 == 0):  # puts 6 cards in a row
                y = 0
                x = x + 1
            self.buttons[floor] = Button(self.window, width=3, text=str(floor) + ".", bg="#99ccff", font=20,
                                         command=lambda f=floor: self.pressed(f))
            self.buttons[floor].grid(row=x, column=y, padx=15, pady=15, ipadx=25, ipady=12)
            y = y + 1

    def pressed(self, index):
        self.buttons[index].configure(bg="#ff944d")
        self.buttons[index].configure(state=DISABLED)
        item = random.choice(self.data)  # this chooses a tuple with: (id, question, type, picture)
        if item not in self.tab:  # i think this doesnt work now :(
            card = Card(Tk())  # opening the single card window
            card.question.configure(text=item[1])  # item[1] is the question

            # to display the picture too:
            if item[3] == "":
                pass
            else:
                binary_pic = ImageTk.PhotoImage(data=item[3], master=card.canvas)  # master = canvas is important !!!
                card.canvas.create_image(20, 20, anchor=NW, image=binary_pic)
                card.canvas.image = binary_pic

            mainloop()

            self.tab.append(item)
        else:
            self.pressed(index)

    def open_manager(self):
        mgr = Tk()
        global manager
        manager = Manager(mgr)
        manager.back.configure(command=self.back_from_manager)
        mgr.mainloop()

    def back_from_manager(self):
        manager.window.destroy()
        # reloading the questions here somehow?

    def new_game(self):
        for floor in self.floors:
            self.buttons[floor].configure(bg="#99ccff")
            self.buttons[floor].configure(state=NORMAL)
        self.tab = []


if __name__ == "__main__":
    Cards(Tk())
    mainloop()
