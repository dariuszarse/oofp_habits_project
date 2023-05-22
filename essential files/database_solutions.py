#this file contains the functions for the database setup and the habit streak checkup on app startup

import sqlite3
import datetime

def create_table():
    '''this function opens up a connection to a database called habits.db and creates a cursor to execute sql queries'''

    connection = sqlite3.connect('habits.db')
    cursor = connection.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS HABITS
(   HABIT_NAME CHAR(50),
    HABIT_FREQUENCY CHAR(1),
    HABIT_START_DATE DATE,
    HABIT_CHECK_OFF_LAST DATE,
    HABIT_CHECK_OFF_NEXT DATE,
    HABIT_CURRENT_STREAK INT(5),
    HABIT_LONGEST_STREAK INT(5))""")
    connection.commit()
    connection.close()

def dummy_data():
    '''this function fills the table habits in habits.db with dummy data if the table is empty'''

    connection = sqlite3.connect('habits.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM HABITS')
    results=cursor.fetchall()
    if len(results) == 0:
        cursor.execute('''INSERT INTO HABITS(HABIT_NAME, HABIT_FREQUENCY, HABIT_START_DATE, HABIT_CHECK_OFF_LAST, HABIT_CHECK_OFF_NEXT, HABIT_CURRENT_STREAK, HABIT_LONGEST_STREAK) 
    VALUES('Swimming','W','2023-05-12','2023-05-12', '2023-05-19', '1','1'), ('Exercise', 'D', '2023-04-20', '2023-05-15', '2023-05-16', '15', '15'), ('Hairdresser', 'M', '2023-01-03', '2023-05-06', '2023-06-06', '2', '2'), ('Dancing', 'W', '2023-04-25', '2023-05-08', '2023-05-15', '3', '3'), ('Coding', 'D', '2023-03-13', '2023-05-16', '2023-05-17', '54', '54')''')
    connection.commit()
    connection.close()

def habit_broken():
    '''this function checks for potential broken habit streaks in the habits table of the habits.db'''
    
    connection = sqlite3.connect('habits.db')
    cursor = connection.cursor()
    today = datetime.datetime.today().date()
    cursor.execute("UPDATE HABITS SET HABIT_CURRENT_STREAK = 0 WHERE HABIT_CHECK_OFF_NEXT < date(?) = TRUE", (today,))
    connection.commit()
    connection.close()
