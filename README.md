# DSC UG PYTHON CHALLENGE

App to calculate the amount a person earns per
the time spent teaching.

## REQUIREMENTS:
- Pip install [Openpyxl](https://pypi.org/project/openpyxl/)
- Pip install [Pillow](https://pypi.org/project/Pillow/)
- Pip install [tkCalendar](https://pypi.org/project/tkcalendar/1.1.5/)


## About App:
- ### General:
    This is a GUI-based app using tkinter with Python. It contains widgets that are <b>statically</b>
    placed on 3 canvases(`top_canvas`, `middle_canvas` and `bottom_canvas`) in the app, therefore trying
    to resize the app would not work.

- ### Status Bar:
    The App contains a status bar which is divided into **2 sections**: The **left
    section** which gives information on a button if the mouse pointer hovers over it, and the **right section** which 
    constantly tells the system time using a threaded function.

- ### Buttons and Spinboxes:
    The App contains **12** total **clickable** and **animated** buttons which have various functions
    and give information on their use when you hover over them,
    as well as **2** spinboxes.


- *Calendar Buttons*:
    
    Both buttons open a small calendar window which defaults to the current date, but the user can 
    select whichever date he pleases - past or future. After which, the user is required to click on the **Submit Button**.
  
  
- *Checkmark Buttons*:
  
  Both buttons confirm the user's selection of time and date from the **spinboxes** and **calendar** 
  respectively. They will override the time selected if these buttons are clicked after clicking one of
  the **Get Time Now** buttons.


- *Cancel Buttons*:
    
    Both buttons removes the user-selected date and time chosen from the screen. 
    

- *Get Time/Date Now Buttons*:

    Both buttons grab the system's current date and time, overriding the user-selected ones if the user selected a time
    and date before clicking any of these buttons.
  

- *Spin boxes*:
    
    The **4** spin boxes allow the user to set the time started or completed.
  

- *Calculate Payment Button*:

    This button allows the user to calculate the amount to be paid based on a given rate of **$5.00 per hour**.
    It's disabled right after the calculation and requires the **reset button** to reactivate.
    Wrong information that may lead to a result of negative amount will generate an error.
    The reset button again is used to reset this.
  

- *Reset Button*:
    
    This button removes the information provided by the user from the screen and reactivates the payment button to be
    used again.
  
  
- *Save Button*:
    
    This button allows the user to save information provided to an Excel file called `payment_history.xlsx`.
    When the App is first opened, a click on the button opens a file dialog box where the user is given the choice
    to pick where  he wants to save the Excel file. The app then searches that location if the Excel file already exists.
    If so, it just edits it. Otherwise, it creates a new Excel file and starts inputting the information provided.
    After the button is clicked for the first time, the next clicks don't open the file dialog box, but rather saves 
    the information to the previously used Excel file for convenience.
  

- *Submit Button*:
    
    This button is located in the calendar window when the calendar is opened, and it saves the date chosen by the user.
  

## PS:
This is my first GUI APP especially with Tkinter, so some of my methods and overall design may be inefficient.
Bugs and minor glitches may also be encountered while using the App.

**Contact**: tpandivine48@gmail.com, CHR-onicles©