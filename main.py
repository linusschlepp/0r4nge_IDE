import os
import shutil
import subprocess
from tkinter import *
from tkinter.filedialog import *
from tkinter.ttk import *

import PIL.ImageFile

from popup import PopUp
from pathlib import Path
from PIL import Image, ImageTk as itk
import popup_ as pu


# TODO: Fix add-images/icons to project especially TreeView
class Window:
    def __init__(self, win):
        self.win = win
        self.win.iconbitmap("images/Orange_IDE.ico")
        self.tree_view = Treeview(win)
        self.tree_view['columns'] = "Name"
        self.text_area = Text(win, height=50, width=130)
        self.text_area.place(x=500, y=5)
        self.counter = 0
        self.menu_bar = Menu(self.win)
        self.win.config(menu=self.menu_bar)

        self.file_menu = Menu(self.menu_bar)

        self.file_menu.add_command(
            label='Add file',
            command=lambda: self.add_file(False)
        )
        self.file_menu.add_command(
            label='Add directory',
            command=lambda: self.add_file(True)
        )
        self.file_menu.add_command(
            label='Add new project',
            command=lambda: self.add_project()
        )

        self.file_menu.add_command(
            label='Select existing project',
            command=lambda: self.select_file()
        )

        self.menu_bar.add_cascade(
            label="Add",
            menu=self.file_menu,
            underline=0
        )

        self.menu_bar.add_command(
            label='Execute',
            command=lambda: self.create_file(self.text_area.get("1.0", END))
        )

        self.menu_bar.add_command(
            label='Quit',
            command=lambda: self.close_window()
        )

        # self.btn_execute = Button(win, text='Execute',
        #                           command=lambda: self.create_file(self.t3.get("1.0", END)))
        # self.btn_select = Button(win, text='Select',
        #                          command=lambda: self.select_file())
        # self.btn_add_file = Button(win, text='Add file',
        #                            command=lambda: self.add_file(False))
        # self.btn_add_dir = Button(win, text='Add directory',
        #                           command=lambda: self.add_file(True))

        self.tree_view.pack(side=TOP, fill=X)
        self.text_area.bind("<Key>", lambda event: self.change_file())
        self.tree_view.bind("<Double-1>", self.on_double_click)
        self.tree_view.bind("<Button-3>", self.do_popup)
        self.tree_view.place(x=5, y=60)
        # self.btn_execute.place(x=5, y=5)
        # self.btn_select.place(x=90, y=5)
        # self.btn_add_file.place(x=175, y=5)
        # self.btn_add_dir.place(x=260, y=5)
        window.title('0r4nge IDE')
        window.geometry('1700x800+10+10')

        self.text = StringVar()
        dir = str(open('currentFile.txt').read())

        self.lbl_path = None
        self.lbl_file = None
        self.current_file = None
        self.dir_list = []
        self.name_file = str(os.listdir(dir)[0]) if len(os.listdir(dir)) > 0 else ""

        try:
            self.current_file = dir + "\\" + self.name_file
        except IndexError:
            pass

        self.set_root_node(dir)

        window.mainloop()

    def set_root_node(self, dir):

        if open('currentFile.txt').read() is not None:
            try:
                self.text.set(dir)

                if os.path.isfile(Path(self.current_file)):
                    self.text_area.insert(1.0, open(str(Path(self.current_file))).read())
                self.root_node = self.tree_view.insert('', text=str(Path(dir).name), index='end')

                self.file_structure(self.root_node, dir)

                if self.lbl_path is not None and self.lbl_file is not None:
                    self.lbl_path.destroy()
                    self.lbl_file.destroy()
                self.lbl_path = Label(self.win, text=str(Path(self.text.get()).name) + " - " + self.text.get(),
                                      font=('Helvetica', 10, 'bold italic'))
                self.lbl_path.place(x=5, y=15)

                self.lbl_file = Label(self.win, text="Selected file: " + self.name_file,
                                      font=('Helvetica', 8, 'bold'))
                self.lbl_file.place(x=5, y=35)

            except FileNotFoundError or IndexError as e:
                if type(e) == "IndexError":
                    pass
                else:
                    print(e)

    def rename_file(self):

        new_name = PopUp(self.win)
        self.win.wait_window(new_name.top)
        new_name = str(new_name.value)

        if len(new_name) == 0:
            return

        if self.tree_view.selection()[0] == self.root_node:
            self.file = open('currentFile.txt', 'w')
            self.file.write(str(Path(self.current_file).parent) + "\\" + new_name)
            self.text.set(str(Path(self.current_file).parent) + "\\" + new_name)
            self.file.close()
            self.lbl_path.destroy()
            self.lbl_path = Label(self.win, text=str(Path(self.text.get()).name) + " - " + self.text.get(),
                                  font=('Helvetica', 10, 'bold italic'))
            self.lbl_path.place(x=5, y=15)
        if os.path.isfile(Path(self.current_file)):
            new_name = new_name + ".py"
        os.rename(self.current_file, str(Path(self.current_file).parent) + "\\" + new_name)
        self.tree_view.item(self.tree_view.selection()[0], text=new_name)

    def delete_file(self):

        if os.path.isfile(Path(self.current_file)):
            os.remove(self.current_file)

        elif os.path.isdir(Path(self.current_file)):
            shutil.rmtree(self.current_file)

        self.tree_view.delete(self.tree_view.selection()[0])

        print(type(self.current_file))
        print(self.current_file)

    def do_popup(self, event):
        self.right_click_menu = Menu(self.win, tearoff=0)
        self.right_click_menu.add_command(label="Rename", command=self.rename_file)
        self.right_click_menu.add_command(label="Delete", command=self.delete_file)
        if os.path.isdir(Path(self.current_file)):
            self.right_click_menu.add_command(label="Add file", command=lambda: self.add_file_to(False))
            self.right_click_menu.add_command(label="Add directory", command=lambda: self.add_file_to(True))
        try:
            self.right_click_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.right_click_menu.grab_release()

    def add_file_to(self, is_dir):
        file_name = PopUp(self.win)
        self.win.wait_window(file_name.top)
        file_name = str(file_name.value)

        if len(file_name) == 0:
            return

        if not is_dir:
            file_name = file_name + ".py"
        self.tree_view.insert(parent=self.tree_view.selection()[0], index='end', text=file_name)

        try:
            file_name = self.current_file + "\\" + file_name
            if is_dir:
                os.mkdir(file_name)
            else:
                open(file_name, 'w')
        except AttributeError as e:
            print(e)

    def change_file(self):
        self.current_file = self.get_node_path(self.tree_view.item(self.tree_view.focus()))
        file = open(self.current_file, 'w')
        file.write(self.text_area.get("1.0", END))
        print(self.current_file)
        file.close()

    def file_structure(self, parent, dir):
        width = 16
        height = 16
        img = Image.open('gif.gif')
        img = img.resize((width, height))
        render = itk.PhotoImage(PIL.Image.open('gif.gif'))

        for file in os.listdir(dir):
            f = os.path.join(dir, file)
            new_root = self.tree_view.insert(parent, index='end', text=file, tags=Path(f),
                                             image=render)
            if os.path.isdir(f):
                self.dir_list.append(Path(f).name)
                self.file_structure(new_root, f)

    def close_window(self):
        self.win.destroy()

    def on_double_click(self, event):

        current_item = self.tree_view.item(self.tree_view.focus())

        self.current_file = self.get_node_path(current_item)

        self.lbl_file.destroy()
        self.lbl_file = Label(self.win, text="Selected file: " + str(Path(self.current_file).name),
                              font=('Helvetica', 8, 'bold'))
        self.lbl_file.place(x=5, y=35)

        if os.path.isfile(Path(self.current_file)):
            self.text_area.delete(1.0, END)
            self.text_area.insert(1.0, open(str(Path(self.get_node_path(current_item)))).read())

    def get_node_path(self, item):
        temp_path = ""
        parent_item = self.tree_view.parent(self.tree_view.selection()[0])
        item = self.tree_view.item(self.tree_view.selection()[0])

        if parent_item == "":
            return self.text.get()

        s = self.tree_view.item(parent_item)['text']
        while s != Path(self.text.get()).name:
            temp_path = s + "\\" + temp_path
            parent_item = self.tree_view.parent(parent_item)
            s = self.tree_view.item(parent_item)['text']

        return self.text.get() + "\\" + temp_path + "\\" + str(item["text"]).strip("['").strip("']'")

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

        self.text_area.delete(1.0, END)
        self.file.close()
        self.text.set(str(Path(self.file_name)))
        self.tree_view.delete(*self.tree_view.get_children())
        self.set_root_node(str(Path(self.file_name)))

    def add_project(self):
        file = asksaveasfilename()
        os.makedirs(file)
        self.file = open('currentFile.txt', 'w')
        self.file.write(file)

        self.text_area.delete(1.0, END)
        self.file.close()
        self.text.set(file)
        self.tree_view.delete(*self.tree_view.get_children())
        self.set_root_node(file)

    def add_file(self, is_dir):
        self.dir_list.append("")
        file_name = pu.PopUp(self.win, list=self.dir_list)
        self.win.wait_window(file_name.top)
        dir_name = file_name.variable.get()
        file_name = str(file_name.value)
        self.temp_item = None

        #
        # TODO: create the right file structure to add it to the files
        if len(dir_name) != 0:
            test_len = len(self.tree_view.get_children())
            # for item in self.tree_view.get_children():
            #     s = self.tree_view.item(item)['text']
            #     if self.tree_view.item(item)['text'] == dir_name:
            #         temp_item = item
            #         break
            self.rec_approach(self.tree_view.get_children(), dir_name)

        if len(file_name) == 0:
            return

        if not is_dir:
            file_name = file_name + ".py"

        if self.temp_item is not None:
            self.tree_view.insert(self.temp_item, index='end', text=file_name)
        else:
            self.tree_view.insert(self.root_node, index='end', text=file_name)

        try:
            file_name = self.text.get() + "\\" + file_name
            if is_dir:
                os.mkdir(file_name)
            else:
                open(file_name, 'w')
        except AttributeError as e:
            print(e)

     # iterate through children of tree_view recursively
    def rec_approach(self, children, dir_name):
        for item in children:
            if self.tree_view.item(item)['text'] == dir_name:
                self.temp_item = item
            elif len(self.tree_view.get_children(item)) != 0:
                self.rec_approach(self.tree_view.get_children(item), dir_name)


window = Tk()
my_win = Window(window)
