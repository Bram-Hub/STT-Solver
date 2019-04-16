from tkinter import * 

def enter_file():
    print("hello")
    filename = e1.get()

file_window = Tk()

file_frame = Frame(file_window)
file_frame.pack(side = BOTTOM)



l1 = Label(file_window, text="File Name")
l1.pack( side = LEFT)
e1 = Entry(file_window, bd =5)
e1.pack(side = RIGHT)
button = Button(file_frame, text="Enter", command=enter_file)
button.pack()

file_window.mainloop()
