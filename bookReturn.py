#Student ID: F223882
"""---------------------------------------------------------------------------------------------"""
"""Module bookReturn is a module containing functions for initialisation of the return menu, the"""
"""validation of data inputted, and determination of whether inputted book can be returned.-----"""
"""---------------------------------------------------------------------------------------------"""

from tkinter import *
from tkinter import messagebox

import datetime

import sys
sys.path.append('IntroToProgCW')

import database

current_temp = "12/1/2022"
current = datetime.datetime.strptime(current_temp, "%d/%m/%Y")

#Function to initialise return menu for users to input required data.
def returnBook(main_menu, previous_frame):
    previous_frame.destroy()

    main_frame = Frame(main_menu)
    main_frame.place(relx = 0.5, rely = 0.5, anchor = CENTER)

    display_frame = Frame(main_frame)
    display_frame.grid(row = 1, column = 0)
    action_frame = Frame(main_frame)
    action_frame.grid(row = 2, column = 0)

    #Only book ID is required to return the book.
    instructions = Label(display_frame, text = "Enter Book ID to return.")
    instructions.grid(row = 0, column = 0, padx = 30, pady = 30)

    book_id_label = Label(action_frame, text = "Book ID:")
    book_id_label.grid(row = 0, column = 0, padx = 30, pady = 30)
    book_id_entry = Entry(action_frame)
    book_id_entry.grid(row = 0, column = 1, padx = 30, pady = 30)

    #Button to trigger the credential check of the book ID, and then the actual return itself if requirements are met.
    submit_button = Button(action_frame, text = "Submit", \
                           command = lambda: returnValidation(main_menu, main_frame, display_frame, book_id_entry.get()))
    submit_button.grid(row = 2, column = 0, columnspan = 2, padx = 30, pady = 30)

    import menu
    back_button = Button(action_frame, text = "Back", command = lambda: menu.userMenu(main_menu, main_frame))
    back_button.grid(row = 3, column = 0, padx = 30, pady = 30)
    quit_button = Button(action_frame, text = "Quit", command = lambda: main_menu.destroy())
    quit_button.grid(row = 3, column = 1, padx = 30, pady = 30)

#Function to check that book ID is valid.
def returnValidation(main_menu, previous_frame, display_frame, book_id):
    try:
        #To check if the inputted book ID is within the set of book IDs of all books in the system.
        bookinfolist = database.readBookInfo()
        if int(book_id) in range(0, len(bookinfolist)):
            #If so, information is passed onto the function to determine if the book can be returned.
            returnDecider(main_menu, previous_frame, book_id)
        else:
            #If not, return error.
            reminder = Label(display_frame, text = "Please enter the right book ID.")
            reminder.grid(row = 1, column = 0, padx = 30, pady = 30)
    except:
        #If it is in the wrong data type, return error.
        reminder = Label(display_frame, text = "Please enter the right book ID.")
        reminder.grid(row = 1, column = 0, padx = 30, pady = 30)

#Function to determine whether the book inputted can be returned.
def returnDecider(main_menu, previous_frame, book_id):

    #Find the last entry of the inputted book in the log file.
    logfile = database.readLogFile()
    relevant_entries = []
    for entry in logfile:
        if entry[0] == book_id:
            relevant_entries.append(entry)
    focus_entry = relevant_entries[-1]

    #If the book is not checked out and not reserved, then it cannot be returned.
    if (focus_entry[2] == "-") and (focus_entry[3] == "-") and (focus_entry[4] == "-"):
        messagebox.showinfo("Return Rejected", "Book is already returned.")

    #If the book is not checked out but is reserved, it cannot be returned as the book is still in the library.
    elif (focus_entry[2] == "-") and (focus_entry[3] == "-") and (focus_entry[4] != "-"):
        messagebox.showinfo("Return Rejected", "Book is already returned. Set to be checked out by Member ID: %s."%(focus_entry[5]))

    #If the book is checked out and is not reserved, then it can be returned. 
    elif (focus_entry[2] != "-") and (focus_entry[3] != "-") and (focus_entry[4] == "-"):
        #Required information is passed on to the external function from module database
        #to be written into a new latest entry for the inputted book.
        database.logFileDisplay(main_menu, previous_frame, focus_entry[0], focus_entry[1], "-", "-", "-", "-")

    #If the book is checked out and reserved, then it can be returned.
    elif (focus_entry[2] != "-") and (focus_entry[3] != "-") and (focus_entry[4] != "-"):
        #The book would be returned, but it would retain the reservation date and reservation ID, which would be updated by the automatic function in module menu.
        database.logFileDisplay(main_menu, previous_frame, focus_entry[0], focus_entry[1], "-", "-", focus_entry[4], focus_entry[5])
    else:
        messagebox.showinfo("Error Encountered", "There appears to be a problem with records for this book, please await assistance.", icon = "warning")





        
