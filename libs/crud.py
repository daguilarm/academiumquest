import tkinter
from tkinter import ttk

# Edit window
from tkinter.ttk import Style


class Crud:
	def __init__(self, values):
		self.values = values

		# Define container
		self.crud = tkinter.Toplevel()

		self.crud_position()

	def edit(self):

		self.crud.wm_title("Editar pregunta")

		crud_font = tkinter.font.Font(family="Verdana", size=14)
		crud_font_title = tkinter.font.Font(family="Verdana", size=28)

		# Label for edit
		tkinter.Label(
			self.crud,
			text="Editar pregunta",
			font=crud_font_title,
			padx=20,
			pady=20,
		).grid(row=0, column=0, columnspan=2)

		# This will be adding style, and
		# naming that style variable as
		# W.Tbutton (TButton is used for ttk.Button).
		style = Style()

		style.configure(
			'Delete.TButton',
			font=crud_font,
			background='red',
			borderwidth=0,
		)

		style.configure(
			'Regular.TButton',
			font=crud_font,
			borderwidth=0,
		)

		# Exit button
		cancel_button = ttk.Button(
			self.crud,
			text='Cancelar',
			command=self.crud.destroy,
			style='Delete.TButton'
		).grid(row=1, column=0, padx=10, pady=10)


		# Update button
		ttk.Button(
			self.crud,
			text='Editar',
			command=self.crud.destroy,
			style='Regular.TButton'
		).grid(row=1, column=1, padx=10, pady=10)

	# Determine the window position
	def crud_position(self):
		# Screen dimensions
		screen_width = self.crud.winfo_screenwidth()
		screen_height = self.crud.winfo_screenheight()

		# Calculate popup position
		size = tuple(int(_) for _ in self.crud.geometry().split('+')[0].split('x'))
		x = screen_width / 2 - size[0] / 2
		y = (screen_height - size[1]) * 20 / 100

		# Set the position
		self.crud.geometry("+%d+%d" % (x, y))
