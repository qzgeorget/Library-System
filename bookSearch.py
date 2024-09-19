#Student ID: F223882
"""-----------------------------------------------------------------------------------------"""
"""Module bookSearch is a module containing functions for initialisation of the search menu,"""
"""the query of books by their titles, and display frame of query results-------------------"""
"""-----------------------------------------------------------------------------------------"""

from tkinter import *
from tkinter import messagebox

import datetime

import sys
sys.path.append('IntroToProgCW')

#Importing non pre-existing Python module database to allow the reading of the comma separated files, BookInfo.txt and logfile.txt.
import database

current_temp = "12/1/2022"
current = datetime.datetime.strptime(current_temp, "%d/%m/%Y")

#Function to initialise the menu to search for books in the system, allowing the user to enter the necessary data for their search.
def searchBook(main_menu, previous_frame):

    #Remove the previous page's main frame to make way for this page's.
    previous_frame.destroy()

    #Main frame for search menu initialised
    main_frame = Frame(main_menu)
    main_frame.place(relx = 0.5, rely = 0.5, anchor = CENTER)

    instructions = Label(main_frame, text = "Enter information about the book:")
    instructions.grid(row = 0, column = 0, columnspan = 2, padx = 30, pady = 30)
    
    display_frame = Frame(main_frame)
    display_frame.grid(row = 1, column = 0)
    action_frame = Frame(main_frame)
    action_frame.grid(row = 2, column = 0)

    #Entry box for the user to input thier query keywords.
    query_entry = Entry(action_frame)
    query_entry.grid(row = 0, column = 0, columnspan = 2,  padx = 30, pady = 30)

    #Button to trigger the search function to look for the books in the system.
    search_button = Button(action_frame, text = "Submit Query", command = lambda: titleSearch(main_menu, main_frame, query_entry.get()))
    search_button.grid(row = 1, column = 0, columnspan = 2, padx = 30, pady = 30)

    #Importing non pre-existing Python module menu to allow the return to the main user menu.
    import menu
    #Button widget Back initialised to allow the user to return to the main user menu.
    back_button = Button(action_frame, text = "Back", command = lambda: menu.userMenu(main_menu, main_frame))
    back_button.grid(row = 2, column = 0, padx = 30, pady = 30)
    quit_button = Button(action_frame, text = "Quit", command = lambda: main_menu.destroy())
    quit_button.grid(row = 2, column = 1, padx = 30, pady = 30)

#Function to search for the books queried by the user and initialise page to display search results.
def titleSearch(main_menu, previous_frame, keywordstring):
    bookinfolist = database.readBookInfo()
    keywordstring = keywordstring.lower()

    returnquerylist = [bookinfolist[0]]
    returnquerylist[0].append("Availability")
    
    bookinfolist = bookinfolist[1:]
    #Iterate through all books in the system.
    for book in bookinfolist:
        #Return all books which book titles equal to or contains the keyword phrase.
        if (keywordstring in book[2].lower()) or (keywordstring == book[2].lower()):
            returnquerylist.append(book)

            #Iterating through logfile.txt to return the last entry for each book returned.
            logfile = database.readLogFile()
            book_entries = []
            for entry in logfile:
                if entry[0] == book[0]:
                    book_entries.append(entry)
            focus_entry = book_entries[-1]

            #Determine the availability status of the book based on the current date and the last entry.
            if (focus_entry[2] == "-") and (focus_entry[3] == "-") and (focus_entry[4] == "-"):
                book_availability = "Available"
            elif (focus_entry[2] == "-") and (focus_entry[3] == "-") and (focus_entry[4] != "-"):
                checkout_date = current.strftime("%d/%m/%Y")
                two_weeks_date = current + datetime.timedelta(days = 14)
                return_date = two_weeks_date.strftime("%d/%m/%Y")
                reservation_date = focus_entry[4]

                return_date_temp = datetime.datetime.strptime(return_date, "%d/%m/%Y")
                reservation_date_temp = datetime.datetime.strptime(reservation_date, "%d/%m/%Y")
                
                checkout_gap = reservation_date_temp - return_date_temp
                
                if checkout_gap > (datetime.timedelta(days = 2)):
                    book_availability = "Available"
                else:
                    book_availability = "Reserved"
            elif (focus_entry[2] != "-") and (focus_entry[3] != "-") and (focus_entry[4] == "-"):
                book_availability = "Reserve Available"
            elif (focus_entry[2] != "-") and (focus_entry[3] != "-") and (focus_entry[4] != "-"):
                book_availability = "Reserved"
            else:
                book_availability = "Unavailable"

            returnquerylist[-1].append(book_availability)

    for each in returnquerylist:
        count = 0
        for book in returnquerylist:
            if each == book:
                count += 1
        for x in range(1,count):
            returnquerylist.remove(each)

    #Display page initialised.
    previous_frame.destroy()

    main_frame = Frame(main_menu)
    main_frame.place(relx = 0.5, rely = 0.5, anchor = CENTER)
    
    display_frame = Frame(main_frame)
    display_frame.grid(row = 0, column = 0, pady = 10)
    action_frame = Frame(main_frame)
    action_frame.grid(row = 1, column = 0, pady = 10)

    for x in range(0, len(returnquerylist)):
        for y in range(0, 7):
            if y == 2:
                item = Label(display_frame, text = str(returnquerylist[x][y]), width = 50, height = 1, relief = "solid")
                item.grid(row = x, column = y)
            else:
                item = Label(display_frame, text = str(returnquerylist[x][y]), width = 15, height = 1, relief = "solid")
                item.grid(row = x, column = y)
                
    back_button = Button(action_frame, text = "Back", command = lambda: searchBook(main_menu, main_frame))
    back_button.grid(row = 0, column = 0, padx = 30, pady = 30)
    quit_button = Button(action_frame, text = "Quit", command = lambda: main_menu.destroy())
    quit_button.grid(row = 0, column = 1, padx = 30, pady = 30)
    
