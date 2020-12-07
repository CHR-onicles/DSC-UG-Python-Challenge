"""
Author: CHR-onicles©
Date: 05/12/2020

DSC UG Python Challenge - Time Tracker App.
"""

from tkinter import *
from tkcalendar import *
from tkinter.filedialog import askdirectory
from tkinter import messagebox
from PIL import Image, ImageTk
from datetime import datetime as dt
import openpyxl
import os
import threading

# MAIN WINDOW CONFIGURATIONS

root = Tk()
root.title('TimeTracker')
root.iconbitmap('images/cat.ico')
ROOT_WIDTH = 550
ROOT_HEIGHT = 640
root.geometry(f'{ROOT_WIDTH}x{ROOT_HEIGHT}')
root.minsize(ROOT_WIDTH, ROOT_HEIGHT)  # Preventing user from increasing or reducing app size
root.maxsize(ROOT_WIDTH, ROOT_HEIGHT)  # as most widgets are statically placed!
root.configure(bg='#5fc29e')  # turquoise-ish colour used in status bar and calendar too.

# GLOBAL VARIABLES------------

# Calendar stuff
cal_window = None
first_time_open = False
date_from_calendar = ''
date_from_calendar2 = ''

# Status bar text
rate_text = 'Rate: 1hr = $5.00'

# Payment calculation variable
amount_to_be_paid = 0.0

# Excel stuff
excel_first_time_open = 0


# -----------------------------

# DEFINING BINDING EVENT FUNCTIONS

def spin_box_hover_in(event, spin_box):
    """
    Function to change the spinbox's foreground colour and status bar when hovered on.

    :param event: necessary argument in order for binding event to work.
    :param spin_box: spin box object that is passed in to be updated.
    """
    spin_box.config(fg='black')

    # I couldn't find a simpler way to do the code below
    if spin_box == root.winfo_children()[0].winfo_children()[0] \
            or spin_box == root.winfo_children()[1].winfo_children()[0]:  # Simply if spin box in focus is the hour
        status_bar_left.config(text='Set the hour...', font=('consolas', 12, 'italic'))

    elif spin_box == root.winfo_children()[0].winfo_children()[1] \
            or spin_box == root.winfo_children()[1].winfo_children()[1]:  # Simply if spin box in focus is the minutes
        status_bar_left.config(text='Set the minutes...', font=('consolas', 12, 'italic'))


def spin_box_hover_out(event, spin_box):
    """
    Function to change the spinbox's foreground color back to normal.

    :param event: necessary argument in order for binding event to work.
    :param spin_box: spin box object that is passed in to be updated.
    """
    spin_box.config(fg='gray')
    status_bar_left.config(text=rate_text, font=('consolas', 12))


def submit_button_hover_in(event):
    """
    Binding event function to update submit button in calendar,
    when it is hovered on.
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
    Function to change colour and font style of calculate payment button and status bar
    when hovered on.
    """
    calc_payment_button.config(font=('consolas', 20, 'italic'), bg='white')
    status_bar_left.config(text='Calculate payment based on info provided...', font=('consolas', 10, 'italic'))


def calculate_payment_button_hover_out(event):
    """
    Function to change calculate payment button's colour, font style and status bar
    back to normal when mouse pointer is no longer hovering on the button.
    """
    calc_payment_button.config(font=('consolas', 20), bg='SystemButtonFace')
    status_bar_left.config(text=rate_text, font=('consolas', 12))


def save_button_hover_in(event):
    """
    Binding event function to update save button's color, size and status bar
    when mouse pointer hovers on it.
    """
    global save_icon, save_button, sb_window
    bottom_canvas.delete(sb_window)
    save_icon = ImageTk.PhotoImage(Image.open('images/save3.png').resize((70, 65), Image.ANTIALIAS))
    save_button = Button(bottom_canvas, image=save_icon, command=save_to_excel)
    sb_window = bottom_canvas.create_window(490, 160, window=save_button)
    save_button.bind('<Leave>', save_button_hover_out)

    # Update status bar
    status_bar_left.config(text='Save payment info to excel file...', font=('consolas', 11, 'italic'))


def save_button_hover_out(event):
    """
    Binding event function to return save button to normal when hovered out of.
    """
    global save_icon, save_button, sb_window
    bottom_canvas.delete(sb_window)
    save_icon = ImageTk.PhotoImage(Image.open('images/save3.png').resize((65, 60), Image.ANTIALIAS))
    save_button = Button(bottom_canvas, image=save_icon, bg='SystemButtonFace', command=save_to_excel)
    sb_window = bottom_canvas.create_window(490, 160, window=save_button)
    save_button.bind('<Enter>', save_button_hover_in)

    # Update status bar again
    status_bar_left.config(text=rate_text, font=('consolas', 12))


def reset_button_hover_in(event):
    """
    Function to update reset button and status bar when hovered on.
    """
    global reset_icon, reset_button, r_window
    bottom_canvas.delete(r_window)
    reset_icon = ImageTk.PhotoImage(Image.open('images/Reset.png').resize((65, 65), Image.ANTIALIAS))
    reset_button = Button(bottom_canvas, image=reset_icon, command=reset_values)
    r_window = bottom_canvas.create_window(60, 160, window=reset_button)
    reset_button.bind('<Leave>', reset_button_hover_out)

    # Update status bar
    status_bar_left.config(text='Reset calculation...', font=('consolas', 12, 'italic'))


def reset_button_hover_out(event):
    """
    Function to update reset button and status bar back to normal when hovered out of.
    """
    global reset_icon, reset_button, r_window
    bottom_canvas.delete(r_window)
    reset_icon = ImageTk.PhotoImage(Image.open('images/Reset.png').resize((60, 60), Image.ANTIALIAS))
    reset_button = Button(bottom_canvas, image=reset_icon, command=reset_values)
    r_window = bottom_canvas.create_window(60, 160, window=reset_button)
    reset_button.bind('<Enter>', reset_button_hover_in)

    # Update status bar
    status_bar_left.config(text=rate_text, font=('consolas', 12))


def calendar_button_hover_in(event, canvas):
    """
    Function to update the calendar button when it is hovered on.
    """

    # Created 2 separate instances because of conflict between them when they both use the same resources.
    if canvas == root.winfo_children()[0]:  # this is top canvas
        global cl_window, calendar_button, cal_icon
        canvas.delete(cl_window)
        cal_icon = ImageTk.PhotoImage(Image.open('images/cal2_icon.png').resize((55, 55), Image.ANTIALIAS))
        calendar_button = Button(canvas, image=cal_icon, bg='light gray', command=lambda: open_calendar(canvas))
        cl_window = canvas.create_window(180, 110, window=calendar_button)
        calendar_button.bind('<Leave>', lambda e: calendar_button_hover_out(e, canvas))

    else:
        global cl_window2, cale_icon, calendar_button2
        canvas.delete(cl_window2)
        cale_icon = ImageTk.PhotoImage(Image.open('images/cal2_icon.png').resize((55, 55), Image.ANTIALIAS))
        calendar_button2 = Button(canvas, image=cale_icon, bg='light gray', command=lambda: open_calendar(canvas))
        cl_window2 = canvas.create_window(180, 110, window=calendar_button2)
        calendar_button2.bind('<Leave>', lambda e: calendar_button_hover_out(e, canvas))

    status_bar_left.config(text='Pick a date from the calendar...', font=('consolas', 12, 'italic'))


def calendar_button_hover_out(event, canvas):
    """
    Function to update the calendar button when it is hovered out of.
    """
    if canvas == root.winfo_children()[0]:  # top canvas
        global cl_window, calendar_button, cal_icon
        canvas.delete(cl_window)
        cal_icon = ImageTk.PhotoImage(Image.open('images/cal2_icon.png').resize((50, 50), Image.ANTIALIAS))
        calendar_button = Button(canvas, image=cal_icon, bg='light gray', command=lambda: open_calendar(canvas))
        cl_window = canvas.create_window(180, 110, window=calendar_button)
        calendar_button.bind('<Enter>', lambda e: calendar_button_hover_in(e, canvas))

    else:
        global cl_window2, cale_icon, calendar_button2
        canvas.delete(cl_window2)
        cale_icon = ImageTk.PhotoImage(Image.open('images/cal2_icon.png').resize((50, 50), Image.ANTIALIAS))
        calendar_button2 = Button(canvas, image=cale_icon, bg='light gray', command=lambda: open_calendar(canvas))
        cl_window2 = canvas.create_window(180, 110, window=calendar_button2)
        calendar_button2.bind('<Enter>', lambda e: calendar_button_hover_in(e, canvas))

    status_bar_left.config(text=rate_text)


def confirm_button_hover_in(event, canvas):
    """
    Function to update the confirm button when it is hovered on.
    """
    pass


def confirm_button_hover_out(event, canvas):
    """
    Function to update the confirm button when it is hovered out of.
    """
    pass


def cancel_button_hover_in(event, canvas):
    """
    Function to update the cancel button when it is hovered on.
    """
    pass

def cancel_button_hover_out(event, canvas):
    """
    Function to update the cancel button when it is hovered out of.
    """
    pass



# DEFINING COMMAND FUNCTIONS

def open_calendar(canvas):
    """
    Command function to open calendar for user to choose a date.

    :param: canvas: canvas object for the function to know which canvas called it and
                    give it specific attributes.
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
        cal_window.iconbitmap('images/cat.ico')
        cal_window.geometry('250x270')
        cal_window.maxsize(250, 270)
        cal_window.minsize(250, 270)
        cal_window.configure(bg='#5fc29e')

        def get_date():
            """
            Based on the canvas argument from outer function, this function
            updates a global variable on the date got from the calendar.
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
    Function to update the time in the status bar through a thread.
    """
    cur_time = dt.now().strftime('%H:%M:%S')
    status_bar_right.config(text='|System Time(24h): ' + cur_time)
    status_bar_right.after(1000, status_bar_time_update)


def confirm_button_click(canvas):
    """
    Command function to display user's choice of date and time on the canvas provided.

    :param canvas: canvas object to know which canvas called it and attribute specific
                    configurations to it or some other global variables.
    """
    global date_window, date_window2

    if canvas == top_canvas:
        global selected_date_label, s_time

        if len(top_hour_spin_box.get()) > 2 or len(top_minute_spin_box.get()) > 2:
            messagebox.showerror(title='INVALID INPUT', message='TIME ENTERED IS INVALID')

        else:
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

        if len(m_hour_spin_box.get()) > 2 or len(m_minute_spin_box.get()) > 2:
            messagebox.showerror(title='INVALID INPUT', message='TIME ENTERED IS INVALID')

        else:
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
    Command function to remove label/text telling user his choice of date and time.

    :param canvas: canvas object to know which canvas called it and update specific labels.
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
    invalid_label = bottom_canvas.create_text(250, 150, text='')

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
    amount_to_be_paid = round(float(total_minutes_elapsed * 1 / 12), 2)

    if total_minutes_elapsed < 0:
        messagebox.showerror(title='INVALID ARGUMENT', message='INVALID INFORMATION ENTERED!')
        calc_payment_button.config(state=DISABLED)
    else:
        amount_label = bottom_canvas.create_text(270, 150, text='$' + str(amount_to_be_paid),
                                                 font=('consolas', 40, 'bold'), fill='#e8ebea')
        calc_payment_button.config(state=DISABLED)


def reset_values():
    """
    Function to reset dates, time and amount calculated.
    """
    global calc_payment_button
    bottom_canvas.delete(amount_label)
    bottom_canvas.delete(invalid_label)
    middle_canvas.delete(date_window2)
    top_canvas.delete(date_window)
    calc_payment_button.config(state=NORMAL)


def save_to_excel():
    """
    Function to save date/time started and completed and payment calculated
    to an excel file.
    """
    global excel_first_time_open, amount_to_be_paid

    def create_new_file():
        """
        Function to create new excel file and input information from app.
        """
        workbook = openpyxl.Workbook()
        sheet = workbook['Sheet']

        # Column headers
        sheet['A1'] = 'Date Started'
        sheet['B1'] = 'Time Started'
        sheet['C1'] = 'Date Completed'
        sheet['D1'] = 'Time Completed'
        sheet['E1'] = 'Calculated Payment'
        sheet['F1'] = 'Time Info was Saved'

        # Increase width for better view
        for cols in ['A', 'B', 'C', 'D', 'E', 'F']:
            sheet.column_dimensions[cols].width = 20

        # This is the first time so we can write specifically to certain cells
        sheet['A2'] = date_from_calendar
        sheet['B2'] = s_time
        sheet['C2'] = date_from_calendar2
        sheet['D2'] = s_time2
        sheet['E2'] = '$' + str(amount_to_be_paid)
        sheet['F2'] = dt.now().strftime('%d/%m/%Y, %H:%M:%S')

        # Save excel file and close it
        workbook.save('payment_history.xlsx')
        workbook.close()

        # Message box for successful entry
        messagebox.showinfo(title='Save To Excel File', message='Information saved successfully to excel file!')

    def edit_existing_file():
        """
        Function to edit already existing excel file and input info from app.
        """
        workbook = openpyxl.load_workbook('payment_history.xlsx')
        sheet = workbook['Sheet']

        found_available_cell = False
        row_num = 0
        for row in sheet.iter_rows(min_row=1, max_row=100, min_col=1, max_col=6):
            row_num += 1
            for count, cell in enumerate(row):

                # if all cells in a row are empty, then that row is available for writing
                if cell.value is None and cell == row[-1]:
                    sheet.cell(row=row_num, column=1).value = date_from_calendar
                    sheet.cell(row=row_num, column=2).value = s_time
                    sheet.cell(row=row_num, column=3).value = date_from_calendar2
                    sheet.cell(row=row_num, column=4).value = s_time2
                    sheet.cell(row=row_num, column=5).value = '$' + str(amount_to_be_paid)
                    sheet.cell(row=row_num, column=6).value = dt.now().strftime('%d/%m/%Y, %H:%M:%S')
                    found_available_cell = True
                    break
                elif cell.value is not None:  # if any cell contains information, break
                    break
            if found_available_cell == True:
                break

        # Save and close excel file
        workbook.save('payment_history.xlsx')
        workbook.close()
        messagebox.showinfo(title='Save To Excel File', message='Information saved successfully to excel file!')

    # Main Excel Logic
    if excel_first_time_open == 0:  # Save button has not been clicked already
        dir_location = askdirectory(initialdir='.\\', title='Select Directory To Save To')

        # Change location to the user-chosen one
        os.chdir(dir_location)

        # Search for already existing file
        for item in os.listdir():
            if item != 'payment_history.xlsx' and item == os.listdir()[-1]:
                create_new_file()

            elif item == 'payment_history.xlsx':
                edit_existing_file()
                break
    else:
        edit_existing_file()

    excel_first_time_open += 1


# TOP CANVAS------------------------------------------------------------------------------------

top_canvas = Canvas(root, width=ROOT_WIDTH, height=200, borderwidth=0)
top_canvas.grid(row=0, column=0, sticky=W + E, columnspan=2)
img1 = ImageTk.PhotoImage(Image.open('images/clock_dark.jfif'), Image.ANTIALIAS)
top_canvas.create_image(0, 0, image=img1, anchor=NW)
top_canvas.create_text(270, 30, text='Date/Time Started', font=('android 7', 25))

# Top Canvas Hour Spin Box
top_hour_spin_box = Spinbox(top_canvas, from_=0, to=23, width=2, font=('consolas', 20), fg='gray')
top_canvas.create_window(340, 100, window=top_hour_spin_box)
top_hour_spin_box.bind('<Enter>', lambda event: spin_box_hover_in(event, top_hour_spin_box))
top_hour_spin_box.bind('<Leave>', lambda event: spin_box_hover_out(event, top_hour_spin_box))

# Semicolon separating minute from hours
top_canvas.create_text(375, 100, text=':', font=('android 7', 25, 'bold'), fill='white')

# Top Canvas Minute Spin Box
top_minute_spin_box = Spinbox(top_canvas, from_=0, to=59, width=2, font=('consolas', 20), fg='gray')
top_canvas.create_window(410, 100, window=top_minute_spin_box)
top_minute_spin_box.bind('<Enter>', lambda event: spin_box_hover_in(event, top_minute_spin_box))
top_minute_spin_box.bind('<Leave>', lambda event: spin_box_hover_out(event, top_minute_spin_box))

# Time text
top_canvas.create_text(280, 100, text='Time:', font=('consolas', 20))

# Date text
top_canvas.create_text(110, 100, text='Date:', font=('consolas', 20))

# Calendar button for top canvas
t_cal_icon = ImageTk.PhotoImage(Image.open('images/cal2_icon.png').resize((50, 50), Image.ANTIALIAS))
t_calendar_button = Button(top_canvas, image=t_cal_icon, bg='light gray', command=lambda: open_calendar(top_canvas))
cl_window = top_canvas.create_window(180, 110, window=t_calendar_button)
t_calendar_button.bind('<Enter>', lambda event: calendar_button_hover_in(event, top_canvas))
t_calendar_button.bind('<Leave>', lambda event: calendar_button_hover_out(event, top_canvas))

# Selected date and time text
s_time = ''
selected_date_label = Label(top_canvas, text='You selected: ' + date_from_calendar + ' ' + s_time,
                            font=('consolas', 20, 'italic', 'bold'))

# Checkmark icon
c_icon = ImageTk.PhotoImage(Image.open('images/check_icon.png').resize((60, 60), Image.ANTIALIAS))
check_button = Button(top_canvas, image=c_icon, command=lambda: confirm_button_click(top_canvas))
top_canvas.create_window(490, 90, window=check_button)

# Cancel icon
cancel_icon = ImageTk.PhotoImage(Image.open('images/remove_icon.jpg').resize((60, 60), Image.ANTIALIAS))
cancel_button = Button(top_canvas, image=cancel_icon, command=lambda: cancel_button_click(top_canvas))
top_canvas.create_window(490, 160, window=cancel_button)

# MIDDLE CANVAS--------------------------------------------------------------

middle_canvas = Canvas(root, width=ROOT_WIDTH, height=200, borderwidth=0)
middle_canvas.grid(row=1, column=0, columnspan=2, sticky=W + E)
img2 = ImageTk.PhotoImage(Image.open('images/time_dark.jfif').resize((600, 400)), Image.ANTIALIAS)
middle_canvas.create_image(0, 0, image=img2, anchor=NW)
middle_canvas.create_text(280, 26, text='Date/Time Completed', font=('android 7', 25), fill='#e8ebea')

# Middle Canvas Hour Spin Box
m_hour_spin_box = Spinbox(middle_canvas, from_=0, to=23, width=2, font=('consolas', 20), fg='gray')
m_hour_spin_box.bind('<Enter>', lambda event: spin_box_hover_in(event, m_hour_spin_box))
m_hour_spin_box.bind('<Leave>', lambda event: spin_box_hover_out(event, m_hour_spin_box))
middle_canvas.create_window(340, 100, window=m_hour_spin_box)

# Semicolon separating minute from hours
middle_canvas.create_text(375, 100, text=':', font=('android 7', 25, 'bold'), fill='#e8ebea')

# Middle Canvas Minute Spin Box
m_minute_spin_box = Spinbox(middle_canvas, from_=0, to=59, width=2, font=('consolas', 20), fg='gray')
middle_canvas.create_window(410, 100, window=m_minute_spin_box)
m_minute_spin_box.bind('<Enter>', lambda event: spin_box_hover_in(event, m_minute_spin_box))
m_minute_spin_box.bind('<Leave>', lambda event: spin_box_hover_out(event, m_minute_spin_box))

# Time text
middle_canvas.create_text(280, 100, text='Time:', font=('consolas', 20), fill='#e8ebea')
# this hex colour is used because of the background picture of the canvas.

# Date text
middle_canvas.create_text(110, 100, text='Date:', font=('consolas', 20), fill='#e8ebea')

# Calendar button for middle canvas
m_cal_icon = ImageTk.PhotoImage(Image.open('images/cal2_icon.png').resize((50, 50), Image.ANTIALIAS))
m_calendar_button = Button(middle_canvas, image=m_cal_icon, bg='light gray',
                           command=lambda: open_calendar(middle_canvas))
cl_window2 = middle_canvas.create_window(180, 110, window=m_calendar_button)
m_calendar_button.bind('<Enter>', lambda event: calendar_button_hover_in(event, middle_canvas))
m_calendar_button.bind('<Leave>', lambda event: calendar_button_hover_out(event, middle_canvas))

# Selected date and time text
s_time2 = ''
selected_date_label2 = Label(middle_canvas, text='You selected: ' + date_from_calendar2 + ' ' + s_time2,
                             font=('consolas', 20, 'italic', 'bold'))

# Checkmark icon
c_icon2 = ImageTk.PhotoImage(Image.open('images/check_icon.png').resize((60, 60), Image.ANTIALIAS))
check_button2 = Button(middle_canvas, image=c_icon2, command=lambda: confirm_button_click(middle_canvas))
middle_canvas.create_window(490, 90, window=check_button2)

# Cancel icon
cancel_icon2 = ImageTk.PhotoImage(Image.open('images/remove_icon.jpg').resize((60, 60), Image.ANTIALIAS))
cancel_button2 = Button(middle_canvas, image=cancel_icon2, command=lambda: cancel_button_click(middle_canvas))
middle_canvas.create_window(490, 160, window=cancel_button2)

# BOTTOM CANVAS-----------------------------------------------------------------------------------

bottom_canvas = Canvas(root, width=ROOT_WIDTH, height=200, borderwidth=0)
bottom_canvas.grid(row=2, column=0, columnspan=2, sticky=W + E)
img3 = ImageTk.PhotoImage(Image.open('images/money_dark.jfif').resize((600, 400)), Image.ANTIALIAS)
bottom_canvas.create_image(0, 0, image=img3, anchor=NW)
bottom_canvas.create_text(280, 30, text='Payment', font=('android 7', 25), )

# Calculate Payment Button
calc_payment_button = Button(bottom_canvas, text='Calculate Payment', font=('consolas', 20),
                             command=payment_calculation)
bottom_canvas.create_window(275, 100, window=calc_payment_button)
calc_payment_button.bind('<Enter>', calculate_payment_button_hover_in)
calc_payment_button.bind('<Leave>', calculate_payment_button_hover_out)

# Reset Button
reset_icon = ImageTk.PhotoImage(Image.open('images/Reset.png').resize((60, 60), Image.ANTIALIAS))
reset_button = Button(bottom_canvas, image=reset_icon, command=reset_values)
r_window = bottom_canvas.create_window(60, 160, window=reset_button)
reset_button.bind('<Enter>', reset_button_hover_in)
reset_button.bind('<Leave>', reset_button_hover_out)

# Save to Excel Button
save_icon = ImageTk.PhotoImage(Image.open('images/save3.png').resize((65, 60), Image.ANTIALIAS))
save_button = Button(bottom_canvas, image=save_icon, command=save_to_excel)
sb_window = bottom_canvas.create_window(490, 160, window=save_button)
save_button.bind('<Enter>', save_button_hover_in)
save_button.bind('<Leave>', save_button_hover_out)

# STATUS BAR--------------------------------------------------------------------------------
global left_status_text, date_and_time_text, status_bar

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

    # TODO: 3. Maybe change button and label locations for top and middle canvas.
    #       4. Add 'get current time' button. - HIGH PRIORITY
    #       5. Update left section of status bar when mouse pointer hovers on checkmark and cancel buttons.
