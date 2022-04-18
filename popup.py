from tkinter import *


class PopUp(Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.top = Toplevel(master)
        self.top.geometry("750x250")
        self.top.title("Enter name")

        self.label = Label(self.top, text="Enter name of the file, you want to add/rename")
        self.label.pack()
        self.entry = Entry(self.top)
        self.entry.pack()
        self.value = self.entry.get()
        self.button = Button(self.top, text='Ok', command=self.set_close)
        self.button.pack()

    def set_close(self):
        self.value = self.entry.get()
        self.top.destroy()




