import tkinter as tk
import sys


class MenuBar(tk.Menu):
    def __init__(self, parent):
        tk.Menu.__init__(self, parent)

        file_menu = tk.Menu(self, tearoff=False)
        self.add_cascade(label="Archivo",underline=0, menu=file_menu)
        file_menu.add_command(label="Salir", underline=1, command=self.quit)

    def quit(self):
        sys.exit(0)
