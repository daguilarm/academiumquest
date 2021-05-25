# Created by @daguilarm at 24/5/21
from tkinter import *
import sys


class MenuBar(Menu):
    def __init__(self, parent):
        Menu.__init__(self, parent)

        file_menu = Menu(self, tearoff=False)
        self.add_cascade(label="Archivo",underline=0, menu=file_menu)
        file_menu.add_command(label="Salir", underline=1, command=self.quit)

    def quit(self):
        sys.exit(0)
