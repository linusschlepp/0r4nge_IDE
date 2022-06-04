from tkinter import *

'''
This popup window contains a drop down menu, where the user can select the directories, to add the file to
'''


class PopUp(Frame):
    def __init__(self, master, list_dir):
        self.list = list_dir
        self.top = Toplevel(master)
        self.top.geometry("750x250")
        self.top.title("Enter name")

        self.variable = StringVar(self.top)
        self.variable.set(list_dir[len(list_dir) - 1])
        # dropdown gets filled with the directories
        self.option_menu = OptionMenu(self.top, self.variable, *list_dir)

        self.label = Label(self.top, text="Enter name of the file/ directory, you want to add/rename")
        self.label.pack()
        self.entry = Entry(self.top)
        self.entry.pack()
        self.value = self.entry.get()
        self.button = Button(self.top, text='Ok', command=self.set_close)
        self.lbl_dir = Label(self.top, text="Add to directory?")
        self.lbl_dir.pack()
        self.option_menu.pack()
        self.button.pack()

    def set_close(self):
        self.value = self.entry.get()
        self.top.destroy()
