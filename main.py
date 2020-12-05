from tkinter import *
from tkcalendar import *
from PIL import Image, ImageTk
from datetime import datetime as dt
import openpyxl
import os
import threading



# main window configurations

root = Tk()
root.title('TimeTracker')
root.iconbitmap('cat.ico')
ROOT_WIDTH = 550
ROOT_HEIGHT = 640
root.geometry(f'{ROOT_WIDTH}x{ROOT_HEIGHT}')
root.minsize(ROOT_WIDTH, ROOT_HEIGHT)
# root.maxsize(ROOT_WIDTH, ROOT_HEIGHT)
root.configure(bg='#5fc29e')
# root.attributes('-alpha', 0.9)  # set transparency

# Global variables
cal_window = None
first_time_open = False



# Defining command functions and event functions

def m_focus_in(event):
    """
    Describe function here
    """
    m_hour_spin_box.config(fg='black')
    m_minute_spin_box.config(fg='black')
    # left_status_text = 'Setting ' # TODO: Add left status text later
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


def submit_button_hover_in(event):
    """
    Binding event function to update submit button in calendar,
    when it is hovered into.
    """
    submit_button.config(bg='white', font=('consolas', 14, 'italic'))


def submit_button_hover_out(event):
    """
    Binding event function to update submit button in calendar,
    when it is hovered out of.
    """
    submit_button.config(bg='SystemButtonFace', font=('consolas', 14))


def get_date():
    print(cal.get_date())


def open_calendar(canvas):
    """
    Command function to open calendar for user to choose a date.
    """

    global first_time_open, cal_window

    def create_calendar_window():
        global first_time_open, cal_window

        # Grabbing current date from system
        year = dt.now().year
        month = dt.now().month
        day = dt.now().day

        # Calendar window configurations
        cal_window = Toplevel()
        cal_window.title('Calendar')
        cal_window.iconbitmap('cat.ico')
        cal_window.geometry('250x250')
        cal_window.configure(bg='#5fc29e')
        # cal_window.attributes('-alpha', 0.9)  # Setting transparency
        global cal
        cal = Calendar(cal_window, selectmode='day', year=year, month=month, day=day)
        cal.pack(fill=BOTH, expand=1)

        # Submit button for calendar
        global submit_button
        submit_button = Button(cal_window, text='Submit', font=('consolas', 14), command=get_date)
        submit_button.pack(pady=(5, 0))
        submit_button.bind('<Enter>', submit_button_hover_in)
        submit_button.bind('<Leave>', submit_button_hover_out)
        first_time_open = True

    if first_time_open == False:  # Opened calendar window for the first time
        create_calendar_window()

    else:
        if cal_window.winfo_exists():  # Calendar window is still open
            first_time_open = True
        else:  # Calendar window was opened but closed.
            create_calendar_window()


def status_bar_time_update():
    """
    Function to update the time in the status bar.
    """
    cur_time = dt.now().strftime('%H:%M:%S')
    status_bar_right.config(text='System Time: ' + cur_time)
    status_bar_right.after(1000, status_bar_time_update)


        
    
    




# TOP CANVAS
global top_canvas
top_canvas = Canvas(root, width=ROOT_WIDTH, height=200, borderwidth=0)
top_canvas.grid(row=0, column=0, sticky=W+E, columnspan=2)
img1 = ImageTk.PhotoImage(Image.open('clock.jpg'), Image.ANTIALIAS)
top_canvas.create_image(0,0, image=img1, anchor=NW)
top_canvas.create_text(270, 40, text='Time Started', font=('android 7', 25))



# Top Canvas Hour Spin Box
global top_hour_spin_box, top_minute_spin_box
top_hour_spin_box = Spinbox(top_canvas, from_=0, to=23, width=2, font=('consolas', 20), fg='gray')
top_canvas.create_window(400, 100, window=top_hour_spin_box)
top_hour_spin_box.bind('<Enter>', t_focus_in)
top_hour_spin_box.bind('<Leave>', t_focus_out)

# Semicolon separating minute from hours
top_canvas.create_text(435, 100, text=':', font=('android 7', 25, 'bold'), fill='white')

# Top Canvas Minute Spin Box
top_minute_spin_box = Spinbox(top_canvas, from_=0, to=59, width=2, font=('consolas', 20), fg='gray')
top_canvas.create_window(470, 100, window=top_minute_spin_box)
top_minute_spin_box.bind('<Enter>',  t_focus_in)
top_minute_spin_box.bind('<Leave>', t_focus_out)

# Time text
top_canvas.create_text(340, 100, text='Time:', font=('consolas', 20))

# Date text
top_canvas.create_text(110, 100, text='Date:', font=('consolas', 20))

# Calendar button for top canvas
global t_calendar_button
t_cal_icon = ImageTk.PhotoImage(Image.open('cal2_icon.png').resize((50,50), Image.ANTIALIAS))
t_calendar_button = Button(top_canvas, image=t_cal_icon, bg='light gray', command=lambda: open_calendar(top_canvas))
top_canvas.create_window(180, 110, window=t_calendar_button)  # TODO: Later add hover over bind event.





# MIDDLE CANVAS

middle_canvas = Canvas(root,width=ROOT_WIDTH, height=200, borderwidth=0, bd=0)  # still has slight border cant remove it.
middle_canvas.grid(row=1, column=0, columnspan=2, sticky=W+E)
img2 = ImageTk.PhotoImage(Image.open('time2.jpg').resize((600,400)), Image.ANTIALIAS)
middle_canvas.create_image(0,0, image=img2, anchor=NW)
middle_canvas.create_text(280, 40, text='Time Completed', font=('android 7', 25), fill='#e8ebea')


# Middle Canvas Hour Spin Box
global m_hour_spin_box, m_minute_spin_box
m_hour_spin_box = Spinbox(middle_canvas, from_=0, to=23, width=2, font=('consolas', 20), fg='gray')
m_hour_spin_box.bind('<Enter>', m_focus_in)
m_hour_spin_box.bind('<Leave>', m_focus_out)
middle_canvas.create_window(400, 100, window=m_hour_spin_box)

# Semicolon separating minute from hours
middle_canvas.create_text(435, 100, text=':', font=('android 7', 25, 'bold'), fill='#e8ebea')

# Middle Canvas Minute Spin Box
m_minute_spin_box = Spinbox(middle_canvas, from_=0, to=59, width=2, font=('consolas', 20), fg='gray')
middle_canvas.create_window(470, 100, window=m_minute_spin_box)
m_minute_spin_box.bind('<Enter>', m_focus_in)
m_minute_spin_box.bind('<Leave>', m_focus_out)

# Time text
middle_canvas.create_text(340, 100, text='Time:', font=('consolas', 20), fill='#e8ebea')
# this hex colour is used because of the background picture of the canvas.

# Date text
middle_canvas.create_text(110, 100, text='Date:', font=('consolas', 20), fill='#e8ebea')

# Calendar button for middle canvas
global m_calendar_button
m_cal_icon = ImageTk.PhotoImage(Image.open('cal2_icon.png').resize((50,50), Image.ANTIALIAS))
m_calendar_button = Button(middle_canvas, image=m_cal_icon, bg='light gray', command=lambda: open_calendar(middle_canvas))
middle_canvas.create_window(180, 110, window=m_calendar_button)  # TODO: Later add hover over bind event.

# TODO:
#           2. Add payment label and calculation stuff.
#           3. Add save to Excel feature.


# Bottom Canvas
bottom_canvas = Canvas(root, width=ROOT_WIDTH, height=200, borderwidth=0)
bottom_canvas.grid(row=2, column=0, columnspan=2, sticky=W+E)
img3 = ImageTk.PhotoImage(Image.open('money.jpg').resize((600,400)), Image.ANTIALIAS)
bottom_canvas.create_image(0,0, image=img3, anchor=NW)
bottom_canvas.create_text(280, 40, text='Payment', font=('android 7', 25),)

# Calculate Payment Button
calc_payment_button = Button(bottom_canvas, text='Calculate Payment', font=('consolas',20))
bottom_canvas.create_window(270, 100, window=calc_payment_button)

#TODO: Create money paid label
# 2. Warning label for wrong input





# Status Bar
global left_status_text, rate_text, date_and_time_text, status_bar
rate_text = 'Rate: 1hr = $5.00'

# Left Status bar text
status_bar_left = Label(root, text=rate_text, font=('consolas', 12), bg='#5fc29e', anchor=W)
status_bar_left.grid(row=3, column=0, sticky=W)


# Right status bar text
status_bar_right = Label(root, text='', font=('consolas', 12), bg='#5fc29e', anchor=E)
status_bar_right.grid(row=3, column=1, sticky=E)  # TODO: Break into 2 parts.
# Thread for status bar time
threading.Thread(target=status_bar_time_update).start()


# Put event updates on the left and date and time on the right
# Event updates in Status Bar



if __name__ == '__main__':
    root.mainloop()

