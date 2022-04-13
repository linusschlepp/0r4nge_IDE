import json
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


class Window:
    def __init__(self, win):
        self.win = win
        self.tree_view = Treeview(win)
        self.tree_view['columns'] = ("Name")
      #  self.tree_view.column("#0", width=120, minwidth=25, stretch=NO)
       #  self.tree_view.heading("#0", text="Name", anchor=W)
       # self.tree_view.column("Name", width=150, minwidth=150, stretch=NO)
        # self.tree_view.column("Name", anchor=W, width=170)
        self.t3 = Text(win, height=50, width=130)
        self.t3.place(x=500, y=5)

        #  self.menu_bar = Menubutton(window, image=PhotoImage(file='addIcon.png'))
        # self.menu_bar = Menu(window)
        #  self.menu_bar.grid(row=0, column=0)

        # self.file_menu = Menu(self.menu_bar)
        # self.menu_bar.config(menu=self.file_menu)

        # self.file_menu.add_command(label="Execute", command=lambda: self.create_file(self.t3.get("1.0", END)))
        # self.file_menu.add_command(label="Select", command=lambda: self.select_file())
        # self.file_menu.add_command(label="Add", command=lambda: new_file())

        # self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        #  window.config(menu=self.menu_bar)

        if open('currentFile.txt').read() is not None:
            try:
                # self.t3.insert(1.0, open(open('currentFile.txt').read()).read())
                self.text = StringVar()
                dir = str(open('currentFile.txt').read())
                self.text.set(dir)
                self.current_file = dir + "\\" + str(os.listdir(dir)[0])

                self.lbl_file = str(os.listdir(dir)[0])
                self.lbl_file = Label(win, text="Selected file: " + os.listdir(dir)[0],
                                      font=('Helvetica', 8, 'bold'))
                self.lbl_file.place(x=5, y=70)
                self.t3.insert(1.0, open(str(Path(self.current_file))).read())
                self.tree_view.insert(parent='', iid=0, text=str(Path(dir).name), index='end')
                for file in os.listdir(dir):
                    f = os.path.join(dir, file)
                    if os.path.isfile(f):
                        self.tree_view.insert(parent='0', index='end', text=str(file))

                self.lbl_path = Label(win, text=str(Path(self.text.get()).name) + " - " + self.text.get(),
                                      font=('Helvetica', 10, 'bold italic'))
                self.lbl_path.place(x=5, y=50)
            except FileNotFoundError:
                pass

        self.btn_execute = Button(win, text='Execute',
                                  command=lambda: self.create_file(self.t3.get("1.0", END)))
        self.btn_select = Button(win, text='Select',
                                 command=lambda: self.select_file())
        self.btn_new = Button(win, text='Add',
                              command=lambda: self.new_file())

        # self.tree_view.heading("#0", text="Label", anchor=W)
        # self.tree_view.heading("Name", text="Name", anchor=W)
        # self.tree_view.insert(parent='', index='end', iid=0, text="Parent", values=("Test"))

        self.tree_view.pack(side=TOP, fill=X)
        self.tree_view.bind("<Double-1>", self.OnDoubleClick)
        self.tree_view.place(x=5, y=100)
        self.btn_execute.place(x=5, y=5)
        self.btn_select.place(x=90, y=5)
        self.btn_new.place(x=175, y=5)
        window.title('0r4nge IDE')
        window.geometry('1700x800+10+10')
        window.mainloop()

    def OnDoubleClick(self, event):
        current_item = self.tree_view.item(self.tree_view.focus())
        self.current_file = self.text.get() + "\\" + str(current_item["text"]).strip("['").strip("']'")
        self.lbl_file.destroy()
        self.lbl_file = Label(self.win, text="Selected file: " + str(current_item["text"]).strip("['").strip("']'"),
                              font=('Helvetica', 8, 'bold'))
        self.lbl_file.place(x=5, y=70)
        self.t3.delete(1.0, END)
        self.t3.insert(1.0, open(str(Path(self.current_file))).read())

    def create_file(self, file_content):
        file = open(self.current_file, 'w')
        file_name = str(Path(file.name))
        absolute_path = str(Path(file.name).parent.absolute())
        file.write(file_content)
        file.close()
        command = "cd " + absolute_path + "&&" + "python " + file_name
        subprocess.run(["start", "/wait", "cmd", "/K", command], shell=True)

        file.close()

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

    def popupwin(self):
        # Create a Toplevel window
        self.top = Toplevel(self.win)
        self.top.geometry("750x250")
        self.top.title("Enter name")

        # Create an Entry Widget in the Toplevel window
        self.entry = Entry(self.top, width=25)
        self.entry.pack()

        # Create a Button to print something in the Entry widget
        #  Button(top, text="Ok", command=lambda: insert_val(entry)).pack(pady=5, side=TOP)
        # Create a Button Widget in the Toplevel Window
        self.button = Button(self.top, text="Ok", command=lambda: self.top.destroy())
        self.button.pack(pady=5, side=TOP)

        # Create a Label
    #    self.label = Label(self.win, text="Click the Button to Open the Popup Dialogue", font=('Helvetica 15 bold'))
    #    self.label.pack(pady=20)

        self.new_file = self.entry.get()

    def new_file(self):
        file_name = input("enter file name: ")
        self.tree_view.insert('', END, values=file_name+".py")
        file_name = self.text.get() + "\\" + file_name+".py"
        try:
            open(file_name, 'w')
        except AttributeError:
            pass


window = Tk()
my_win = Window(window)
