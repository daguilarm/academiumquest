import libs.orm as sql
import tkinter
from tkinter import ttk, INSERT
from tkinter.ttk import Style


# CRUD
class Crud:
	def __init__(self, table, values):
		self.table = table
		self.root = self.table.root
		self.values = values

		# Crud action
		self.action = ''

		# Reset all the open windows
		self.crud_reset_windows()

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

		# Fields
		self.id = int(self.values[0])
		self.category = tkinter.StringVar()
		self.question = tkinter.StringVar()
		self.answer_1 = tkinter.StringVar()
		self.answer_2 = tkinter.StringVar()
		self.answer_3 = tkinter.StringVar()
		self.answer_4 = tkinter.StringVar()
		self.correct = tkinter.IntVar()
		self.type = tkinter.StringVar()

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
		self.category = self.field_category()

		# Question field
		self.question = self.field_question()

		# Answer 1
		self.answer_1 = self.field_answer(1)

		# Answer 2
		self.answer_2 = self.field_answer(2)

		# Answer 3
		self.answer_3 = self.field_answer(3)

		# Answer 4
		self.answer_4 = self.field_answer(4)

		# Correct answer
		self.correct = self.field_correct()

		# Question type
		self.type = self.field_type()

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

		return field

	# Field question
	def field_question(self):
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

		return field

	# Field answer
	def field_answer(self, number):
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

		return field

	# Correct answer
	def field_correct(self):
		# Update row
		self.row += 1

		# Label
		tkinter.Label(
			self.crud,
			text="Respuesta correcta",
			font=self.font,
		).grid(self.field, row=self.row, column=0)

		# Field
		field = ttk.Combobox(
			self.crud,
			values=list(range(1, 5)),
			font=self.font,
			state='readonly',
			width=50,
		)
		field.grid(self.field, row=self.row, column=1, columnspan=3)

		# Item bind from the database
		field.set(self.values[8])

		return field

	# Correct answer
	def field_type(self):
		# Update row
		self.row += 1

		# Label
		tkinter.Label(
			self.crud,
			text="Tipo",
			font=self.font,
		).grid(self.field, row=self.row, column=0)

		# Field
		field = ttk.Combobox(
			self.crud,
			values=['eir', 'ope'],
			font=self.font,
			state='readonly',
			width=50,
		)
		field.grid(self.field, row=self.row, column=1, columnspan=3)

		# Item bind from the database
		field.set(self.values[9])

		return field

	# Action buttons
	def field_buttons(self):
		# Update row
		self.row += 1

		# Exit/Cancel button
		button_exit = ttk.Button(
			self.crud,
			text='Cancelar',
			command=self.crud.destroy,
			style='Delete.TButton',
		)
		button_exit.grid(row=self.row, column=1, padx=10, pady=10, sticky='we')

		# Action button
		# Define action base on self.action...
		button_update = ttk.Button(
			self.crud,
			text='Editar',
			command=lambda: self.crud_update(),
			style='Regular.TButton',
		)
		button_update.grid(row=self.row, column=2, padx=10, pady=10, sticky='we')

	# Update values
	def crud_update(self):
		# Get the values
		field_id = self.id
		field_category = int(self.get_category_id())
		field_question = self.question.get('1.0', 'end').strip()
		field_answer_1 = self.answer_1.get('1.0', 'end').strip()
		field_answer_2 = self.answer_2.get('1.0', 'end').strip()
		field_answer_3 = self.answer_3.get('1.0', 'end').strip()
		field_answer_4 = self.answer_4.get('1.0', 'end').strip()
		field_correct = int(self.correct.get().strip())
		field_type = self.type.get().strip()

		update = sql.db.\
			table('questions').\
			where('id', field_id).\
			update(
			{
				'category_id': field_category,
				'question': field_question,
				'answer_1': field_answer_1,
				'answer_2': field_answer_2,
				'answer_3': field_answer_3,
				'answer_4': field_answer_4,
				'correct': field_correct,
				'type': field_type,
			}
		)

		if update:
			self.table.refresh(self.table)
			self.crud.destroy()

	# Get the category ID
	def get_category_id(self):
		category = self.category.get().strip().split(' - ')

		return category[1].strip()

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
	def crud_reset_windows(self):
		# Get all the items
		for items in self.root.winfo_children():
			# If it is not the root...
			if '!toplevel' in str(items):
				items.destroy()
