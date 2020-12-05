from tkinter import *
from PIL import Image, ImageTk
import openpyxl
import os

# main window configurations
root = Tk()
root.title('TimeTracker')
root.iconbitmap('cat.ico')
# root.configure(bg='#CEFAFA')
# root.configure(bg='#9de6ce')
ROOT_WIDTH = 500
ROOT_HEIGHT = 500
root.geometry(f'{ROOT_WIDTH}x{ROOT_HEIGHT}')
root.minsize(ROOT_WIDTH, ROOT_HEIGHT)
root.maxsize(ROOT_WIDTH+100, ROOT_HEIGHT+200)
# root.attributes('-alpha', 0.9)  # set transparency
# root.wm_attributes('-transparentcolor', '#CEFAFA')


# frames in window
# Top Frame
top_frame = Frame(root, borderwidth=0.1, relief='solid')
top_frame.pack(fill=BOTH, expand=TRUE)
img = ImageTk.PhotoImage(Image.open('clock.jpg').resize((600, 400)), Image.ANTIALIAS)
Label(top_frame, image=img).place(x=0,y=0, relwidth=1, relheight=1)
top_title_label = Label(top_frame, text='Time Started', font=('android 7', 20))
top_title_label.grid(row=0, column=0, padx=120, ipadx=20)  # maybe use pack here




# Midle frame
middle_frame = Frame(root, borderwidth=0.1, relief='solid')
img3 = ImageTk.PhotoImage(Image.open('time2.jpg').resize((600, 400)), Image.ANTIALIAS)
Label(middle_frame, image=img3).place(x=0,y=0, relwidth=1, relheight=1)
middle_frame.pack(fill=BOTH, expand=TRUE)
middle_title_label = Label(middle_frame, text='Time Completed', font=('android 7', 20))
middle_title_label.grid(row=0, column=0, padx=120, ipadx=20)


# Bottom frame
bottom_frame = Frame(root, borderwidth=0.1, relief='solid')
bottom_frame.pack(fill=BOTH, expand=TRUE)
img2 = ImageTk.PhotoImage(Image.open('money.jpg').resize((600, 400)), Image.ANTIALIAS)
Label(bottom_frame, image=img2).place(x=0,y=0, relwidth=1, relheight=1)
bottom_title_label = Label(bottom_frame, text='Payment', font=('android 7', 20))
# bottom_title_label.grid(row=0, column=0, padx=120, ipadx=20)
bottom_title_label.pack(expand=TRUE, anchor=N)  # Grid or pack?

# Status Bar
status = Label(root, text='Current Time: Cur Date and Time here', font=('consolas', 10), bg='#9de6ce', anchor=E)
status.pack(fill=X, side=BOTTOM)

# Put event updates on the left and date and time on the right


if __name__ == '__main__':
    root.mainloop()
