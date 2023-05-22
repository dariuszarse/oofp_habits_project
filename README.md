# oop_course_habit_tracker

Project scope:

This project was the creation of a habit tracker back end in Python 3.7 or later. The habit class was to be implemented with the object-oriented paradigm in mind.
Requirements included the possibility of creating custom habits with (at least) the daily and weekly frequency, the inclusion of dummy data for 5 predefined habits
(at least 1 daily and 1 weekly), a way to store data in between sessions (here I used sqlite3), the functionality of analyzing habits, a way for the user to interact
with the app, and lastly a unit test suite.

Install and run the program:

In order to run the habit tracker app you will need a program capable of executing .py files. For simplicity I'd recommend downloading the newest version of the python IDE
from python.org, although I personally use visual studio code. 
Download the essential files folder including all files and locate them on your computer. Then simply execute main.py and the program will start.

How to navigate through the app:

In the Habits_Submission_Development file I cover in detail how to navigate through the app. Although it is designed to be intuitive, if any questions arise have a look there.

Test:

To run the unit tests execute the tests.py file. It is still required to have all essential files in the same folder. Check the docstrings of each test to see what it does
and for which situation it is designed. The insert_dummy_data test for example only tests if the dummy data is successfully inserted into the database table and will fail
if you have already created an additional habit or deleted an existing one.
