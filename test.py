from tkinter import *
from PIL import ImageTk, Image
from datetime import datetime as dt
import time
import threading


# app = Tk()
# app.title("Welcome")
# image2 =Image.open('scenic.jpg').resize((400,400))
# image1 = ImageTk.PhotoImage(image2)
# w = image1.width()
# h = image1.height()
# app.geometry(f'{w}x{h}')
# # app.configure(background='scenic.png')
# app.configure(background = image1)
#
# # labelText = StringVar()
# # labelText.set("Welcome !!!!")
# # #labelText.fontsize('10')
# #
# # label1 = Label(app, image=image1, textvariable=labelText,
# #                font=("Times New Roman", 24),
# #                justify=CENTER, height=4, fg="blue")
# # label1.pack()
#
# app.mainloop()

from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
root = Tk()
root.geometry('400x400')
root.title('My App')

# C = Canvas(top, bg="blue", height=250, width=300)
# filename = ImageTk.PhotoImage(Image.open('money.jpg'))
# background_label = Label(top, image=filename)
# background_label.place(x=0, y=0, relwidth=1, relheight=1)

# print(datetime.now().year)
# print(datetime.now().day)
# print(datetime.now().month)
# print(type(datetime.now().month))

c = Canvas(root, width=400, height=100, bg='blue', bd=0)
bt = Button(c, text='Click 1')
et = Entry(c, width=10, font='none 15')
c.create_window(100,80, window=bt)
c.create_window(250, 80, window=et)
c.grid(row=0, column=0, columnspan=2, sticky=W+E)

c2 = Canvas(root, height=100, bg='red', bd=0)
bt2 = Button(c2, text='Click Here')
et2 = Entry(c2, width=10, font='none 15')
c2.create_window(100, 80, window=bt2)
c2.create_window(250, 80, window=et2)
c2.grid(row=1, column=0, columnspan=2, sticky=W+E)


def update():
    time = dt.now().strftime('%H:%M:%S')
    status_bar_right.config(text=time)
    status_bar_right.after(1000, update)

status_bar_left = Label(root, text='Stuff\nStuff About App',justify='left', font=('consolas', 12), bd=1, relief='sunken')
status_bar_left.grid(row=10, column=0, sticky=W)

global status_bar_right
status_bar_right = Label(root, text='sdsdfd', justify='right', font=('consolas', 12), bd=1, relief='sunken')
status_bar_right.grid(row=10, column=1, sticky=E)
threading.Thread(target=update).start()

pic = ImageTk.PhotoImage(Image.open('images/save3.png'))
top = Toplevel()
lb = Label(top, image=pic)
lb.pack()


root.mainloop()