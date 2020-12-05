from tkinter import *
from PIL import ImageTk, Image


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
top = Tk()
top.geometry('400x400')
top.title('My App')

C = Canvas(top, bg="blue", height=250, width=300)
filename = ImageTk.PhotoImage(Image.open('money.jpg'))
background_label = Label(top, image=filename)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

print(C.keys())

C.pack()
top.mainloop()