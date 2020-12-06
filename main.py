"""
Author: CHR-onicles
Date: 05/12/2020

DSC UG Python Challenge.
"""

from tkinter import *
from tkcalendar import *
from PIL import Image, ImageTk
from datetime import datetime as dt
import openpyxl
import os
import threading



# MAIN WINDOW CONFIGURATIONS

root = Tk()
root.title('TimeTracker')
root.iconbitmap('cat.ico')
ROOT_WIDTH = 550
ROOT_HEIGHT = 640
root.geometry(f'{ROOT_WIDTH}x{ROOT_HEIGHT}')
root.minsize(ROOT_WIDTH, ROOT_HEIGHT)
# root.maxsize(ROOT_WIDTH, ROOT_HEIGHT)
root.configure(bg='#5fc29e')


# Global variables
# Calendar stuff
cal_window = None
first_time_open = False
date_from_calendar = ''
date_from_calendar2 = ''


# Defining command functions and event functions

def m_focus_in(event):
    """
    Function to change  the middle canvas'  hour and minute spinbox
     foreground colour when hovered on.
    """
    m_hour_spin_box.config(fg='black')
    m_minute_spin_box.config(fg='black')

def m_focus_out(event):
    """
    Function to change middle canvas' hour and minute spinbox foreground colour
    when mouse pointer is no longer hovering on it.
    """
    m_hour_spin_box.config(fg='gray')
    m_minute_spin_box.config(fg='gray')

def t_focus_in(event):
    """
    Function to change the top canvas'  hour and minute spinbox foreground
     colour when hovered on.
    """
    top_hour_spin_box.config(fg='black')
    top_minute_spin_box.config(fg='black')

def t_focus_out(event):
    """
    Function to change top canvas' hour and minute spinbox foreground colour
    when mouse pointer is no longer hovering on it.
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


def calculate_payment_button_hover_in(event):
    """
    Function to change colour and font style of calculate payment button
    when hovered on.
    """
    calc_payment_button.config(font=('consolas', 20, 'italic'), bg='white')


def calculate_payment_button_hover_out(event):
    """
    Function to change calculate payment button's colour and font style
    back to normal when mouse pointer is no longer hovering on the button.
    """
    calc_payment_button.config(font=('consolas', 20), bg='SystemButtonFace')


def open_calendar(canvas):
    """
    Command function to open calendar for user to choose a date.
    :param: canvas
    """

    global first_time_open, cal_window
    # calc_payment_button.config(state=DISABLED)  # Trying to disable calculate payment button when
    #   calendar is open... requires way more code, so will use another kind of check.

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
        cal_window.geometry('250x270')
        cal_window.maxsize(250, 270)
        cal_window.minsize(250, 270)
        cal_window.configure(bg='#5fc29e')

        def get_date():
            """
            Describe function here
            """
            global cal_window, selected_label, date_from_calendar, date_from_calendar2
            if canvas == top_canvas:
                date_from_calendar = cal.get_date()

                # rearranging of date format to: YYYY/MM/DD
                temp = date_from_calendar.split('/')
                temp2 = temp[1] + '/' + temp[0] + '/' + temp[2]
                date_from_calendar = temp2
            elif canvas == middle_canvas:
                date_from_calendar2 = cal.get_date()

                # rearranging of date format to: YYYY/MM/DD
                temp = date_from_calendar2.split('/')
                temp2 = temp[1] + '/' + temp[0] + '/' + temp[2]
                date_from_calendar2 = temp2


            selected_label = Label(cal_window, text='Date Selected!', font=('consolas', 14, 'italic'),
                                   bg='#5fc29e')
            selected_label.pack(pady=5)
            # selected_label.pack_forget()
            submit_button.config(state=DISABLED)

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
    Function to update the time in the status bar through a thread
    """
    cur_time = dt.now().strftime('%H:%M:%S')
    status_bar_right.config(text='System Time(24hrs): ' + cur_time)
    status_bar_right.after(1000, status_bar_time_update)


def confirm_button_click(canvas):
    """
    Describe function here
    :param canvas:
    """
    global date_window, date_window2

    if canvas == top_canvas:
        global selected_date_label, s_time
        if (0 <= int(top_hour_spin_box.get()) <= 9) and (0 <= int(top_minute_spin_box.get()) <= 9):
            s_time = '0' + top_hour_spin_box.get() + ':' + '0' + top_minute_spin_box.get()
        elif 0 <= int(top_minute_spin_box.get()) <= 9:  # append 0 if single number
            s_time = top_hour_spin_box.get() + ':' + '0' + top_minute_spin_box.get()
        elif 0 <= int(top_hour_spin_box.get()) <= 9:
            s_time = '0' + top_hour_spin_box.get() + ':' + top_minute_spin_box.get()
        else:
            s_time = top_hour_spin_box.get() + ':' + top_minute_spin_box.get()
        selected_date_label.config(text='You selected: ' + date_from_calendar + ' ' + s_time)
        date_window = canvas.create_window(225, 170, window=selected_date_label)

    elif canvas == middle_canvas:
        global selected_date_label2, s_time2
        if (0 <= int(m_minute_spin_box.get()) <= 9) and (0 <= int(m_hour_spin_box.get()) <= 9):
            s_time2 = '0' + m_hour_spin_box.get() + ':' + '0' + m_minute_spin_box.get()
        elif 0 <= int(m_minute_spin_box.get()) <= 9:  # append 0 if single number
            s_time2 = m_hour_spin_box.get() + ':' + '0' + m_minute_spin_box.get()
        elif 0 <= int(m_hour_spin_box.get()) <= 9:
            s_time2 = '0' + m_hour_spin_box.get() + ':' + m_minute_spin_box.get()
        else:
            s_time2 = m_hour_spin_box.get() + ':' + m_minute_spin_box.get()
        selected_date_label2.config(text='You selected: ' + date_from_calendar2 + ' ' + s_time2)
        date_window2 = canvas.create_window(225, 170, window=selected_date_label2)


def cancel_button_click(canvas):
    """
    Describe function here
    :param canvas:
    """
    if canvas == middle_canvas:
        global selected_date_label2
        canvas.delete(date_window2)
    elif canvas == top_canvas:
        global selected_date_label
        canvas.delete(date_window)


def payment_calculation():
    """
    Function to calculate payment amount based on the date and time passed in
    by user.
    Rate: $5 for 60mins (1hr)
    """
    # Do nothing with dates for now since both dates(date started and date completed) will be the same.

    global amount_label, calc_payment_button, amount_to_be_paid, invalid_label
    amount_label = bottom_canvas.create_text(250, 150, text='')
    # bottom_canvas.delete(amount_label)
    # Perform operations on hours and minutes only
    # Grabbing hours and minutes
    hour_completed = int(m_hour_spin_box.get())
    minutes_completed = int(m_minute_spin_box.get())
    hour_started = int(top_hour_spin_box.get())
    minutes_started = int(top_minute_spin_box.get())

    hours_elapsed = hour_completed - hour_started
    minutes_elapsed = minutes_completed - minutes_started

    hours_to_mins = hours_elapsed * 60
    total_minutes_elapsed = minutes_elapsed + hours_to_mins
    amount_to_be_paid = round(float(total_minutes_elapsed * 1/12), 2)

    if total_minutes_elapsed < 0:
        invalid_label = bottom_canvas.create_text(280, 150, text='Invalid Information Provided',
                                                  font=('consolas', 16, 'bold'), fill='red')
        calc_payment_button.config(state=DISABLED)
        calc_payment_button.bell()
    else:
        amount_label = bottom_canvas.create_text(260, 150, text='$' + str(amount_to_be_paid),
                                                 font=('consolas', 40, 'bold'))
        calc_payment_button.config(state=DISABLED)

def reset_values():
    """
    Function to reset dates, time and amount calculated.
    """
    global amount_label, date_window, date_window2, calc_payment_button, amount_to_be_paid, invalid_label
    bottom_canvas.delete(amount_label)
    bottom_canvas.delete(invalid_label)
    # middle_canvas.delete(date_window2)
    # top_canvas.delete(date_window)
    calc_payment_button.config(state=NORMAL)



# TOP CANVAS----------------------------------------------------------

top_canvas = Canvas(root, width=ROOT_WIDTH, height=200, borderwidth=0)
top_canvas.grid(row=0, column=0, sticky=W+E, columnspan=2)
img1 = ImageTk.PhotoImage(Image.open('clock.jpg'), Image.ANTIALIAS)
top_canvas.create_image(0, 0, image=img1, anchor=NW)
top_canvas.create_text(270, 30, text='Date/Time Started', font=('android 7', 25))



# Top Canvas Hour Spin Box
top_hour_spin_box = Spinbox(top_canvas, from_=0, to=23, width=2, font=('consolas', 20), fg='gray')
top_canvas.create_window(340, 100, window=top_hour_spin_box)
top_hour_spin_box.bind('<Enter>', t_focus_in)
top_hour_spin_box.bind('<Leave>', t_focus_out)

# Semicolon separating minute from hours
top_canvas.create_text(375, 100, text=':', font=('android 7', 25, 'bold'), fill='white')

# Top Canvas Minute Spin Box
top_minute_spin_box = Spinbox(top_canvas, from_=0, to=59, width=2, font=('consolas', 20), fg='gray')
top_canvas.create_window(410, 100, window=top_minute_spin_box)
top_minute_spin_box.bind('<Enter>',  t_focus_in)
top_minute_spin_box.bind('<Leave>', t_focus_out)

# Time text
top_canvas.create_text(280, 100, text='Time:', font=('consolas', 20))

# Date text
top_canvas.create_text(110, 100, text='Date:', font=('consolas', 20))

# Calendar button for top canvas
t_cal_icon = ImageTk.PhotoImage(Image.open('cal2_icon.png').resize((50,50), Image.ANTIALIAS))
t_calendar_button = Button(top_canvas, image=t_cal_icon, bg='light gray', command=lambda: open_calendar(top_canvas))
top_canvas.create_window(180, 110, window=t_calendar_button)

# Selected date and time text
# global selected_date_label, s_time
s_time = ''
selected_date_label = Label(top_canvas, text='You selected: ' + date_from_calendar + ' ' + s_time,
                            font=('consolas', 20, 'italic', 'bold'))

# Checkmark icon
c_icon = ImageTk.PhotoImage(Image.open('check_icon.png').resize((60, 60), Image.ANTIALIAS))
check_button = Button(top_canvas, image=c_icon, command=lambda: confirm_button_click(top_canvas))
top_canvas.create_window(490, 90, window=check_button)

# Cancel icon
cancel_icon = ImageTk.PhotoImage(Image.open('remove_icon.jpg').resize((60, 60), Image.ANTIALIAS))
cancel_button = Button(top_canvas, image=cancel_icon, command=lambda: cancel_button_click(top_canvas))
top_canvas.create_window(490, 160, window=cancel_button)






# MIDDLE CANVAS--------------------------------------------------------------

middle_canvas = Canvas(root,width=ROOT_WIDTH, height=200, borderwidth=0, bd=0)
# still has slight border cant remove it.
middle_canvas.grid(row=1, column=0, columnspan=2, sticky=W+E)
img2 = ImageTk.PhotoImage(Image.open('time2.jpg').resize((600, 400)), Image.ANTIALIAS)
middle_canvas.create_image(0,0, image=img2, anchor=NW)
middle_canvas.create_text(280, 26, text='Date/Time Completed', font=('android 7', 25), fill='#e8ebea')


# Middle Canvas Hour Spin Box
m_hour_spin_box = Spinbox(middle_canvas, from_=0, to=23, width=2, font=('consolas', 20), fg='gray')
m_hour_spin_box.bind('<Enter>', m_focus_in)
m_hour_spin_box.bind('<Leave>', m_focus_out)
middle_canvas.create_window(340, 100, window=m_hour_spin_box)

# Semicolon separating minute from hours
middle_canvas.create_text(375, 100, text=':', font=('android 7', 25, 'bold'), fill='#e8ebea')

# Middle Canvas Minute Spin Box
m_minute_spin_box = Spinbox(middle_canvas, from_=0, to=59, width=2, font=('consolas', 20), fg='gray')
middle_canvas.create_window(410, 100, window=m_minute_spin_box)
m_minute_spin_box.bind('<Enter>', m_focus_in)
m_minute_spin_box.bind('<Leave>', m_focus_out)

# Time text
middle_canvas.create_text(280, 100, text='Time:', font=('consolas', 20), fill='#e8ebea')
# this hex colour is used because of the background picture of the canvas.

# Date text
middle_canvas.create_text(110, 100, text='Date:', font=('consolas', 20), fill='#e8ebea')

# Calendar button for middle canvas
m_cal_icon = ImageTk.PhotoImage(Image.open('cal2_icon.png').resize((50, 50), Image.ANTIALIAS))
m_calendar_button = Button(middle_canvas, image=m_cal_icon, bg='light gray',
                           command=lambda: open_calendar(middle_canvas))
middle_canvas.create_window(180, 110, window=m_calendar_button)


# Selected date and time text
s_time2 = ''
selected_date_label2 = Label(middle_canvas, text='You selected: ' + date_from_calendar2 + ' ' + s_time2,
                             font=('consolas', 20, 'italic', 'bold'))

# Checkmark icon
c_icon2 = ImageTk.PhotoImage(Image.open('check_icon.png').resize((60, 60), Image.ANTIALIAS))
check_button2 = Button(middle_canvas, image=c_icon2, command=lambda: confirm_button_click(middle_canvas))
middle_canvas.create_window(490, 90, window=check_button2)

# Cancel icon
cancel_icon2 = ImageTk.PhotoImage(Image.open('remove_icon.jpg').resize((60, 60), Image.ANTIALIAS))
cancel_button2 = Button(middle_canvas, image=cancel_icon2, command=lambda: cancel_button_click(middle_canvas))
middle_canvas.create_window(490, 160, window=cancel_button2)







# BOTTOM CANVAS---------------------------------------------------------

bottom_canvas = Canvas(root, width=ROOT_WIDTH, height=200, borderwidth=0)
bottom_canvas.grid(row=2, column=0, columnspan=2, sticky=W+E)
img3 = ImageTk.PhotoImage(Image.open('money.jpg').resize((600,400)), Image.ANTIALIAS)
bottom_canvas.create_image(0, 0, image=img3, anchor=NW)
bottom_canvas.create_text(280, 30, text='Payment', font=('android 7', 25),)

# Calculate Payment Button
calc_payment_button = Button(bottom_canvas, text='Calculate Payment', font=('consolas', 20),
                             command=payment_calculation)
bottom_canvas.create_window(275, 100, window=calc_payment_button)
calc_payment_button.bind('<Enter>', calculate_payment_button_hover_in)
calc_payment_button.bind('<Leave>', calculate_payment_button_hover_out)

# Reset Button
reset_icon = ImageTk.PhotoImage(Image.open('Reset.png').resize((70, 65), Image.ANTIALIAS))
reset_button = Button(bottom_canvas, image=reset_icon, command=reset_values)
bottom_canvas.create_window(60, 160, window=reset_button)


# Save to Excel Button
save_icon = ImageTk.PhotoImage(Image.open('save3.png').resize((70, 65), Image.ANTIALIAS))
save_button = Button(bottom_canvas, image=save_icon)
bottom_canvas.create_window(490, 160, window=save_button)



# TODO: Create money paid label
# TODO: 3. Add save to Excel feature.
#   2. Warning label for wrong input





# Status Bar-------------------------------------------
global left_status_text, date_and_time_text, status_bar
rate_text = 'Rate: 1hr = $5.00'

# Left Status bar text
status_bar_left = Label(root, text=rate_text, font=('consolas', 12), bg='#5fc29e', anchor=W)
status_bar_left.grid(row=3, column=0, sticky=W)


# Right status bar text
status_bar_right = Label(root, text='', font=('consolas', 12), bg='#5fc29e', anchor=E)
status_bar_right.grid(row=3, column=1, sticky=E)

# Thread for status bar time
threading.Thread(target=status_bar_time_update).start()



if __name__ == '__main__':
    root.mainloop()

