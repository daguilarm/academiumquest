import tkinter


# Edit window
def edit(values):
    # Define container
    win = tkinter.Toplevel()
    win.wm_title("Editar pregunta")

    # Screen dimensions
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()

    # Calculate popup position
    size = tuple(int(_) for _ in win.geometry().split('+')[0].split('x'))
    x = screen_width / 2 - size[0] / 2
    y = (screen_height - size[1]) * 20 / 100

    # Set the position
    win.geometry("+%d+%d" % (x, y))

    # Label for edit
    tkinter.Label(win, text="Editar pregunta").grid(row=0, column=0)

    # Exit button
    tkinter.Button(win, text="Okay", command=win.destroy).grid(row=1, column=0)

    print(values)
