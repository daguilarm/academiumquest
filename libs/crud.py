import tkinter


# Edit window
def edit(values):
    win = tkinter.Toplevel()
    win.wm_title("Window")

    l = tkinter.Label(win, text="Input")
    l.grid(row=0, column=0)

    b = tkinter.Button(win, text="Okay", command=win.destroy)
    b.grid(row=1, column=0)

    print(values)
