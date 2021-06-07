import tkinter as tk
import sys

import config
from libs.table import Table


class MenuBar(tk.Menu):
    def __init__(self, parent):
        tk.Menu.__init__(self, parent)

        # Default menu settings
        self.config = {
            'tearoff': False,
            'font': ('', 13),
        }

        # Parent
        self.parent = parent

        # Init the Table class for operations
        self.table = self.create_table()

        # File
        self.file()

        # Questions
        self.questions()

    # File menu
    def file(self):
        # Create the file container
        file_menu = tk.Menu(self, self.config)
        self.add_cascade(label='Archivo',underline=0, menu=file_menu)

        # File options
        file_menu.add_command(label='Acerca de...', underline=1, state='disable')
        file_menu.add_command(label='Buscar actualizaciones...', underline=1, state='disable')

        file_menu.add_separator()

        file_menu.add_command(label='Importar...', underline=1, state='disable', accelerator='cmd+i')
        file_menu.add_command(label='Exportar...', underline=1, state='disable', accelerator='cmd+e')

        file_menu.add_separator()

        file_menu.add_command(label='Salir', underline=1, command=self.quit, accelerator='ctrl+q')
        self.bind_all('<Command-q>', self.quit)

    # Questions menu
    def questions(self):
        # Create the questions container
        question_menu = tk.Menu(self, self.config)
        self.add_cascade(label='Preguntas', underline=0, menu=question_menu)

        # Questions options
        question_menu.add_command(label='Nueva...', underline=1, command=self.question_create, accelerator='cmd+n')
        self.bind_all('<Command-n>', self.question_create)

        question_menu.add_command(label='Editar...', underline=1, accelerator='cmd+e')
        self.bind_all('<Command-e>', self.question_edit)

        question_menu.add_command(label='Reiniciar', underline=1, command=self.table.reset, accelerator='cmd+r')
        self.bind_all('<Command-r>', self.table.reset)

        question_menu.add_separator()

        question_menu.add_command(label='Últimas preguntas', underline=1, state='disable')

    # Create row
    def question_create(self):
        self.table.table_row_create()

    # Edit row
    def question_edit(self):
        self.table

    # Quit program
    def quit(self):
        sys.exit(0)

    # Create Tabla
    def create_table(self):
        return Table(
            self.parent.root,
            self.parent.max_width,
            config.database['per_page'],
            config.database['page'],
            config.database['order'],
            config.database['direction'],
            config.database['filter'],
        )