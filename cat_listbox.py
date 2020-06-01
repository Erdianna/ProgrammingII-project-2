# -*- coding: utf-8 -*-
"""
Created on Wed May 13 18:08:23 2020

@author: Anna

List of categories
"""

from tkinter import *
import sqlite3


def connect_to_db():
    global connect
    global cursor
    connect = sqlite3.connect('cardsgame.db')
    cursor = connect.cursor()


class CategoriesListbox:
    def __init__(self, window):
        self.window = window
        self.label_cat = Label(self.window, text='Categories:')
        self.frame = Frame(self.window)
        self.cat_listbox = Listbox(self.frame, width=40, height=25)
        self.cat_listbox.pack(side="left", fill="both")
        self.cat_listbox.bind("<ButtonRelease-1>", self.click)  # binding event
        # attaching a scrollbar:
        self.cat_scrollbar = Scrollbar(self.frame, orient="vertical")
        self.cat_scrollbar.config(command=self.cat_listbox.yview)
        self.cat_scrollbar.pack(side="right", fill="y")
        self.cat_listbox.config(yscrollcommand=self.cat_scrollbar.set)
        # loading categories:
        self.cats_to_listbox()

    def GUI_pack(self):
        self.label_cat.pack()
        self.frame.pack()

    def GUI_grid(self):
        self.label_cat.grid(row=0, column=0)
        self.frame.grid(row=1, column=0, rowspan=3, columnspan=2)  # takes row 1-2-3

    def load_cats(self):  # loading tables from the db
        connect = sqlite3.connect('cardsgame.db')
        cursor = connect.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        global tables_list
        tables_list = []
        for item in tables:
            tables_list.append(item[0])
        connect.close()

    def cats_to_listbox(self):
        self.cat_listbox.delete(0, 'end')
        self.load_cats()
        for line in tables_list:
            if '_open' in line or '_multiple' in line or 'sqlite_sequence' in line:
                next
            else:
                line = line.replace("_", " ")
                self.cat_listbox.insert(END, line)

    def click(self, event):  # returns the selected table name
        self.selected = self.cat_listbox.get(self.cat_listbox.curselection()).replace(" ", "_")
        connect_to_db()
        cursor.execute(f"SELECT * FROM {self.selected}")
        t0 = cursor.fetchall()
        self.lista = []
        for item in t0:
            self.lista.append(item[1])
        connect.close()


if __name__ == "__main__":
    root = Tk()
    CategoriesListbox(root).GUI_pack()
    root.mainloop()
