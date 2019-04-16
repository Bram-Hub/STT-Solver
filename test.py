from tkinter import * 

def enter_file():
    filename = e1.get()

file_window = Tk()

main_frame = Frame(file_window)
main_frame.pack()

l1 = Label(file_window, text="File Name")
l1.pack( side = LEFT)
e1 = Entry(file_window, bd =5)
e1.pack(side = RIGHT)
button = Button(main_frame, text="Enter", command=enter_file)
button.pack()

file_window.mainloop()
