import libs.orm as sql
import tkinter
from tkinter import ttk
from tkinter.ttk import Style


# CRUD
class Crud:
	def __init__(self, root, values):
		self.root = root
		self.values = values

		# Reset all the open windows
		self.reset_all_open_windows()

		# Define container
		self.crud = tkinter.Toplevel(self.root)

		# Define the window position in the screen
		self.crud_position()

		# Define the fonts
		self.font = tkinter.font.Font(family="Verdana", size=14)
		self.font_title = tkinter.font.Font(family="Verdana", size=28)

		# Define the styles
		self.crud_style()

	# Edit values
	def edit(self):
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

		# ----------- Select subject / category

		# Get all the categories from the database
		list_of_categories = list(sql.categories().flatten().unique().prepend(''))

		# Label
		tkinter.Label(
			self.crud,
			text="Asignatura",
			font=self.font,
			width=20,
		).grid(row=1, column=0, padx=5, pady=5)

		# Options
		field_category = ttk.Combobox(
			self.crud,
			values=list_of_categories,
			font=self.font,
			state='readonly',
			width=50,
		)
		field_category.grid(row=1, column=1, columnspan=3, padx=5, pady=5)
		field_category.set(self.values[2])

		# ----------- Buttons

		# Exit/Cancel button
		ttk.Button(
			self.crud,
			text='Cancelar',
			command=self.crud.destroy,
			style='Delete.TButton'
		).grid(row=12, column=1, padx=10, pady=10, sticky="e")

		# Update button
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
	def reset_all_open_windows(self):
		# Get all the items
		for items in self.root.winfo_children():
			# If it is not the root...
			if '!toplevel' in str(items):
				items.destroy()
