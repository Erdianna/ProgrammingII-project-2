from tkinter import *

def connect_to_db():
    global connect
    global cursor
    connect = sqlite3.connect('cardsgame.db')
    cursor = connect.cursor()

class Card:
    def __init__(self, window):
        self.window = window
        self.window.title("Question")
        self.rootdow_height = 300
        self.rootdow_width = 400
        self.screen_width = self.window.winfo_screenwidth()
        self.screen_height = self.window.winfo_screenheight()
        self.x_cordinate = int((self.screen_width/2) - (self.rootdow_width/2))
        self.y_cordinate = int((self.screen_height/2) - (self.rootdow_height/2))
        self.window.geometry("{}x{}+{}+{}".format(self.rootdow_width, self.rootdow_height, self.x_cordinate, self.y_cordinate))

        # Question label
        self.question = Label(self.window, text="Question")
        self.question.pack()

        # Show answer button
        self.answer_button = Button(self.window, text="Show Answer", command=self.show_answer)
        self.answer_button.pack()

        # Picture
        # self.label = Label(self.window)#, image=binary_pic)
        # self.label.pack()
        # img.place(x=0, y=0)
        self.canvas = Canvas(self.window, width=300, height=300)
        self.canvas.pack()

        # Show answer label


    def show_answer(self):
        connect_to_db()



if __name__ == "__main__":
    Card(Tk())
    mainloop()