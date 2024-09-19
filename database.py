#Student ID: F223882
"""---------------------------------------------------------------------------------------------"""
"""Module database is a module containing functions for reading of BookInfo.txt and logfile.txt,"""
"""the appending of entries to logfile.txt, and display frame of appending actions.-------------"""
"""---------------------------------------------------------------------------------------------"""

from tkinter import *
from tkinter import messagebox

import sys
sys.path.append('IntroToProgCW')

#Function to read the contents of comma separated file, BookInfo.txt into a list of lists.
def readBookInfo():
    bookinfo = open("Book_Info.txt", "r")
    temp1 = bookinfo.read()

    #Each entry is separated by the fact that they are in different rows.
    temp2 = temp1.split("\n")
    bookinfolist = []
    for line in temp2:
        #Each item in an entry is separated by a comma.
        book = line.split(",")
        for each in book:
            #Putting all string items into standard form for comparison in further calculation modules.
            try:
               each = each.lower()
            except:
                next
        bookinfolist.append(book)
    bookinfo.close()
    
    return bookinfolist

#Function to read the contents of comma separated file, logfile.txt into a list of lists.
def readLogFile():
    log = open("logfile.txt", "r")
    temp1 = log.read()

    #Each entry is separated by the fact that they are in different rows.
    temp2 = temp1.split("\n")
    logfile = []
    for line in temp2:
        #Each item in an entry is separated by a comma.
        entry = line.split(",")
        logfile.append(entry)
    log.close()
    
    return logfile

#Function to initialise the display frame of all the information for appending an entry to logfile.txt.
def logFileDisplay(main_menu, previous_frame, book_id, member_id, checkout_date, return_date, reservation_date, reservation_id):
    previous_frame.destroy()

    main_frame = Frame(main_menu)
    main_frame.place(relx = 0.5, rely = 0.5, anchor = CENTER)

    display_frame = Frame(main_frame)
    display_frame.grid(row = 0, column = 0)
    action_frame = Frame(main_frame)
    action_frame.grid(row = 1, column = 0)

    #Displaying all six pieces of vital information for each entry.
    book_id_title = Label(display_frame, text = "Book ID: ")
    book_id_title.grid(row = 0, column = 0, padx = 30, pady = 30)
    member_id_title = Label(display_frame, text = "Borrower ID: ")
    member_id_title.grid(row = 1, column = 0, padx = 30, pady = 30)
    checkout_date_title = Label(display_frame, text = "Checkout Date: ")
    checkout_date_title.grid(row = 2, column = 0, padx = 30, pady = 30)
    return_date_title = Label(display_frame, text = "Return Date: ")
    return_date_title.grid(row = 3, column = 0, padx = 30, pady = 30)
    reservation_date_title = Label(display_frame, text = "Reservation Date: ")
    reservation_date_title.grid(row = 4, column = 0, padx = 30, pady = 30)
    reservation_id_title = Label(display_frame, text = "Reservation Member ID: ")
    reservation_id_title.grid(row = 5, column = 0, padx = 30, pady = 30)

    book_id_data = Label(display_frame, text = book_id)
    book_id_data.grid(row = 0, column = 1, padx = 30, pady = 30)
    member_id_data = Label(display_frame, text = member_id)
    member_id_data.grid(row = 1, column = 1, padx = 30, pady = 30)
    checkout_date_data = Label(display_frame, text = checkout_date)
    checkout_date_data.grid(row = 2, column = 1, padx = 30, pady = 30)
    return_date_data = Label(display_frame, text = return_date)
    return_date_data.grid(row = 3, column = 1, padx = 30, pady = 30)
    reservation_date_data = Label(display_frame, text = reservation_date)
    reservation_date_data.grid(row = 4, column = 1, padx = 30, pady = 30)
    reservation_id_data = Label(display_frame, text = reservation_id)
    reservation_id_data.grid(row = 5, column = 1, padx = 30, pady = 30)

    #Button to trigger the function which appends the entry to the actual logfile.txt.
    submit_button = Button(action_frame, text = "Submit", \
                           command = lambda: logFileWriter(main_menu, book_id, member_id, checkout_date, return_date, reservation_date, reservation_id, main_frame))
    submit_button.grid(row = 0, column = 0, columnspan = 2, padx = 30, pady = 30)

    import menu
    back_button = Button(action_frame, text = "Back", command = lambda: menu.userMenu(main_menu, main_frame))
    back_button.grid(row = 1, column = 0, padx = 30, pady = 30)
    quit_button = Button(action_frame, text = "Quit", command = lambda: main_menu.destroy())
    quit_button.grid(row = 1, column = 1, padx = 30, pady = 30)

#Function to append information passed down from display function to logfile.txt. (See above)
def logFileWriter(main_menu, book_id, member_id, checkout_date, return_date, reservation_date, reservation_id, previous_frame):

    #Manipulate data from previous function into one long string variable.
    entry = [book_id, member_id, checkout_date, return_date, reservation_date, reservation_id]
    entry_string = "\n"
    for x in range(0,5):
        entry_string = entry_string + entry[x] + ","
    entry_string = entry_string + entry[5]

    #Append to logfile.txt.
    logfile = open("logfile.txt","a")
    logfile.write(entry_string)
    logfile.close()

    #Visual confirmation for use.
    messagebox.showinfo("Confirmation", "Log File has been updated!")

    #Returns to main user menu page after action is done.
    #If the window remains on the display page, the same action would be allowed
    #to be carried out again without previous checks, duplicating the entry and
    #thereby making the Book Select function inaccurate.
    import menu
    menu.userMenu(main_menu, previous_frame)







