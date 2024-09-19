#Student ID: F223882
"""---------------------------------------------------------------------------------------------"""
"""Module bookCheckout is a module containing functions for initialisation of the checkout menu,"""
"""the validation of inputted data, and determination of checkout and reservation availability.-"""
"""---------------------------------------------------------------------------------------------"""

from tkinter import *
from tkinter import messagebox

import datetime

import sys
sys.path.append('IntroToProgCW')

import database

current_temp = "12/1/2022"
current = datetime.datetime.strptime(current_temp, "%d/%m/%Y")

#Function to initialise the checkout menu of the programme for user to input the required information.
def checkoutBook(main_menu, previous_frame):
    previous_frame.destroy()

    main_frame = Frame(main_menu)
    main_frame.place(relx = 0.5, rely = 0.5, anchor = CENTER)

    display_frame = Frame(main_frame)
    display_frame.grid(row = 0, column = 0)
    action_frame = Frame(main_frame)
    action_frame.grid(row = 2, column = 0)

    instructions = Label(display_frame, text = "Enter information about the book and customer to checkout")
    instructions.grid(row = 0, column = 0, padx = 30, pady = 30)

    #Only book ID and member ID of the customer is required to checkout a book.
    book_id_label = Label(action_frame, text = "Book ID:")
    book_id_label.grid(row = 0, column = 0, padx = 30, pady = 30)
    member_id_label = Label(action_frame, text = "Member ID:")
    member_id_label.grid(row = 1, column = 0, padx = 30, pady = 30)
    book_id_entry = Entry(action_frame)
    book_id_entry.grid(row = 0, column = 1, padx = 30, pady = 30)
    member_id_entry = Entry(action_frame)
    member_id_entry.grid(row = 1, column = 1, padx = 30, pady = 30)

    #Button to trigger the credential check of both the book ID and the member ID,
    #and then the actual checkout itself if requirements are met.
    submit_button = Button(action_frame, text = "Submit", \
                           command = lambda: checkoutValidation(main_menu, main_frame, book_id_entry.get(),member_id_entry.get()))
    submit_button.grid(row = 2, column = 0, columnspan = 2, padx = 30, pady = 30)
    
    import menu
    back_button = Button(action_frame, text = "Back", command = lambda: menu.userMenu(main_menu, main_frame))
    back_button.grid(row = 3, column = 0, padx = 30, pady = 30)
    quit_button = Button(action_frame, text = "Quit", command = lambda: main_menu.destroy())
    quit_button.grid(row = 3, column = 1, padx = 30, pady = 30)

#Function to check whether inputs from the librarian is valid or not.
def checkoutValidation(main_menu, previous_frame, book_id, member_id):

    #Assume both checks are not met to start with, only change them to 'True' if met.
    member_id_accept = False
    book_id_accept = False

    try:
        #Member ID must be four digits.
        if int(member_id) in range(1000,10000):
            member_id_accept = True

        #Book ID must be correspondant with a book in the system.
        bookinfolist = database.readBookInfo()
        if int(book_id) in range(0, len(bookinfolist)):
            book_id_accept = True
    except:
        member_id_accept = False
        book_id_accept = False

    #If both checks are met, passes information onto function to determine whether the book is available for checkout.
    if (book_id_accept == True) and (member_id_accept == True):
        checkoutDecider(main_menu, previous_frame, book_id, member_id)
    else:
        #If not met, return error message.
        reminder = Label(previous_frame, text = "Please enter the right book ID and member ID.")
        reminder.grid(row = 1, column = 0, padx = 30, pady = 30)

#Function to decide whether a book is available for checkout, or reservation, or not at all.
def checkoutDecider(main_menu, previous_frame, book_id, member_id):
    
    #To find the last entry in log file for the book to be checked out.
    logfile = database.readLogFile()
    relevant_entries = []
    for entry in logfile:
        if entry[0] == book_id:
            relevant_entries.append(entry)   
    focus_entry = relevant_entries[-1]

    #If book is not checked out and not reserved, then it is available to checkout.
    if (focus_entry[2] == "-") and (focus_entry[3] == "-") and (focus_entry[4] == "-"):
        #Set checkout date as current date, return date as two weeks from current date, and reservation date is still empty.
        checkout_date = current.strftime("%d/%m/%Y")
        two_weeks_date = current + datetime.timedelta(days = 14)
        return_date = two_weeks_date.strftime("%d/%m/%Y")
        reservation_date = "-"

        #Pass information onto imported function from module database to be written onto logfile.txt.
        database.logFileDisplay(main_menu, previous_frame, focus_entry[0], member_id, checkout_date, return_date, reservation_date, "-")

    #If book is not checked out but is reserved:
    elif (focus_entry[2] == "-") and (focus_entry[3] == "-") and (focus_entry[4] != "-"):
        #Assume the book is available for checkout to find the return date for this checkout.
        checkout_date = current.strftime("%d/%m/%Y")
        two_weeks_date = current + datetime.timedelta(days = 14)
        return_date = two_weeks_date.strftime("%d/%m/%Y")
        reservation_date = focus_entry[4]

        #Covert date data into manipulable form.
        return_date_temp = datetime.datetime.strptime(return_date, "%d/%m/%Y")
        reservation_date_temp = datetime.datetime.strptime(reservation_date, "%d/%m/%Y")

        #Check that return date is at least 2 days before the reservation date.
        checkout_gap = reservation_date_temp - return_date_temp
        #If check is met, book is available for checkout.
        if checkout_gap > (datetime.timedelta(days = 2)):
            database.logFileDisplay(main_menu, previous_frame, focus_entry[0], member_id, checkout_date, return_date, reservation_date, "-")
        #If check is not met, return error.
        else:
            messagebox.showinfo("Checkout Rejected", "Return Date would be too close to the pre-reserved checkout date.")

    #If book is checked out but not reserved:
    elif (focus_entry[2] != "-") and (focus_entry[3] != "-") and (focus_entry[4] == "-"):
        #Ask for user input on whether they wish to reserve the book.
        result = messagebox.askquestion("Reservation Option?", \
                                        "Requested book is currently unavailable, would they like to make a reservation for it?")

        #If reservation is chosen:
        if result == 'yes':
            #Set reservation date for book as two days after the return date of the present checkout.
            return_date = focus_entry[3]
            return_date_temp = datetime.datetime.strptime(return_date, "%d/%m/%Y")
            reservation_date_temp = return_date_temp + datetime.timedelta(days = 2)
            reservation_date = reservation_date_temp.strftime("%d/%m/%Y")

            database.logFileDisplay(main_menu, previous_frame, focus_entry[0], focus_entry[1], focus_entry[2], return_date, reservation_date, member_id)

    #If book is both checked out and reserved, it is not available as a book can only be reserved once.
    elif (focus_entry[2] != "-") and (focus_entry[3] != "-") and (focus_entry[4] != "-"):
        #Return error.
        messagebox.showinfo("Checkout Rejected", "This book has already been reserved.")

    #If any other scenarios arise, the last entry for that book is incorrect and
    #the book would be frozen until a member of staff can confirm its status.
    else:
        messagebox.showinfo("Error Encountered", "There appears to be a problem with records for this book, please await assistance.", icon = "warning")




        
