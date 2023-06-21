# oop_course_habit_tracker

Project scope:

The focus of this project was the creation of a habit tracker back end in Python (3.7 or later). The habit class was to be implemented with the object-oriented paradigm in mind.
Requirements included the possibility of creating custom habits with (at least) the daily and weekly frequency, the inclusion of dummy data for 5 predefined habits
(at least 1 daily and 1 weekly), a way to store data in between sessions (here I used sqlite3), the functionality of analyzing habits, a way for the user to interact
with the app, and lastly a unit test suite.

Install and run the program:

In order to run the habit tracker app you will need a program capable of executing .py files. I personally use Visual Studio Code; however, I'd recommend downloading the newest version of the Python IDE from python.org for anyone that does not have their own IDE set up. After installing the Python IDE (or your preferred application of choice capable of running .py files), download all the .py files (database_solutions, habit, habit_management, main) and store them in the same folder on your computer. The last step is simply execute main.py which will start the program.

How to navigate through the app:

Essentially the program runs through a loop until you decide to quit. 
The main menu is the starting point of the loop and will always be returned to. From there you will be guided through the program.
Although it is designed to be intuitive, if any questions do arise please refer to the Habits_Submission_Development file where I cover in detail how to navigate through the app and which options are available.

Test:

In order to run the test unit, download test.py and save it in the same folder as the other .py files. You should run main.py first, without changing any habits as the tests rely on 
the dummy data created when starting up main.py for the first time. If you have changed habits already, delete the newly created habits.db file and run main.py. Just start
it up and select option 5 to quit the app right away. Then execute test.py. Check the docstrings of the tests to see what they do
and what the success criteria are.
