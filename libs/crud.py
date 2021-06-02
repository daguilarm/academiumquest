import libs.orm as sql
import tkinter
from tkinter import ttk, INSERT, messagebox
from tkinter.ttk import Style


# CRUD
class Crud:
	"""
		All the CRUD actions and methods described here are for libs/table.py
	"""

	def __init__(self, table, values = ''):
		self.table = table
		self.root = self.table.root
		self.values = values

		# Crud action
		self.action = ''

		# Destroy all the open windows
		self.destroy_windows()

		# Define container
		self.crud = tkinter.Toplevel(self.root)

		# Define the window position in the screen
		self.crud_position()

		# Define the fonts
		self.font = tkinter.font.Font(family="Verdana", size=14)
		self.font_title = tkinter.font.Font(family="Verdana", size=28)
		self.font_button = tkinter.font.Font(family="Verdana", size=18)

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

	# Create or Edit values
	def render(self, action='edit'):
		"""
			CRUD action edit:
				- All the methods and parameters necessaries for update are here.
				- All the fields has been packed in methods in order to be reused in other actions
		"""
		self.action = action

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

	""" 
		All the field methods are packed belongs.
		Each field has it own method.
		Each method calculate it own position in the grid, using the 'self.row' variable.
		This methods are reusable for 'edit' or 'create' actions, using the 'self.action' variable.
	"""

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

		# If action is EDIT: Item bind from the database
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

		# If action is EDIT: Item bind from the database
		if self.action == 'edit':
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

		# If action is EDIT: Item bind from the database
		if self.action == 'edit':
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

		# If action is EDIT: Item bind from the database
		if self.action == 'edit':
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

		# If action is EDIT: Item bind from the database
		if self.action == 'edit':
			field.set(self.values[9])

		return field

	""" 
		All the buttons methods are packed belongs.
		The buttons calculate it own position in the grid, using the 'self.row' variable.
		The button: 'button_action' is reusable for 'edit' or 'create' actions, using the 'self.action' variable.
	"""

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

		# Define action base on self.action...
		if self.action == 'edit':
			action_text = 'Editar'
			action_exec = 'edit'
		else:
			action_text = 'Crear'
			action_exec = 'create'

		# Action button
		button_action = ttk.Button(
			self.crud,
			text=action_text,
			command=lambda: self.crud_execute(action=action_exec),
			style='Regular.TButton',
		)
		button_action.grid(row=self.row, column=2, padx=10, pady=10, sticky='we')

	""" 
		This method execute the actions: edit or create.
	"""

	# Update or Create values
	def crud_execute(self, action):
		fields = {
			'id': self.id,
			'category': int(self.get_category_id()),
			'question': self.question.get('1.0', 'end').strip(),
			'answer_1': self.answer_1.get('1.0', 'end').strip(),
			'answer_2': self.answer_2.get('1.0', 'end').strip(),
			'answer_3': self.answer_3.get('1.0', 'end').strip(),
			'answer_4': self.answer_4.get('1.0', 'end').strip(),
			'correct': int(self.correct.get().strip()),
			'type': self.type.get().strip(),
		}

		# Edit action
		if action == 'edit':
			operation = sql.questions_update(fields)
		# Create action
		else:
			pass

		# Close the window and update the application
		self.table.refresh(self.table)
		self.crud.destroy()

		# Show success or fail messages
		crud_execute_message(operation)

	""" 
		All the auxiliary methods.
	"""

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
			font=self.font_button,
			background='red',
			borderwidth=0,
			padding=15,
		)

		style.configure(
			'Regular.TButton',
			font=self.font_button,
			borderwidth=0,
			padding=15,
		)

	# Destroy all open windows
	def destroy_windows(self):
		# Get all the items
		for items in self.root.winfo_children():
			# If it is not the root...
			if '!toplevel' in str(items):
				items.destroy()


# Message alert: Success or fail messages
def crud_execute_message(operation):
	# Success
	if operation:
		tkinter.messagebox.showinfo(
			title='Operación realizada',
			message='Se ha realizado con éxito la operación.'
		)

	# Fail
	else:
		tkinter.messagebox.showerror(
			title='Se ha producido un error',
			message='Ha ocurrido un error al realizar la operación.\n' +
			'Si el error persiste, por favor, contacte con el administrador del sistema.'
		)