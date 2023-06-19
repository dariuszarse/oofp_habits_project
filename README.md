# oop_course_habit_tracker

Project scope:

This project was the creation of a habit tracker back end in Python 3.7 or later. The habit class was to be implemented with the object-oriented paradigm in mind.
Requirements included the possibility of creating custom habits with (at least) the daily and weekly frequency, the inclusion of dummy data for 5 predefined habits
(at least 1 daily and 1 weekly), a way to store data in between sessions (here I used sqlite3), the functionality of analyzing habits, a way for the user to interact
with the app, and lastly a unit test suite.

Install and run the program:

In order to run the habit tracker app you will need a program capable of executing .py files. For simplicity I'd recommend downloading the newest version of the python IDE
from python.org, although I personally use visual studio code. 
Download all the .py files (database_solutions, habit, habit_management, main) and store them in the same folder on your computer. Then simply execute main.py and the program will start.

How to navigate through the app:

Essentially the program runs through a loop until you decide to quit. 
The main menu is the starting point of the loop and will always be returned to. From there you will be guided through the program.
Although it is designed to be intuitive, if any questions arise have a look at the Habits_Submission_Development file. 
There I cover in detail how to navigate through the app and which options are available.

Test:

To run the unit download test.py and safe it in the same folder as the other .py files. You should run main.py first, without changing any habits as the tests rely on 
the dummy data created when starting up main.py for the first time. If you have changed habits already, delete the newly created habits.db file and run main.py. Just start
it up and select option 5 to quit the app right away. Then execute test.py. Check the docstrings of the tests to see what they do
and what the success criteria are.
