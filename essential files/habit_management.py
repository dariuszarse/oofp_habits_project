from datetime import datetime
from dateutil.relativedelta import relativedelta
import sqlite3
import re
import habit as habit


def display_habits():
    '''this function gives the user a selection of options in which habits to look at and how they should be structured. according to the selection
    it then selects the desired data from the database and prints it to the screen.'''

    display_order_message = '''\nWhat would you like to see displayed?
    [1] All tracked habits (ordered by name)
    [2] Your daily habits
    [3] Your weekly habits
    [4] Your monthly habits
    [5] Your longest active streak
    [6] Your habits' longest ever streaks
    [7] The longest streak of a selected habit
    [8] Your most urgent habit to check off'''

    #opening connection
    connection = sqlite3.connect("habits.db")
    cursor = connection.cursor()

    #asking for user input regarding what habits should be displayed how
    while True:
        user_choice = input(display_order_message+'\n')
        regex = "[1-8]"
        if not re.match(regex, user_choice):
            print("\nThat is not a valid option. Try again!\n")
        
        #retrieving data from database according to user input
        elif user_choice == '1':
            cursor.execute("SELECT * FROM HABITS ORDER BY HABIT_NAME")
            print('\nHere are all your currently tracked habits:')
            break
        elif user_choice == '2':
            cursor.execute("SELECT * FROM HABITS WHERE HABIT_FREQUENCY = 'D'")
            print('\nHere are all your daily habits:')
            break
        elif user_choice == '3':
            cursor.execute("SELECT * FROM HABITS WHERE HABIT_FREQUENCY = 'W'")
            print('\nHere are all your weekly habits:')
            break
        elif user_choice == '4':
            cursor.execute("SELECT * FROM HABITS WHERE HABIT_FREQUENCY = 'M'")
            print('\nHere are all your monthly habits:')
            break
        elif user_choice == '5':
            cursor.execute("SELECT HABIT_NAME, HABIT_CURRENT_STREAK FROM HABITS ORDER BY HABIT_CURRENT_STREAK DESC LIMIT 1")
            print('\nHere is your longest active streak:')
            break
        elif user_choice == '6':
            cursor.execute("SELECT HABIT_NAME, HABIT_LONGEST_STREAK FROM HABITS ORDER BY HABIT_LONGEST_STREAK DESC")
            print('\nHere are your longest streaks:')
            break
        elif user_choice == '7':
            cursor.execute("SELECT HABIT_NAME FROM HABITS ORDER BY HABIT_NAME")
            print('These are your currently tracket habits:\n')
            print(cursor.fetchall())
            user_choice = input('For which one would you like to see your longest streak? Please enter the exact name of the habit here:\n')
            match = False
            while match == False:
                cursor.execute("SELECT HABIT_NAME FROM HABITS WHERE HABIT_NAME=?", (user_choice,))
                if user_choice not in str(cursor.fetchall()):
                    user_choice = input('\nUnfortunately we could not recognize your input. Please try again.\nFor which habit would you like to see your longest streak? Please enter the exact name of the habit here:\n')
                else:
                    match = True
                    cursor.execute("SELECT HABIT_NAME, HABIT_LONGEST_STREAK FROM HABITS WHERE HABIT_NAME=?", (user_choice,))
                    print("\nHere is your habits' longest streak:")
                    break
            break
        elif user_choice == '8':
            cursor.execute("SELECT HABIT_NAME, HABIT_CHECK_OFF_NEXT FROM HABITS ORDER BY HABIT_CHECK_OFF_NEXT ASC LIMIT 1")
            print('\nHere is your most urgent habit with its due date:')
            break

    #printing data for user and closing connection
    print(cursor.fetchall())
    connection.close()

    print('Redirecting you...')


def check_off_habit():
    '''this function lets the user check off a habit that they select in the habits table. user input is validated so that the user is forced to select a valid habit.
    once the habit is selected the function will increase the current streak of that habit by 1. Lastly, if the current streak afterwards is higher than the longest streak
    the function will update the longest streak to match the value of the current streak.'''
    
    #opening connection
    connection = sqlite3.connect("habits.db")
    cursor = connection.cursor()

    #retrieving all habits ordered by name
    cursor.execute("SELECT HABIT_NAME FROM HABITS ORDER BY HABIT_NAME")
    current_habits_message = cursor.fetchall()
    print('\nHere are all your currently tracked habits:\n'+str(current_habits_message)+'\n')

    #letting user choose which habit should be checked off
    user_choice = input('Which habit would you like to check off? Please enter the exact name of the habit here:\n')
    match = False
    while match == False:
        cursor.execute("SELECT HABIT_NAME FROM HABITS WHERE HABIT_NAME=?", (user_choice,))
        if user_choice not in str(cursor.fetchall()):
            user_choice = input('\nUnfortunately we could not recognize your input. Please try again.\nWhich habit would you like to check off? Please enter the exact name of the habit here:\n')
        
        else:
            match = True
            cursor.execute("SELECT * FROM HABITS WHERE HABIT_NAME=?", (user_choice,))

            #updating check_off_last attribute
            check_off_last = datetime.today().strftime('%Y-%m-%d')
            cursor.execute('UPDATE HABITS SET HABIT_CHECK_OFF_LAST =? WHERE HABIT_NAME =?', (check_off_last, user_choice,))
            
            #retrieving habit_frequency for check_off_next update 
            cursor.execute('SELECT HABIT_FREQUENCY FROM HABITS WHERE HABIT_NAME=?', (user_choice,))
            habit_frequency = cursor.fetchone()

            if habit_frequency == ('D',):
                check_off_next = datetime.today()+relativedelta(days=+1)
                check_off_next = check_off_next.date().strftime('%Y-%m-%d')
            elif habit_frequency == ('W',):
                check_off_next = datetime.today()+relativedelta(weeks=+1)
                check_off_next = check_off_next.date().strftime('%Y-%m-%d')
            else:
                check_off_next = datetime.today()+relativedelta(months=+1)
                check_off_next = check_off_next.date().strftime('%Y-%m-%d')

            #updating check_off_next and the current (and if neccessary longest) streak
            cursor.execute('UPDATE HABITS SET HABIT_CHECK_OFF_NEXT =? WHERE HABIT_NAME =?', (check_off_next, user_choice,))
            cursor.execute('UPDATE HABITS SET HABIT_CURRENT_STREAK = HABIT_CURRENT_STREAK + 1 WHERE HABIT_NAME =?', (user_choice,))
            cursor.execute('UPDATE HABITS SET HABIT_LONGEST_STREAK = HABIT_CURRENT_STREAK WHERE HABIT_CURRENT_STREAK > HABIT_LONGEST_STREAK')
            connection.commit()
            connection.close()
            print('Your habit has been successfully checked off for today!')
    
    print('Redirecting you...')


def create_new_habit():
    '''this function creates a new object of the class Habit_class which is defined in habit.py. attributes habit_name and habit_frequency have to be input by the user
    while all other attributes will be set automatically'''

    #calling init function Habit_class
    new_habit = habit.Habit_class.init_from_input()
    
    connection = sqlite3.connect('habits.db')
    cursor = connection.cursor()

    #inserting new habit into database
    cursor.execute('''INSERT INTO HABITS (HABIT_NAME, HABIT_FREQUENCY, HABIT_START_DATE, HABIT_CHECK_OFF_LAST, HABIT_CHECK_OFF_NEXT, HABIT_CURRENT_STREAK, HABIT_LONGEST_STREAK) 
    VALUES (?,?,?,?,?,?,?)''', (new_habit.habit_name, new_habit.habit_frequency, new_habit.habit_start_date, new_habit.habit_check_off_last, new_habit.habit_check_off_next, new_habit.habit_current_streak, new_habit.habit_longest_streak,))
    
    connection.commit()
    connection.close()
    print('You have successfully created a new habit! Good luck!')
    print('Redirecting you...')


def edit_habit():
    '''this function first lets the user select a habit they'd like to either edit or delete. after successful validation of user input the habit information is retrieved from the database
    and the user is presented with the option to edit name, frequency or just delete the whole habit. the input is validated again and the respective action is taken and committed to the database'''

    #opening connection
    connection = sqlite3.connect("habits.db")
    cursor = connection.cursor()

    #retrieving habits from database
    cursor.execute("SELECT HABIT_NAME FROM HABITS ORDER BY HABIT_NAME")
    current_habits_message = cursor.fetchall()
    print('\nHere are all your currently tracked habits:\n'+str(current_habits_message)+'\n')

    #asking for user input on which habit to check off
    user_choice = input('Which habit would you like to edit? Please enter the exact name of the habit here:\n')

    match = False
    while match == False:
        cursor.execute("SELECT HABIT_NAME FROM HABITS WHERE HABIT_NAME=?", (user_choice,))
        if user_choice not in str(cursor.fetchall()):
            user_choice = input('\nUnfortunately we could not recognize your input. Please try again.\nWhich habit would you like to edit? Please enter the exact name of the habit here:\n')
        else:
            match = True
            cursor.execute("SELECT * FROM HABITS WHERE HABIT_NAME=?", (user_choice,))

            #storing user input for future use as new variable
            chosen_habit = user_choice
            print('You have selected to edit your habit '+str(chosen_habit))

            edit_delete_message = '''\nYou have the following options:
[1] Edit the name of the habit
[2] Edit the frequency of checking off the habit
[3] Delete the habit
Please enter what you would like to do here: '''

    #giving the user their choice regarding edit name/frequency or delete
    while True:
        user_choice = input(edit_delete_message)
        regex = "[1-3]"
        if not re.match(regex, user_choice):
            print("\nThat is not a valid option. Try again!")

        elif user_choice == '1':
            #asking for the new habit name and writing it to the database
            new_name = str(input('What would you like to rename your habit too? '))
            cursor.execute('UPDATE HABITS SET HABIT_NAME=? WHERE HABIT_NAME=?', (new_name, chosen_habit))
            connection.commit()
            connection.close()
            print('Your habit has been successfully renamed!')
            break

        elif user_choice == '2':
            #asking for wanted frequency, validating input (dDwWmM) and writing it to database
            while True:
                new_frequency = input("How often do you want to check off your habit? Please enter D for daily, W for weekly or M for monthly: ")
                regex = "[wWdDmM]"
                if not re.match(regex, new_frequency):
                    print("You didn't enter a valid frequency for your habit")
                else:
                    
                    cursor.execute('UPDATE HABITS SET HABIT_FREQUENCY=? WHERE HABIT_NAME=?', (new_frequency, chosen_habit))
                    connection.commit()
                    connection.close()
                    print('You have successfully updated your habit frequency!')
                    break
            break

        elif user_choice == '3':
            #deleting selected habit
            cursor.execute('DELETE FROM HABITS WHERE HABIT_NAME=?', (chosen_habit,))
            connection.commit()
            connection.close()
            print('The habit has been deleted!')
            break
    
    print('Redirecting you...')