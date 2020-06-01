# -*- coding: utf-8 -*-
"""
Created on Sat May  2 19:42:29 2020

@author: Anna
"""

from cards import *
from manager import *

def connect_to_db():
    global connect
    global cursor
    connect = sqlite3.connect('cardsgame.db')
    cursor = connect.cursor()


class CardsGame:
    def __init__(self, window):
        self.window = window
        self.window.title("Cards Game")
        rootdow_height = 560
        rootdow_width = 450
        x_cordinate = int((window.winfo_screenwidth() / 2) - (rootdow_width / 2))
        y_cordinate = int((window.winfo_screenheight() / 2) - (rootdow_height / 2))
        self.window.geometry(f"{rootdow_width}x{rootdow_height}+{x_cordinate}+{y_cordinate}")
        # ================================================================================ #
        self.label_1 = Label(window, text="Welcome to the game!\n\n"
                                          "Choose the category of cards you want to play with:")
        self.label_1.pack()

        # List of categories from cat_listbox.py:
        global ctg_lb
        ctg_lb = CategoriesListbox(window)
        ctg_lb.GUI_pack()
        # Play button
        button_1 = Button(window, text="Play", command=self.open_cards)
        button_1.pack()
        # Manager button:
        button_2 = Button(window, text="Cards Manager", command=self.open_manager)
        button_2.pack()

    def open_manager(self):
        mgr = Tk()
        global manager
        manager = Manager(mgr)
        manager.back.configure(command=self.back_from_manager)
        mgr.mainloop()

    def back_from_manager(self):
        manager.window.destroy()
        ctg_lb.cats_to_listbox() # reloading the categories listbox

    def open_cards(self):
        self.window.destroy()
        cards = Cards(Tk()) # cards is the window with the blue cubes
        # cards.lista = ctg_lb.lista # this list contains only the a list of the question
        # but i also need to get the picture and answer to the questions -> how?
        cards.selected_table_name = ctg_lb.selected # name of the table

        connect_to_db()
        cursor.execute(f"SELECT * FROM {ctg_lb.selected}")
        cards.data = cursor.fetchall() # data is a list of lists
        # data looks like: [(1, 'question1', 'open', b'\xff\xd8\x..), (2, 'question2', 'open', b'\xff\xd8\xff), ...]
        #print(cards.data)
        mainloop()


if __name__ == "__main__":
    root = Tk()
    start_GUI = CardsGame(root)
    root.mainloop()
