#Student ID: F223882
"""-----------------------------------------------------------------------------------------------------------------------------------------------------------"""
"""Module menu is a module containing functions for the initial librarian login, credential check and main menu page of the programme."""
"""This module also includes two automatic modules which take into account the current date during the running of the programme.------------------------------"""
"""-----------------------------------------------------------------------------------------------------------------------------------------------------------"""

#Importing pre-existing Python module TKinter to allow GUI construction.
from tkinter import *
from tkinter import messagebox

#Importing pre-existing Python module datetime to manipulate time and date values.
import datetime

#Importing pre-existing Python module sys to route to specific folder.
import sys
sys.path.append('IntroToProgCW')

#Importing non pre-existing Python module sys to allow functionalities of different modules to be accessible through the main menu.
import bookSearch
import bookCheckout
import bookReturn
import bookSelect
import database

#Allows the setting of current date as there are functionalities which take into account current date.
current_temp = "12/1/2022"
current = datetime.datetime.strptime(current_temp, "%d/%m/%Y")

#Automatic function to check the current date and return books with return deadlines on that date.
def checkLateReturns(main_menu, main_frame):
    
    #Most recent entries first in the list.
    logfile = database.readLogFile()
    logfile.reverse()

    #Find the total number of books in the system.
    number_of_books = len(database.readBookInfo())
    possible_books = []
    for x in range(0, number_of_books):
        possible_books.append(str(x))

    #Find the most recent entry for each book in the system.
    most_recent_entries = []
    for entry in logfile:
        if entry[0] in possible_books:
            most_recent_entries.append(entry)
            possible_books.remove(entry[0])
            
    #Find the current date.
    today_date = current.strftime("%d/%m/%Y")

    #Titles for the table showing today's returns.
    todays_returns = [["Book ID","Member ID"]]

    #Check most recent entry of each book for their return date and select if date matches current date.
    for entry in most_recent_entries:
        if entry[3] == today_date:
            todays_returns.append([entry[0],entry[1]])

    #Display books for today's return in a tabular format.
    if len(todays_returns) > 1:
        late_display = Frame(main_frame)
        late_display.grid(row = 3, column = 0)

        late_title = Label(late_display, text = "Today's Returns:")
        late_title.grid(row = 0, column = 0)

        display_frame = Frame(late_display)
        display_frame.grid(row = 1, column = 0)

        for x in range(0, len(todays_returns)):
            for y in range(0,2):
                item = Label(display_frame, text = str(todays_returns[x][y]),width = 10, height = 2, relief = "solid")
                item.grid(row = x, column = y)

#Automatic function to update the reserved books to checked out status once their reserve date arrives.
def updateLogFile():

    #Most recent entries first in the list.
    logfile = database.readLogFile()
    logfile.reverse()

    #Find the total number of books in the system.
    number_of_books = len(database.readBookInfo())
    possible_books = []
    for x in range(0,number_of_books):
        possible_books.append(str(x))

    #Find the most recent entry for each book in the system.
    most_recent_entries = []
    for entry in logfile:
        if entry[0] in possible_books:
            most_recent_entries.append(entry)
            possible_books.remove(entry[0])

    #Find the current date.
    today_date = current.strftime("%d/%m/%Y")

    #Find entries with reservation dates matching current date, enter new entry into log file
    #updating checkout date and return date as well as opening up reservation date.
    for entry in most_recent_entries:
        if entry[4] == today_date:
            two_weeks_date = current + datetime.timedelta(days = 14)
            return_date = two_weeks_date.strftime("%d/%m/%Y")
            reservation_date = "-"
            reservation_id = "-"
            #The value of entry[5] is the value of the reservation ID, which replaces the member ID of the entry
            #once the reservation has been updated according to the current date.
            entry = [entry[0], entry[5], today_date, return_date, reservation_date, reservation_id]
            entry_string = "\n"
            for x in range(0,5):
                entry_string = entry_string + entry[x] + ","
            entry_string = entry_string + entry[5]
            
            logfile = open("logfile.txt","a")
            logfile.write(entry_string)
            logfile.close()

#Function to display librarian login page, initialising page for the programme.
def main():

    #Running automatic function to update reservation dates. (See above)
    updateLogFile()

    #Initialising GUI window.
    main_menu = Tk()
    main_menu.title("Generalised Library Systems")
    main_menu.geometry("1600x1200")

    #Initialising page frame for login page.
    main_frame = Frame(main_menu)
    main_frame.grid(row = 0, column = 0)
    main_frame.place(relx = 0.5, rely = 0.5, anchor = CENTER)

    #Initialising widgets inside page frame
    login_label = Label(main_frame, text = "Login ID")
    login_label.grid(row = 0, column = 0, columnspan = 2, padx = 30, pady = 30)

    login_entry = Entry(main_frame)
    login_entry.grid(row = 1, column = 0, columnspan = 2, padx = 30, pady = 30)

    #Event to trigger the passing of information into pin checking function.
    #Window main_menu and main_frame must be passed through to the next function to allow the changing of pages within one window.
    submit_button = Button(main_frame, text = "Submit", command = lambda: checkCredentials(main_menu, login_entry, main_frame))
    submit_button.grid(row = 2, column = 0, columnspan = 2, padx = 30, pady = 30)

    #Closes window and terminates programme.
    quit_button = Button(main_frame, text = "Quit", command = lambda: main_menu.destroy())
    quit_button.grid(row = 4, column = 0, columnspan = 2, padx = 30, pady = 30)

    main_menu.mainloop()

#Function to check if the librarian's Login ID is valid.
def checkCredentials(main_menu, login_entry, previous_frame):
    try:
        if int(login_entry.get()) in range (1000,10000):
            #If ID is valid, move onto the user menu with all functionalities on display.
            userMenu(main_menu, previous_frame)
        else:
            #If ID is the correct date type but out of range, return error message.
            login_reminder = Label(previous_frame, text = "Please enter a value between 1000 and 9999.")
            login_reminder.grid(row = 3, column = 0, columnspan = 2)
    except:
        #If ID is not the correct data type, return error message.
        login_reminder = Label(previous_frame, text = "Please enter a value between 1000 and 9999.")
        login_reminder.grid(row = 3, column = 0, columnspan = 2)

#Function to initialise the user menu of the programme, containing all functionalities.
def userMenu(main_menu, previous_frame):

    #Frame previous_frame is passed down from librarian login menu, where it will be destroyed here to make space for the new page.
    previous_frame.destroy()

    #New page frame initialised.
    main_frame = Frame(main_menu)
    main_frame.place(relx = 0.5, rely = 0.5, anchor = CENTER)

    #Running automatic function to display returns deadlining today. (See above)
    checkLateReturns(main_menu, main_frame)

    #Segmenting frames initialised to carry widgets.
    display_frame = Frame(main_frame)
    display_frame.grid(row = 1, column = 0)
    action_frame = Frame(main_frame)
    action_frame.grid(row = 2, column = 0)

    title_label = Label(display_frame, text = "Menu")
    title_label.grid(row = 0, column = 0, padx = 10, pady = 10)

    #Buttons, when pressed, updates the window to the page containing the user's desired functionality.
    #Same technique to change between pages is used as the transition between the login page and the user menu.
    search_button = Button(action_frame, text = "Search Book", command = lambda: bookSearch.searchBook(main_menu, main_frame))
    search_button.grid(row = 0, column = 0, padx = 10, pady = 10)
    checkout_button = Button(action_frame, text = "Checkout Book", command = lambda: bookCheckout.checkoutBook(main_menu, main_frame))
    checkout_button.grid(row = 0, column = 1, padx = 10, pady = 10)
    return_button = Button(action_frame, text = "Return Book", command = lambda: bookReturn.returnBook(main_menu, main_frame))
    return_button.grid(row = 0, column = 2, padx = 10, pady = 10)
    select_button = Button(action_frame, text = "Select Book", command = lambda: bookSelect.selectBook(main_menu, main_frame))
    select_button.grid(row = 0, column = 3, padx = 10, pady = 10)

    quit_button = Button(action_frame, text = "Quit", command = lambda: main_menu.destroy())
    quit_button.grid(row = 1, column = 0, columnspan = 4, padx = 30, pady = 30)

#Make sure this isn't run every time Python module menu is called.
if __name__ == "__main__":
    main()
