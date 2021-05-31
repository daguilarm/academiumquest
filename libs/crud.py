import libs.orm as sql
import tkinter
from tkinter import ttk, INSERT
from tkinter.ttk import Style


# CRUD
class Crud:
	def __init__(self, root, values):
		self.root = root
		self.values = values

		# Crud action
		self.action = ''

		# Reset all the open windows
		self.reset()

		# Define container
		self.crud = tkinter.Toplevel(self.root)

		# Define the window position in the screen
		self.crud_position()

		# Define the fonts
		self.font = tkinter.font.Font(family="Verdana", size=14)
		self.font_title = tkinter.font.Font(family="Verdana", size=28)

		# Define the fields width
		self.width_label = 20
		self.width_field = 50

		# Define the styles
		self.crud_style()

	# Edit values
	def edit(self):
		self.action = 'edit'

		# Set the title
		self.crud.wm_title("Editar pregunta")

		# Label for edit
		tkinter.Label(
			self.crud,
			text="Editar pregunta",
			font=self.font_title,
			padx=20,
			pady=20,
		).grid(row=0, column=0, columnspan=4)

		# Select subject / category
		self.field_category()

		# Label
		tkinter.Label(
			self.crud,
			text="Pregunta",
			font=self.font,
			width=self.width_label,
		).grid(row=2, column=0, padx=5, pady=5)
		field = tkinter.Text(self.crud, width=self.width_field, height=10, font=self.font)
		field.grid(row=2, column=1, columnspan=3, padx=5, pady=5)
		field.insert(INSERT, self.values[3])

		# Action buttons
		self.field_buttons()

	# Field category
	def field_category(self):
		# Get all the categories from the database
		list_of_categories = list(sql.categories().flatten().unique().prepend(''))

		# Label
		tkinter.Label(
			self.crud,
			text="Asignatura",
			font=self.font,
			width=self.width_label,
		).grid(row=1, column=0, padx=5, pady=5)

		# Options
		field = ttk.Combobox(
			self.crud,
			values=list_of_categories,
			font=self.font,
			state='readonly',
			width=50,
		)
		field.grid(row=1, column=1, columnspan=3, padx=5, pady=5)

		# Item bind from the database
		if self.action == 'edit':
			field.set(self.values[2])

	# Action buttons
	def field_buttons(self):
		# Exit/Cancel button
		ttk.Button(
			self.crud,
			text='Cancelar',
			command=self.crud.destroy,
			style='Delete.TButton'
		).grid(row=12, column=1, padx=10, pady=10, sticky="e")

		# Action button
		# Define action base on self.action...
		ttk.Button(
			self.crud,
			text='Editar',
			command=self.crud.destroy,
			style='Regular.TButton'
		).grid(row=12, column=2, padx=10, pady=10, sticky="w")

	# Determine the window position
	def crud_position(self):
		x = (self.crud.winfo_screenwidth() / 2) - 350
		y = 250
		self.crud.geometry("+%d+%d" % (x, y))

	# Define the CRUD styles
	def crud_style(self):
		# This will be adding style, and
		style = Style()

		style.configure(
			'Delete.TButton',
			font=self.font,
			background='red',
			borderwidth=0,
		)

		style.configure(
			'Regular.TButton',
			font=self.font,
			borderwidth=0,
		)

	# Destroy all open windows
	def reset(self):
		# Get all the items
		for items in self.root.winfo_children():
			# If it is not the root...
			if '!toplevel' in str(items):
				items.destroy()
