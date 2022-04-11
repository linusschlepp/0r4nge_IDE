import os
import subprocess
from tkinter import *
from tkinter.filedialog import *
from tkinter.ttk import *
from pathlib import Path


# def select_file():
#     file = open('currentFile.txt', 'w')
#     file_name = askopenfilename()
#     try:
#         file.write(str(Path(file_name.name)))
#     except AttributeError:
#         pass
#     file.close()
#     my_win.t3.insert(1.0, "")


def new_file():
    file = open('currentFile.txt', 'w')
    file_name = asksaveasfile(mode='r', defaultextension=".py")
    try:
        file.write(str(Path(file_name.name)))
    except AttributeError:
        pass
    file.close()


def create_file(file_content):
    file = open(open('currentFile.txt').read(), 'w')
    file_name = str(Path(file.name))
    absolute_path = str(Path(file.name).parent.absolute())
    file.write(file_content)
    file.close()
    command = "cd " + absolute_path + "&&" + "python " + file_name
    subprocess.run(["start", "/wait", "cmd", "/K", command], shell=True)

    file.close()


class Window:
    def __init__(self, win):
        self.win = win
        self.tree_view = Treeview(win)
        self.tree_view['columns'] = ("Name")
        self.tree_view.column("#0", width=180, minwidth=25)
        self.tree_view.column("Name", anchor=W, width=170)
        self.t3 = Text(win, height=50, width=130)
        self.t3.place(x=840, y=5)

        #  self.menu_bar = Menubutton(window, image=PhotoImage(file='addIcon.png'))
        self.menu_bar = Menu(window)
        #  self.menu_bar.grid(row=0, column=0)

        self.file_menu = Menu(self.menu_bar)
        # self.menu_bar.config(menu=self.file_menu)

        self.file_menu.add_command(label="Execute", command=lambda: create_file(self.t3.get("1.0", END)))
        self.file_menu.add_command(label="Select", command=lambda: self.select_file())
        self.file_menu.add_command(label="Add", command=lambda: new_file())

        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        window.config(menu=self.menu_bar)

        if open('currentFile.txt').read() is not None:
            try:
                # self.t3.insert(1.0, open(open('currentFile.txt').read()).read())
                self.text = StringVar()
                dir = str(open('currentFile.txt').read())
                self.text.set(dir)
                for file in os.listdir(dir):
                    f = os.path.join(dir, file)
                    if os.path.isfile(f):
                        self.tree_view.insert('', END, values=file)

                self.lbl_path = Label(win, text=self.text.get(),
                                      font=('Helvetica', 10, 'bold italic'))
                self.lbl_path.place(x=5, y=5)
            except FileNotFoundError:
                pass

        # self.btn_execute = Button(win, text='Execute',
        #                           command=lambda: create_file(self.t3.get("1.0", END)))
        # self.btn_select = Button(win, text='Select',
        #                          command=lambda: self.select_file())
        # self.btn_new = Button(win, text='Add',
        #                          command=lambda: new_file())

        #  self.tree_view.heading("#0", text="Label", anchor=W)
        #  self.tree_view.heading("Name", text="Name", anchor=W)
        #  self.tree_view.insert(parent='', index='end', iid=0, text="Parent", values=("Test"))
        #
        self.tree_view.pack(side=TOP, fill=X)
        self.tree_view.bind("<Double-1>", self.OnDoubleClick)
        self.tree_view.place(x=5, y=50)
        # self.btn_execute.place(x=5, y=240)
        # self.btn_select.place(x=90, y=240)
        # self.btn_new.place(x=175, y=240)
        window.title('0r4nge IDE')
        window.geometry('1700x800+10+10')
        window.mainloop()

    def OnDoubleClick(self, event):
        item = self.tree_view.identify('item', event.x, event.y)
        print("you clicked on", self.tree_view.item(item, "text"))

    def select_file(self):
        self.file = open('currentFile.txt', 'r')
        self.file_name = askdirectory()
        if len(self.file_name) == 0:
            return
        try:
            self.file = open('currentFile.txt', 'w')
            self.file.write(str(Path(self.file_name)))
        except AttributeError:
            pass

        self.t3.delete(1.0, END)
        self.file.close()
        #  self.lbl_path.destroy()
        # self.lbl_path = Label(self.win, text=str(Path(self.file_name)),
        # font=('Helvetica', 10, 'bold italic'))
        # self.btn_select.place(x=90, y=240)
        self.text.set(str(Path(self.file_name)))
        self.t3.insert(1.0, open(str(Path(self.file_name))).read())


window = Tk()
my_win = Window(window)
