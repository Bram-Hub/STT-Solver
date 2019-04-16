from tkinter import * 

root = Tk()
main_frame = Frame(root)
main_frame.pack()

top_frame = Frame(main_frame)
top_frame.pack(side=TOP)

bottom_frame = Frame(main_frame)
bottom_frame.pack(side=BOTTOM)

button1 = Button(top_frame, text="Top 1")
button1.pack(side=LEFT)
button2 = Button(top_frame, text="Top 2")
button2.pack(side=RIGHT)

button3 = Button(bottom_frame, text="Bottom 1")
button3.pack(side=LEFT)
button4 = Button(bottom_frame, text="Bottom 2")
button4.pack(side=RIGHT)

root.mainloop()
print("Hello") 