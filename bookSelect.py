#Student ID: F223882
"""--------------------------------------------------------------------------------------------------"""
"""Module bookCheckout is a module containing functions for initialisation of the select budget menu,"""
"""calculation of the statistics from log file, and the display of the data in graphical format.-----"""
"""--------------------------------------------------------------------------------------------------"""

from tkinter import *
from tkinter import messagebox

import datetime

#Importing pre-existing Python module matplotlib to allow graphical display of data.
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

import sys
sys.path.append('IntroToProgCW')

import database

#Function to initialise the select menu of the programme for users to input the required information for calculations.
def selectBook(main_menu, previous_frame):
    previous_frame.destroy()

    main_frame = Frame(main_menu)
    main_frame.place(relx = 0.5, rely = 0.5, anchor = CENTER)

    display_frame = Frame(main_frame)
    display_frame.grid(row = 1, column = 0)
    action_frame = Frame(main_frame)
    action_frame.grid(row = 2, column = 0)

    instructions = Label(display_frame, text = "Enter budget to get book and genre suggestion.")
    instructions.grid(row = 0, column = 0, padx = 30, pady = 30)

    #Only the budget allowance is required for calculations.
    budget_label = Label(action_frame, text = "Budget:")
    budget_label.grid(row = 0, column = 0, padx = 30, pady = 30)
    budget_entry = Entry(action_frame)
    budget_entry.grid(row = 0, column = 1, padx = 30, pady = 30)

    #Button to trigger the calculation function.
    submit_button = Button(action_frame, text = "Submit", \
                           command = lambda: selectValidation(main_menu, main_frame, display_frame, budget_entry.get()))
    submit_button.grid(row = 2, column = 0, columnspan = 2, padx = 30, pady = 30)

    import menu
    back_button = Button(action_frame, text = "Back", command = lambda: menu.userMenu(main_menu, main_frame))
    back_button.grid(row = 3, column = 0, padx = 30, pady = 30)
    quit_button = Button(action_frame, text = "Quit", command = lambda: main_menu.destroy())
    quit_button.grid(row = 3, column = 1, padx = 30, pady = 30)

#Function to check that book ID is valid.
def selectValidation(main_menu, main_frame, display_frame, budget):
    
    #To check if the inputted budget is in the right format.
    try:
        budget = int(budget)
        selectResults(main_menu, main_frame, budget)
    except:
        #If not, return error.
        reminder = Label(display_frame, text = "Please enter the right budget in integer form.")
        reminder.grid(row = 1, column = 0, padx = 30, pady = 30)

#Function to initialise the display page for all the conclusion to the calculations.
def selectResults(main_menu, previous_frame, budget):

    #Retrieve data from function to find out calculations for top books and top genres. (See below)
    book_tally, genre_tally = purchaseSuggestion()

    previous_frame.destroy()

    main_frame = Frame(main_menu)
    main_frame.place(relx = 0.5, rely = 0.5, anchor = CENTER)

    display_frame = Frame(main_frame)
    display_frame.grid(row = 0, column = 0)
    action_frame = Frame(main_frame)
    action_frame.grid(row = 1, column = 0)

    #Manipulate 2-dimensional list genre_tally into a form manipulable by the matplotlib module.
    genres = []
    for each in genre_tally:
        genres.append(each[0])
    numbers = []
    for each in genre_tally:
        numbers.append(each[1])

    #Make use of function createGraphs to create pie chart. (See below)
    #This is then embedded into a TKinter canvas and hence displayed on a window.
    fig = createGraphs(genres,numbers)
    canvas = FigureCanvasTkAgg(fig, display_frame)
    canvas.draw()
    canvas.get_tk_widget().grid(row=0, column=0, rowspan = 20)

    #Find the top 3 books.
    book_info_list = database.readBookInfo()
    top_book_names = []
    for book in book_info_list[1:]:
        for x in range(0,3):
            if book_tally[x][0] == book[0]:
                top_book_names.append(book[2])

    #Display the top 3 books in a clear fashion.
    book_first_label = Label(display_frame, text = "Top Book So Far: %s"%(top_book_names[0]))
    book_first_label.grid(row = 0, column = 1)
    book_second_label = Label(display_frame, text = "Runner Up Book So Far: %s"%(top_book_names[1]))
    book_second_label.grid(row = 1, column = 1)
    book_third_label = Label(display_frame, text = "2nd Runner Up Book So Far: %s"%(top_book_names[2]))
    book_third_label.grid(row = 2, column = 1)

    #Finding the total number of genres in logfile.txt.
    total_entry_number = 0
    for each in numbers:
        total_entry_number += each

    #Find out the portion of the budget that would be assigned to their corresponding module.
    budget_assignment = []
    for each in numbers[:]:
        genre_budget = ((each / total_entry_number) * budget)
        #If the budget assigned is less than 10 pounds, the genre would not be displayed
        #and their portion would just become surplus.
        if genre_budget < 10:
            genres.remove(genres[numbers.index(each)])
            numbers.remove(each)
        else:
            budget_assignment.append(int("%.0f"%(genre_budget)))

    #Combine the list of the genres and the list of assigned budgets together
    #to form a 2-dimensional list of genres alongside their budget.
    final_budget_assign_list = []
    for x in range(0,len(genres)):
        final_budget_assign_list.append([genres[x],budget_assignment[x]])

    #Display the assignation of the budget and their respective budget.
    title_label = Label(display_frame, text = "Genres: Budget Assigned")
    title_label.grid(row = 3, column = 1)
    for x in range(0,len(final_budget_assign_list)):
        genre = final_budget_assign_list[x][0]
        assigned_budget = final_budget_assign_list[x][1]
        genre_budget_label = Label(display_frame, text = "%s: £%s - %s books"%(genre, assigned_budget, str(int(assigned_budget) // 10)))
        genre_budget_label.grid(row = 4+x, column = 1)

    back_button = Button(action_frame, text = "Back", command = lambda: selectBook(main_menu, main_frame))
    back_button.grid(row = 0, column = 0, padx = 30, pady = 30)
    quit_button = Button(action_frame, text = "Quit", command = lambda: main_menu.destroy())
    quit_button.grid(row = 0, column = 1, padx = 30, pady = 30)

#Function to calculate the ranking of the books and genres by popularity.
def purchaseSuggestion():
    
    #Retrieve all entries of the log file, and tally up the number of entries for each book.
    logfile = database.readLogFile()
    book_info_list = database.readBookInfo()
    number_of_books = len(book_info_list)
    book_tally = []
    for x in range(0, number_of_books):
        book_tally.append([str(x),0])
    for entry in logfile:
        for book in book_tally:
            if entry[0] == book[0]:
                book[1] += 1
    sorted_book_tally = sorted(book_tally, key = lambda x: x[1], reverse = True)

    #Retrieve all entries of the log file, and tally up the number of entries for each genre.
    genre_books = {}
    genre_tally = {}
    for book in book_info_list[1:]:
        if book[1] in genre_books:
            genre_books[book[1]].append(book[0])
        else:
            genre_books[book[1]] = [book[0]]
            genre_tally[book[1]] = 0
    for book in sorted_book_tally:
        for genre in genre_books:
            if book[0] in genre_books[genre]:
                genre_tally[genre] += book[1]

    #Convert both sets of data into 2-dimensional lists to be passed into the display function. (See above)
    temp1_genre_tally = sorted(genre_tally.items(), key = lambda x: x[1], reverse = True)
    temp2_genre_tally = dict(temp1_genre_tally)
    sorted_genre_tally = [[k, v] for k, v in temp2_genre_tally.items()]

    return(sorted_book_tally, sorted_genre_tally)

#Function to initialise and construct the pie chart graph.
def createGraphs(genres, numbers):
    
    #Setting font sizes.
    plt.rc('font', size=7)

    #Initialising the plot.
    fig, ax1 = plt.subplots()

    #Defining the dimensions of the figure.
    fig.set_figwidth(7)
    fig.set_figheight(7)

    #Defining the type of graph for the figure.
    ax1.pie(numbers, labels=genres, autopct='%0.0f%%', textprops={'size': 'smaller'}, startangle=90)
    ax1.axis("equal")

    #Defining plot title.
    plt.title("Genre by Popularity")
    
    return fig 






