from tkinter import END

import libs.orm as sql
import tkinter
from tkinter.ttk import Style


# Categories
class Category:
	"""
		All the Categories
	"""

	def __init__(self, root):
		self.root = root

		# Destroy all the open windows
		self.destroy_windows()

		# Define container
		self.frame = tkinter.Toplevel(self.root)

		# Define the window position in the screen
		self.crud_position()

		# Get all the categories
		self.categories = sql.categories()

		# Define the fonts
		self.font = tkinter.font.Font(family="Verdana", size=14)
		self.font_title = tkinter.font.Font(family="Verdana", size=28)
		self.font_button = tkinter.font.Font(family="Verdana", size=18)

		# Define the styles
		self.crud_style()

	# Show and create the categories
	def render(self):
		# Label for edit
		tkinter.Label(
			self.frame,
			text='Listado de Temas',
			font=self.font_title,
			padx=20,
			pady=20,
		).grid(row=0, column=0, columnspan=3)

		for (index, category) in enumerate(self.categories, 1):

			# Category id
			id = tkinter.Entry(self.frame, font=self.font, width=5, fg='black')
			id.grid(row=index, column=0)
			id.insert(END, category['id'])
			id.configure(state='readonly')

			# Category name
			name = tkinter.Entry(self.frame, font=self.font,  width=30, fg='black')
			name.grid(row=index, column=1)
			name.insert(END, category['name'])

	# Determine the window position
	def crud_position(self):
		x = (self.frame.winfo_screenwidth() / 2) - 350
		y = 100
		self.frame.geometry("+%d+%d" % (x, y))

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
