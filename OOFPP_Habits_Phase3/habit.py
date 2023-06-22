#introducing the class habit. For each object the user can enter a name and a frequency (which gets input checked to make sure only valid input is fed to our database). 
#Start_date is taken from datetime and check_off_next is calculated with relativedelta, while check_off_last, current_streak and longest_streak are implemented with their default values.

from datetime import datetime
from dateutil.relativedelta import relativedelta
import re

class Habit_class:
    '''introducing the class Habit_class. For each object the user can enter a name and a frequency (which gets input checked to make sure only valid input is fed to our database). 
    Start_date is taken from datetime and check_off_next is calculated with relativedelta, while check_off_last, current_streak and longest_streak are implemented with their default values.'''
    def __init__(self, habit_name, habit_frequency, habit_start_date, habit_check_off_last='', habit_check_off_next='', habit_current_streak=0, habit_longest_streak=0):
        self.habit_name = habit_name
        self.habit_frequency = self.is_valid_frequency()
        self.habit_start_date = habit_start_date
        self.habit_check_off_last = ''
        self.habit_check_off_next = self.calculate_check_off_next()
        self.habit_current_streak = 0
        self.habit_longest_streak = 0
   
    def is_valid_frequency(self):
        '''this function tests the user input for frequency on validity and once a valid frequency is entered returns it'''
        while True:
            habit_frequency = input("\nHow often do you want to check off your habit? Please enter D for daily, W for weekly or M for monthly: ")
            regex = "[wWdDmM]"
            if not re.match(regex, habit_frequency):
              print("You didn't enter a valid frequency for your habit")
            else:
              break
        return habit_frequency.upper()
    
    def calculate_check_off_next(self):
        '''this function calculates the check_off_next attribute from taking the date today as startdate and adding the frequency via relativedata.
        afterwards it returns the check_off_next attribute'''
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
            
    @classmethod
    def init_from_input(cls):
        '''this function allows for user input on creating a new habit. it returns the class object with a name, empty frequency and a start date'''
        return cls(
            str(input("\nHow would you like to call your habit?\n")),
            '',
            datetime.today().strftime('%Y-%m-%d'),
        )
