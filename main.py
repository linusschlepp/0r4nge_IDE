import os
import subprocess
from tkinter import *
from tkinter.filedialog import *
from tkinter.ttk import *
from popup import PopUp
from pathlib import Path


class Window:
    def __init__(self, win):
        self.win = win
        self.tree_view = Treeview(win)
        self.tree_view['columns'] = ("Name")
        self.t3 = Text(win, height=50, width=130)
        self.t3.place(x=500, y=5)

        if open('currentFile.txt').read() is not None:
            try:

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
                              command=lambda: self.add_file())

        self.tree_view.pack(side=TOP, fill=X)
        self.t3.bind("<Key>", lambda event: self.change_file())
        self.tree_view.bind("<Double-1>", self.on_double_click)
        self.tree_view.place(x=5, y=100)
        self.btn_execute.place(x=5, y=5)
        self.btn_select.place(x=90, y=5)
        self.btn_new.place(x=175, y=5)
        window.title('0r4nge IDE')
        window.geometry('1700x800+10+10')
        window.mainloop()

    def change_file(self):
        file = open(self.current_file, 'w')
        file.write(self.t3.get("1.0", END))
        file.close()

    def on_double_click(self, event):
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
        self.text.set(str(Path(self.file_name)))
        self.t3.insert(1.0, open(str(Path(self.file_name))).read())

    def add_file(self):
        file_name = PopUp(self.win)
        self.win.wait_window(file_name.top)
        self.tree_view.insert(parent='0', index='end', text=str(file_name.value) + ".py")
        file_name = self.text.get() + "\\" + str(file_name.value) + ".py"
        try:
            open(file_name, 'w')
        except AttributeError:
            pass


window = Tk()
my_win = Window(window)
