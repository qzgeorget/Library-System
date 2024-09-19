This programme was coded on Python version 3.9.7, on MacOS Monterey. As I'm writing this code, I recognized that some features in the code may behave differently between Windows OS and MacOS, but testing with the computer lab devices have convinced me that it should go smoothly on Windows OS just like it does for me on MacOS. So hopefully, the robustness of this code I've written comes through. 
For the feature of the back button shifting between pages, I called the functionality modules in the menu module, as well as the menu module in the funcitonality modules. This decision has made a mess, particularly with circular dependency. I have found a way to go around it, namely only importing the menu module before the initialisation of the button inside its own function. It works now, but I'm pretty sure that it isn't the best coding practice in the world but I lack the time to understand it and improve at this moment in time.
Due to the nature of the programme, I found it difficult to write test modules for each of the functions as they all require the GUI and the user's interaction. I apologise in advance if my planning of the runthrough test of the code doesn't work as I had planned but below is a set of instructions to test the functionalities of the code to see if it meet the requirements. 

For the purpose of convenience, the current date for the test has been set to "12/1/2022".
If the current date of any of the modules are not the "12/1/2022", the tests may not work.

It may be wise to create a duplicate file for logifile.txt before any testing in case a manoeuvre has been attempted but not according to the plan in place. I do apologise, but if logfile_duplicate.txt had to be utilised, the test plan would have to be restarted. 

0.0 TO TEST LIBRARIAN LOGIN:
Initialise GUI by running initialiser.py.
0.1 enter string "abc" into login entry box (erroneous - wrong type)
0.2 enter integer 100 into login entry box (erroneous - out of range)
0.3 enter integer 98765 into the login entry box (erroneous - out of range)
0.4 enter integer 1000 into the login entry box (valid - lower bound)
0.5 enter integer 9999 into the login entry box (valid - upper bound)
0.6 enter integer 1234 into the login entry box (valid)

	Press submit to move on into the user menu.

1.0 TO TEST LATE RETURN REMINDER
1.1 user menu would show [Book ID: 4, Member ID: 9873] as today's return.

2.0 TO TEST BOOK SEARCH:
Press on "Search Book" button after librarian login.
2.1 enter 11011010 into title search entry (no results - wrong type)
2.2 enter "Angels and Demons" into title search entry (no results - book not in system)
2.3 enter empty string into title search entry (all books shown)
2.4 enter "a" into the title search entry (all books containing letter "a" shown)
2.5 enter "Percy Jackson" into the title search entry (5 books of the Percy Jackson series shown)
2.6 enter "percy jackson" into the title search entry (same as 2.5)
2.7 enter "It" into the title search entry (all books containing "it" shown, in both cases)

	Press "Back" button to return to user menu.

3.0 TO TEST BOOK CHECKOUT:
Press on the "Checkout Book" button after librarian login.
3.1 enter [Book ID: "abc", Member ID: "abcd"] into checkout entries (erroneous - both wrong type)
3.2 enter [Book ID: 32, Member ID: 1234] into checkout entries (erroneous - book ID out of range)
3.3 enter [Book ID: 12, Member ID: 12345] into checkout entries (erroneous - member ID out of range)
3.4 enter [Book ID: 3, Member ID: 1234] into checkout entries (valid - available)
3.5 enter [Book ID: 9, Member ID: 1234] into checkout entries (valid - unavailable currently, reservation available)
3.6 enter [Book ID: 17, Member ID: 1234] into checkout entries (valid - available currently, but unavailable for checkout as reservation is too near)
3.7 enter [Book ID: 2, Member ID: 1234] into checkout entries (valid - unavailable currently, and unavailable for reservation)

	Press "Back" button to return to user menu.

4.0 TO TEST BOOK RETURN:
Press on the "Return Book" button after librarian login.
4.1 enter "abc" into book ID entry (erroneous - wrong type)
4.2 enter 32 into book ID entry (erroneous - out of range)
4.3 enter 19 into book ID entry (valid - book returned)
4.4 enter 5 into book ID entry (erroneous - book is already back in the system)

	Press "Back" button to return to user menu.

5.0 TO TEST BOOK SELECT:
Press on the "Select Book" button after librarian login.
5.1 enter "abc" into budget entry (erroneous - wrong type)
5.2 enter 100 into budget entry (valid)
5.3 enter 1234 into budget entry (valid)

	Press "Quit" button to terminate the programme.

6.0 TO OBSERVE AUTOMATIC RESERVATION TO CHECKED OUT UPDATE
Open logfile.txt in folders or finder.
Check for entries for [Book ID: 11]
Second to last entry would've been a return command, and the last entry of the book would be a checkout entry with current date as checkout date.