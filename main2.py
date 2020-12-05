from tkinter import *
from tkcalendar import *
from PIL import Image, ImageTk
from datetime import datetime
import openpyxl
import os



# main window configurations

root = Tk()
root.title('TimeTracker')
root.iconbitmap('cat.ico')
# root.configure(bg='#CEFAFA')
# root.configure(bg='#9de6ce')
ROOT_WIDTH = 550
ROOT_HEIGHT = 600
root.geometry(f'{ROOT_WIDTH}x{ROOT_HEIGHT}')
root.minsize(ROOT_WIDTH, ROOT_HEIGHT)
root.maxsize(ROOT_WIDTH, ROOT_HEIGHT)
# root.attributes('-alpha', 0.9)  # set transparency
# root.wm_attributes('-transparentcolor', '#CEFAFA')



# Defining command functions

def m_focus_in(event):
    """
    Describe function here
    """
    m_hour_spin_box.config(fg='black')
    m_minute_spin_box.config(fg='black')
def m_focus_out(event):
    """
    Describe function here
    """
    m_hour_spin_box.config(fg='gray')
    m_minute_spin_box.config(fg='gray')

def t_focus_in(event):
    """

    :param event:
    :return:
    """
    top_hour_spin_box.config(fg='black')
    top_minute_spin_box.config(fg='black')

def t_focus_out(event):
    """

    :param event:
    :return:
    """
    top_hour_spin_box.config(fg='gray')
    top_minute_spin_box.config(fg='gray')


# TOP CANVAS

top_canvas = Canvas(root, width=100, height=100, borderwidth=0)
top_canvas.pack(fill=BOTH, expand=1)
img1 = ImageTk.PhotoImage(Image.open('clock.jpg'), Image.ANTIALIAS)
top_canvas.create_image(0,0, image=img1, anchor=NW)
top_canvas.create_text(270, 40, text='Time Started', font=('android 7', 25))


# Top Canvas spinboxes

global top_hour_spin_box, top_minute_spin_box
top_hour_spin_box = Spinbox(top_canvas, from_=0, to=23, width=2, font=('consolas', 20), fg='gray')
top_canvas.create_window(400, 100, window=top_hour_spin_box)
top_hour_spin_box.bind('<FocusIn>', t_focus_in)
top_hour_spin_box.bind('<FocusOut>', t_focus_out)

# Semicolon separating minute from hours
top_canvas.create_text(435, 100, text=':', font=('android 7', 25, 'bold'), fill='white')

top_minute_spin_box = Spinbox(top_canvas, from_=0, to=59, width=2, font=('consolas', 20), fg='gray')
top_canvas.create_window(470, 100, window=top_minute_spin_box)
top_minute_spin_box.bind('<FocusIn>', t_focus_in)
top_minute_spin_box.bind('<FocusOut>', t_focus_out)






# MIDDLE CANVAS

middle_canvas = Canvas(root, width=100, height=100, borderwidth=0, bd=0)  # still has slight border cant remove it.
middle_canvas.pack(fill=BOTH, expand=1)
img2 = ImageTk.PhotoImage(Image.open('time2.jpg').resize((600,400)), Image.ANTIALIAS)
middle_canvas.create_image(0,0, image=img2, anchor=NW)
middle_canvas.create_text(280, 40, text='Time Completed', font=('android 7', 25), fill='white')


# Middle Canvas spinboxes
global m_hour_spin_box, m_minute_spin_box
m_hour_spin_box = Spinbox(middle_canvas, from_=0, to=23, width=2, font=('consolas', 20), fg='gray')
m_hour_spin_box.bind('<FocusIn>', m_focus_in)
m_hour_spin_box.bind('<FocusOut>', m_focus_out)
middle_canvas.create_window(400, 100, window=m_hour_spin_box)

# Semicolon separating minute from hours
middle_canvas.create_text(435, 100, text=':', font=('android 7', 25, 'bold'), fill='white')

m_minute_spin_box = Spinbox(middle_canvas, from_=0, to=59, width=2, font=('consolas', 20), fg='gray')
middle_canvas.create_window(470, 100, window=m_minute_spin_box)
m_minute_spin_box.bind('<FocusIn>', m_focus_in)
m_minute_spin_box.bind('<FocusOut>', m_focus_out)






# Bottom Canvas
bottom_canvas = Canvas(root, width=100, height=100, borderwidth=0)
bottom_canvas.pack(fill=BOTH, expand=1)
img3 = ImageTk.PhotoImage(Image.open('money.jpg').resize((600,400)), Image.ANTIALIAS)
bottom_canvas.create_image(0,0, image=img3, anchor=NW)
bottom_canvas.create_text(290, 40, text='Payment', font=('android 7', 25),)







# Status Bar
status = Label(root, text='Current Time: Cur Date and Time here', font=('consolas', 10), bg='#9de6ce', anchor=E)
status.pack(fill=X, side=BOTTOM)

# Put event updates on the left and date and time on the right
# Event updates in Status Bar



if __name__ == '__main__':
    root.mainloop()