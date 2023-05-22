#requirements

#return a list of all currently tracked habits
#return a list of all habits with the same periodicity
#return the longest run streak of all defined habits
#and return the longest run streak for a given habit

import re
import os
import habit as habit
import database_solutions as db
import habit_management as mngm

#database setup
db.create_table()
db.dummy_data()

#checking for potential broken streaks on every app startup
db.habit_broken()

#clearing the terminal
os.system("cls")

#welcoming message
print('Welcome to this habit tracking app. I wish you all the best chasing your goals!')

def menu():
    '''this function takes user input (1-5), validates a 'correct' choice and navigates to the chosen function in the 'main.py' file'''

    menu_message = '''\nYou're in the main menu. What would you like to do?
You have the following options:
    [1] Display a selection of habits and/or streaks
    [2] Check off a habit for today
    [3] Create a new habit
    [4] Edit or delete an existing habit
    [5] Quit the app
Please enter the number belonging to the option of your choice here: '''
    while True:
        user_choice = input(menu_message)
        regex = "[1-5]"
        if not re.match(regex, user_choice):
            print("\nThat is not a valid option. Try again!")
        elif user_choice == '1':
            mngm.display_habits()
        elif user_choice == '2':
            mngm.check_off_habit()
        elif user_choice == '3':
            mngm.create_new_habit()
        elif user_choice == '4':
            mngm.edit_habit()
        elif user_choice == '5':
            quit_app()
            break

#with a change in code structure this function is no longer required. it is only still here because it was mentioned in the concept and implementation phase. 
""" def circle_back():
    '''this function gives the user the choice to either return to the main menu for additional app usage or to quit the app'''

    decision_made = False
    while decision_made == False:
                regex = '[1-2]'
                user_choice = input('''Would you like to return to the main menu or quit the app?
[1] Main Menu
[2] Quit the App\n''')
                if not re.match(regex, user_choice):
                    print("\nThat is not a valid option. Try again!\n")
                elif user_choice == '1':
                    decision_made = True
                    menu()
                elif user_choice == '2':
                    decision_made = True
                    quit_app() """

def quit_app():
    '''this function quits the app after sending a good luck message'''

    print('\nHave a great day! Good luck chasing your goals! :)\n')


menu()