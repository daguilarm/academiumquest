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

		# Field config
		self.field = {
			'padx': 10,
			'pady': 10,
			'sticky': 'we',
		}

		# Define the styles
		self.crud_style()

		# Categories
		self.categories = list(sql.categories())

		# Current row
		self.row = 0

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
		).grid(row=self.row, column=0, columnspan=4)

		# Category field
		self.field_category()

		# Question field
		self.question()

		# Answer 1
		self.answer(1)

		# Answer 2
		self.answer(2)

		# Answer 3
		self.answer(3)

		# Answer 4
		self.answer(4)

		# Correct answer
		# answer_option = tkinter.IntVar()
		# tkinter.Radiobutton(self.crud, text="Respuesta 1", variable=answer_option, value=1).grid(row=11, column=0)
		# tkinter.Radiobutton(self.crud, text="Respuesta 2", variable=answer_option, value=2).grid(row=11, column=1)
		# tkinter.Radiobutton(self.crud, text="Respuesta 3", variable=answer_option, value=3).grid(row=11, column=2)
		# tkinter.Radiobutton(self.crud, text="Respuesta 4", variable=answer_option, value=4).grid(row=11, column=3)


		# Action buttons
		self.field_buttons()

	# Field category
	def field_category(self):
		# Update row
		self.row += 1

		# Get all the categories from the database
		categories = {}
		for category in self.categories:
			categories['{} - {}'.format(category.get('name'), category.get('id'))] = category.get('id')

		# Label
		tkinter.Label(
			self.crud,
			text="Asignatura",
			font=self.font,
		).grid(self.field, row=self.row, column=0)

		# Field
		field = ttk.Combobox(
			self.crud,
			values=list(categories.keys()),
			font=self.font,
			state='readonly',
			width=50,
		)
		field.grid(self.field, row=self.row, column=1, columnspan=3)

		# Item bind from the database
		if self.action == 'edit':
			# We have to search the id in the filters
			for category in self.categories:
				if category.get('name') == self.values[2]:
					# Now we have the category name
					field.set('{} - {}'.format(category.get('name'), category.get('id')))

	# Field question
	def question(self):
		# Update row
		self.row += 1

		# Label
		tkinter.Label(
			self.crud,
			text="Pregunta",
			font=self.font,
		).grid(self.field, row=self.row, column=0)

		# Field
		field = tkinter.Text(self.crud, height=10, font=self.font)
		field.grid(self.field, row=self.row, column=1, columnspan=3)

		# Item bind from the database
		field.insert(INSERT, self.values[3])

	# Field answer
	def answer(self, number):
		# Update row
		self.row += 1

		# Label
		tkinter.Label(
			self.crud,
			text='Respuesta {}'.format(number),
			font=self.font,
		).grid(self.field, row=self.row, column=0)

		# Field
		field = tkinter.Text(self.crud, height=5, font=self.font)
		field.grid(self.field, row=self.row, column=1, columnspan=2)

		# Item bind from the database
		field.insert(INSERT, self.values[3 + number])

	# Action buttons
	def field_buttons(self):
		# Update row
		self.row += 1

		# Exit/Cancel button
		ttk.Button(
			self.crud,
			text='Cancelar',
			command=self.crud.destroy,
			style='Delete.TButton',
		).grid(row=self.row, column=1, padx=10, pady=10, sticky='we')

		# Action button
		# Define action base on self.action...
		ttk.Button(
			self.crud,
			text='Editar',
			command=self.crud.destroy,
			style='Regular.TButton',
		).grid(row=self.row, column=2, padx=10, pady=10, sticky='we')

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
