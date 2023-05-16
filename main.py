#requirements

#return a list of all currently tracked habits
#return a list of all habits with the same periodicity
#return the longest run streak of all defined habits
#and return the longest run streak for a given habit


from datetime import datetime
from dateutil.relativedelta import relativedelta
import sqlite3
import re
import os

#creating the database with sqlite3

#opening a connection
connection = sqlite3.connect("habits.db")

#test print for connection check
#print("Opened database successfully")

#creating cursor
cursor = connection.cursor()

#creating the table if it doesn't exist already
cursor.execute("""CREATE TABLE IF NOT EXISTS HABITS
(   HABIT_NAME CHAR(50),
    HABIT_FREQUENCY CHAR(1),
    HABIT_START_DATE DATETIME,
    HABIT_CHECK_OFF_LAST DATE,
    HABIT_CHECK_OFF_NEXT DATE,
    HABIT_CURRENT_STREAK INT(5),
    HABIT_LONGEST_STREAK INT(5))""")


#check if table empty
cursor.execute('SELECT * FROM HABITS')
results=cursor.fetchall()
print(len(results))

#if table empty, fill with mock habits
if len(results) == 0:
    cursor.execute('''INSERT INTO HABITS(HABIT_NAME, HABIT_FREQUENCY, HABIT_START_DATE, HABIT_CHECK_OFF_LAST, HABIT_CHECK_OFF_NEXT, HABIT_CURRENT_STREAK, HABIT_LONGEST_STREAK) 
    VALUES('Swimming','W','2023-05-12','2023-05-12', '2023-05-19', '1','1'), ('Exercise', 'D', '2023-04-20', '2023-05-15', '2023-05-16', '15', '15'), ('Hairdresser', 'M', '2023-01-03', '2023-05-06', '2023-06-06', '2', '2'), ('Dancing', 'W', '2023-04-25', '2023-05-08', '2023-05-15', '3', '3'), ('Coding', 'D', '2023-03-13', '2023-05-16', '2023-05-17', '54', '54')''')

#commit change to database
connection.commit()

#close database connection
connection.close()


#introducing the class habit. For each object the user can enter a name and a frequency (which gets input checked to make sure only valid input is fed to our database). 
#Start_date is taken from datetime and check_off_next is calculated with relativedelta, while check_off_last, current_streak and longest_streak are implemented with their default values.

class Habit:
    def __init__(self, habit_name, habit_frequency, habit_start_date, habit_check_off_last='', habit_check_off_next='', habit_current_streak=0, habit_longest_streak=0):
        self.habit_name = habit_name
        self.habit_frequency = self.is_valid_frequency()
        self.habit_start_date = habit_start_date
        self.habit_check_off_last = ''
        self.habit_check_off_next = self.calculate_check_off_next()
        self.habit_current_streak = 0
        self.habit_longest_streak = 0

#defining validity check on frequency user input    
    def is_valid_frequency(self):
        while True:
            habit_frequency = input("How often do you want to check off your habit? Please enter D for daily, W for weekly or M for monthly: ")
            regex = "[wWdDmM]"
            if not re.match(regex, habit_frequency):
              print("You didn't enter a valid frequency for your habit")
            else:
              break
        return habit_frequency.upper()
    
#defining the function that calculates check_off_next
    def calculate_check_off_next(self):
        if self.habit_frequency == 'D':
                check_off_next = datetime.today()+relativedelta(days=+1)
                check_off_next = check_off_next.date().strftime('%Y-%m-%d')
                return check_off_next
        elif self.habit_frequency == 'W':
                check_off_next = datetime.today()+relativedelta(weeks=+1)
                check_off_next = check_off_next.date().strftime('%Y-%m-%d')
                return check_off_next
        else:
                check_off_next = datetime.today()+relativedelta(months=+1)
                check_off_next = check_off_next.date().strftime('%Y-%m-%d')
                return check_off_next
            
#defining function for creation of habit according to user input
    @classmethod
    def init_from_input(cls):
        return cls(
            str(input("How would you like to call your habit?\n")),
            '',
            datetime.today().strftime('%Y-%m-%d'),
        )

#checking for potential broken streaks on every app startup

#opening a connection
connection = sqlite3.connect("habits.db")

#creating cursor
cursor = connection.cursor()

#saving todays date as variable for comparison purposes
today = datetime.today().date()

#updating any current streaks to 0 where the check_off_next attribute was yesterday or earlier
cursor.execute("UPDATE HABITS SET HABIT_CURRENT_STREAK = 0 WHERE HABIT_CHECK_OFF_NEXT < date(?) = TRUE", (today,))

#commit change to database
connection.commit()

#close database connection
connection.close()


#clearing the terminal
os.system("cls")


#welcoming message
print('Welcome to this habit tracking app. I wish you all the best in chasing your goals!')

#main menu setup
main_menu_message = '''\nYou're in the main menu. What would you like to do?
You have the following options:
    [1] Display a selection of habits and/or streaks
    [2] Check off a habit for today
    [3] Create a new habit
    [4] Edit or delete an existing habit
    [5] Quit the app
Please enter the number belonging to the option of your choice here: '''

#defining navigation function
def main_menu():
    while True:
        user_choice = input(main_menu_message)
        regex = "[1-5]"
        if not re.match(regex, user_choice):
            print("\nThat is not a valid option. Try again!")
        elif user_choice == '1':
            display_habits()
            break
        elif user_choice == '2':
            check_off_habit()
            break
        elif user_choice == '3':
            create_new_habit()
            break
        elif user_choice == '4':
            edit_habit()
            break
        elif user_choice == '5':
            quit_app()
            break

      
#defining circle back function
def circle_back():
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
                    main_menu()
                elif user_choice == '2':
                    decision_made = True
                    quit_app()


#defining display habit function
def display_habits():

    #setup for user input request
    display_order_message = '''\nWhat would you like to be displayed?
    [1] All tracked habits (ordered by name)
    [2] Your daily habits
    [3] Your weekly habits
    [4] Your monthly habits
    [5] Your longest active streak
    [6] Your longest ever streak
    [7] Your most urgent habit to check off'''

    #establishing connection to database
    connection = sqlite3.connect("habits.db")
    cursor = connection.cursor()

    #asking user for input about order of display
    while True:
        user_choice = input(display_order_message+'\n')
        regex = "[1-7]"
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
            cursor.execute("SELECT HABIT_NAME, HABIT_LONGEST_STREAK FROM HABITS ORDER BY HABIT_LONGEST_STREAK DESC LIMIT 1")
            print('\nHere is your longest ever streak:')
            break
        elif user_choice == '7':
            cursor.execute("SELECT HABIT_NAME, HABIT_CHECK_OFF_NEXT FROM HABITS ORDER BY HABIT_CHECK_OFF_NEXT ASC LIMIT 1")
            print('\nHere is your most urgent habit with its due date:')
            break

    #printing data for user
    print(cursor.fetchall())
    print('')
    
    #closing connection to database
    connection.close()

    #returning to main menu
    circle_back()


#defining check off habit function
def check_off_habit():

    #establishing connection to database
    connection = sqlite3.connect("habits.db")
    cursor = connection.cursor()

    #retrieve all habits ordered by name
    cursor.execute("SELECT HABIT_NAME FROM HABITS ORDER BY HABIT_NAME")

    #display habits
    current_habits_message = cursor.fetchall()
    print('\nHere are all your currently tracked habits:\n'+str(current_habits_message)+'\n')

    #ask for user input on which habit to check off
    user_choice = input('Which habit would you like to check off? Please enter the exact name of the habit here:\n')

    #validating user input
    match = False
    while match == False:
        cursor.execute("SELECT HABIT_NAME FROM HABITS WHERE HABIT_NAME=?", (user_choice,))
        if user_choice not in str(cursor.fetchall()):
            user_choice = input('\nUnfortunately we could not recognize your input. Please try again.\nWhich habit would you like to check off? Please enter the exact name of the habit here:\n')
        else:
            match = True
            cursor.execute("SELECT * FROM HABITS WHERE HABIT_NAME=?", (user_choice,))
            chosen_habit = cursor.fetchone()
            print('You have selected to check off your habit '+str(chosen_habit)+'\nYour habit is being updated!\n')

            #with the correct habit selected the check_off_last attribute and the check_off_next attribute need to be updated.
            #we start with the check_off_last attribute
            check_off_last = datetime.today().strftime('%Y-%m-%d')
            cursor.execute('UPDATE HABITS SET HABIT_CHECK_OFF_LAST =? WHERE HABIT_NAME =?', (check_off_last, user_choice,))
            
            #for check_off_next we need to retrieve the frequency and depending on the frequency use dateutil.relativedelta with day/week/month 
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
            cursor.execute('UPDATE HABITS SET HABIT_CHECK_OFF_NEXT =? WHERE HABIT_NAME =?', (check_off_next, user_choice,))
            
            #with both dates updated it is time to update the streaks. starting with the current streak.
            cursor.execute('UPDATE HABITS SET HABIT_CURRENT_STREAK = HABIT_CURRENT_STREAK + 1 WHERE HABIT_NAME =?', (user_choice,))

            #and the longest streak
            cursor.execute('UPDATE HABITS SET HABIT_LONGEST_STREAK = HABIT_CURRENT_STREAK WHERE HABIT_CURRENT_STREAK > HABIT_LONGEST_STREAK')
            
            #writing the change into the database
            connection.commit()

            #closing connection to database
            connection.close()

            #returning to main menu
            circle_back()


#defining create habit function
def create_new_habit():
    new_habit = Habit.init_from_input()
    
    #inserting habit data to database
    #opening connectiong
    connection = sqlite3.connect('habits.db')

    #creating cursor
    cursor = connection.cursor()

    #writing to database
    cursor.execute('''INSERT INTO HABITS (HABIT_NAME, HABIT_FREQUENCY, HABIT_START_DATE, HABIT_CHECK_OFF_LAST, HABIT_CHECK_OFF_NEXT, HABIT_CURRENT_STREAK, HABIT_LONGEST_STREAK) 
    VALUES (?,?,?,?,?,?,?)''', (new_habit.habit_name, new_habit.habit_frequency, new_habit.habit_start_date, new_habit.habit_check_off_last, new_habit.habit_check_off_next, new_habit.habit_current_streak, new_habit.habit_longest_streak,))
    connection.commit()

    #closing connection
    connection.close()

    #navigating back to main menu
    circle_back()

#defining edit/delete habit function
def edit_habit():

    #using same habit selection code as in check_off habits

    #establishing connection to database
    connection = sqlite3.connect("habits.db")
    cursor = connection.cursor()

    #retrieve all habits ordered by name
    cursor.execute("SELECT HABIT_NAME FROM HABITS ORDER BY HABIT_NAME")

    #display habits
    current_habits_message = cursor.fetchall()
    print('\nHere are all your currently tracked habits:\n'+str(current_habits_message)+'\n')

    #ask for user input on which habit to check off
    user_choice = input('Which habit would you like to edit? Please enter the exact name of the habit here:\n')

    #validating user input
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

            #user choice between delete or edit (name or frequency)
            
            #defining message
            edit_delete_message = '''\nYou have the following options:
[1] Edit the name of the habit
[2] Edit the frequency of checking off the habit
[3] Delete the habit
Please enter what you would like to do here: '''

    #letting user choose what to edit/delete with re.match validation
    while True:
        user_choice = input(edit_delete_message)
        regex = "[1-3]"
        if not re.match(regex, user_choice):
            print("\nThat is not a valid option. Try again!")

        elif user_choice == '1':
            #change habit name
            #ask for the new habit name and store as variable. as any name is viable, no input validation
            new_name = str(input('What would you like to rename your habit too? '))

            #sql update command
            cursor.execute('UPDATE HABITS SET HABIT_NAME=? WHERE HABIT_NAME=?', (new_name, chosen_habit))

            #write change to database
            connection.commit()

            #close db connection
            connection.close()
            break

        elif user_choice == '2':
            #edit frequency
            #ask for wanted frequency on the habit, validate input (dDwWmM) and store as variable. using same function as in class definition
            while True:
                new_frequency = input("How often do you want to check off your habit? Please enter D for daily, W for weekly or M for monthly: ")
                regex = "[wWdDmM]"
                if not re.match(regex, new_frequency):
                    print("You didn't enter a valid frequency for your habit")
                else:
                    #update value via sql command
                    cursor.execute('UPDATE HABITS SET HABIT_FREQUENCY=? WHERE HABIT_NAME=?', (new_frequency, chosen_habit))

                    #write change to database
                    connection.commit()

                    #close db connection
                    connection.close()
                    break

        elif user_choice == '3':
            #delete habit
            #delete habit via sql command
            cursor.execute('DELETE FROM HABITS WHERE HABIT_NAME=?', (chosen_habit,))

            #write change to database
            connection.commit()

            #close db connection
            connection.close()
            break
    
    #call circle back function for navigation purposes
    circle_back()


#defining exit program procedure function
def quit_app():
    print('\nHave a great day! Good luck chasing your goals! :)\n')

main_menu()