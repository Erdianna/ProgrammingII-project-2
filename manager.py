# -*- coding: utf-8 -*-
"""
Created on Sat May  9 17:41:28 2020

@author: Anna
"""

from tkinter import simpledialog, messagebox
from add_question import *
from cat_listbox import *


def connect_to_db():
    global connect
    global cursor
    connect = sqlite3.connect('cardsgame.db')
    cursor = connect.cursor()

def q_listbox_click(event):
    global selected_question
    selected_question = q_listbox.get(q_listbox.curselection())
    # entry.delete(0, END)
    # entry.insert(END, selected)


class Manager:
    def __init__(self, window):
        self.window = window
        self.window.title("Cards Manager")
        rootdow_height = 470
        rootdow_width = 800
        x_cordinate = int((window.winfo_screenwidth() / 2) - (rootdow_width / 2))
        y_cordinate = int((window.winfo_screenheight() / 2) - (rootdow_height / 2))
        self.window.geometry(f"{rootdow_width}x{rootdow_height}+{x_cordinate}+{y_cordinate}")

        # ============= List of CATEGORIES ============= #
        global cat_lb
        cat_lb = CategoriesListbox(self.window)
        cat_lb.GUI_grid()
        cat_lb.cat_listbox.bind("<ButtonRelease-1>", self.load_questions)

        # Add new category (table in db) BUTTON:
        add_cat = Button(self.window, text="Add new", command=self.add_cat)
        add_cat.grid(row=4, column=0, ipadx=5)
        # Delete category (table in db) BUTTON:
        delete_cat = Button(self.window, text="Delete", command=self.delete_cat)
        delete_cat.grid(row=4, column=1, ipadx=5)

        # ============= List of QUESTIONS ============= #
        label_q = Label(self.window, text='Questions in the selected category:')
        label_q.grid(row=0, column=2)
        frame2 = Frame(self.window)
        frame2.grid(row=1, column=2, rowspan=3, columnspan=2)  # takes row 1-2-3
        global q_listbox
        q_listbox = Listbox(frame2, width=40, height=25)
        q_listbox.pack(side="left", fill="both")
        q_listbox.bind("<ButtonRelease-1>", q_listbox_click)  # binding event
        # attaching a scrollbar:
        q_scrollbar = Scrollbar(frame2, orient="vertical")
        q_scrollbar.config(command=q_listbox.yview)
        q_scrollbar.pack(side="right", fill="y")
        q_listbox.config(yscrollcommand=q_scrollbar.set)
        # Add new question button:
        add_q = Button(self.window, text="Add new", command=self.add_q)
        add_q.grid(row=4, column=2, ipadx=5)
        # Delete question button:
        delete_q = Button(self.window, text="Delete", command=self.delete_q)
        delete_q.grid(row=4, column=3, ipadx=5)
        self.back = Button(self.window, text="Back")  # , command=self.window.destroy)
        self.back.grid(row=4, column=4, ipadx=5)  # ipadx is how thick the width of button is

        # self.load_questions()

    # Adding a category (new table in the db):
    def add_cat(self):
        table_name = simpledialog.askstring("Adding new question category",
                                            "Please enter the name of the new category:", parent=self.window)
        table_name = table_name.replace(" ", "_")
        table_name_open = table_name + '_open'
        table_name_multiple = table_name + '_multiple'
        connect_to_db()
        try:
            cursor.execute(f"""CREATE TABLE {table_name}(
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                question TEXT,
                type VARCHAR(8),
                picture BLOB)""")

            cursor.execute(f"""CREATE TABLE {table_name_open}(
                 id INTEGER PRIMARY KEY NOT NULL,
                 answer TEXT)""")

            cursor.execute(f"""CREATE TABLE {table_name_multiple}(
                 id INTEGER PRIMARY KEY NOT NULL,
                 correct_answer TEXT,
                 incorrect_answer_1 TEXT,
                 incorrect_answer_2 TEXT,
                 incorrect_answer_3 TEXT,
                 incorrect_answer_4 TEXT)""")
            connect.commit()
        except sqlite3.OperationalError:
            messagebox.showerror("Error", "A category with this name already exists!")
        connect.close()
        cat_lb.cats_to_listbox()

    # Delete category (table from db)
    def delete_cat(self):
        connect_to_db()
        cursor.execute(f"DROP TABLE {selected_table_name}")  # selected_table_name is globally defined after click
        cursor.execute(f"DROP TABLE {selected_table_name + '_open'}")
        cursor.execute(f"DROP TABLE {selected_table_name + '_multiple'}")
        connect.commit()
        connect.close()
        cat_lb.cats_to_listbox()

    # ============= Functions for Qs within a table ============= #
    def make_question_list(self):
        connect_to_db()
        cursor.execute(f'SELECT * FROM {selected_table_name}')
        all_rows = cursor.fetchall()
        global q_lista
        q_lista = []
        for item in all_rows:
            q_lista.append(item[1])
        connect.close()

    def load_qs_to_listbox(self):  # loading questions from q_lista to the listbox
        q_listbox.delete(0, 'end')
        for line in q_lista:
            q_listbox.insert(END, line)

    def load_questions(self, event):
        global selected_table_name
        selected_table_name = cat_lb.cat_listbox.get(cat_lb.cat_listbox.curselection()).replace(" ", "_")
        self.make_question_list()
        self.load_qs_to_listbox()

    def save_question(self):  # saving OPEN question to the db and going back to the manager GUI
        connect_to_db()
        q = str(add_q.entry_q.get())
        t = add_q.var.get()  # type of Q: open or multiple
        a = str(add_q.entry_answer.get())
        try:
            p = add_q.binary_pic
        except:
            p = ""
        cursor.execute(f"INSERT INTO {selected_table_name} (question, type, picture) VALUES(?, ?, ?)", (q, t, p,))
        cursor.execute(f"SELECT id FROM {selected_table_name} WHERE question =?", (q,))
        id_ = cursor.fetchone()
        cursor.execute(f"INSERT INTO {selected_table_name + '_open'} (id, answer) VALUES(?, ?)", (id_[0], a,))
        connect.commit()
        connect.close()
        add_q.window.destroy()
        self.make_question_list()  # reloading the questions to the listbox
        self.load_qs_to_listbox()

    def add_q(self):  # opening new tkinter window for adding questions (add_question.py)
        root_add_q = Tk()
        global add_q
        add_q = addQuestion(root_add_q)
        add_q.save.configure(command=self.save_question)  # adding command to save question
        # add_q.pic_button.configure(command=self.add_picture) # adding command to upload picture
        mainloop()

    def delete_q(self):
        connect_to_db()
        selected_question = q_listbox.get(q_listbox.curselection())
        # print(selected_question)

        cursor.execute(f"SELECT id FROM {selected_table_name} WHERE question =?", (selected_question,))
        id_ = cursor.fetchone()

        cursor.execute(f"DELETE FROM {selected_table_name} WHERE question=?", (selected_question,))
        cursor.execute(f"DELETE FROM {selected_table_name + '_open'} WHERE id=?", (id_[0],))
        connect.commit()
        connect.close()
        self.make_question_list()
        self.load_qs_to_listbox()


if __name__ == "__main__":
    root = Tk()
    mgr = Manager(root)
    mainloop()
