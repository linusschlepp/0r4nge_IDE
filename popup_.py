from tkinter import *


class PopUp(Frame):
    def __init__(self, master, list):
        self.list = list
        self.top = Toplevel(master)
        self.top.geometry("750x250")
        self.top.title("Enter name")

        self.variable = StringVar(self.top)
        self.variable.set(list[len(list) - 1])
        self.option_menu = OptionMenu(self.top, self.variable, *list)

        self.label = Label(self.top, text="Enter name of the file, you want to add/rename")
        self.label.pack()
        self.entry = Entry(self.top)
        self.entry.pack()
        self.value = self.entry.get()
        self.button = Button(self.top, text='Ok', command= self.set_close)
        self.lbl_dir = Label(self.top, text="Add to directory")
        self.lbl_dir.pack()
        self.option_menu.pack()
        self.button.pack()

    def set_close(self):
        self.value = self.entry.get()
     #   self.dir_name = self.variable.get()
        self.top.destroy()
