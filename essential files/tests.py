import unittest
import sqlite3
import datetime


class Test(unittest.TestCase):
    def test_insert_dummy_data(self):
        '''this test checks the number of rows in the table habits in the database habits.db.
        the test succeeds only when the table successfully filled with 5 habits (the dummy data).'''
        connection = sqlite3.connect('habits.db')
        cursor = connection.cursor()
        cursor.execute('Select HABIT_NAME from HABITS')
        results = cursor.fetchall()
        self.assertEqual(len(results), 5)
        cursor.close()
    
    def test_streak_broken(self):
        '''this test checks for all habits and their check_off_next attribute. 
        if the date stored in the attribute is older than today, it checks if the attribute habit_current_streak has been set to 0.
        the test succeeds if this is true for all instances.'''
        connection = sqlite3.connect('habits.db')
        cursor = connection.cursor()
        today = datetime.datetime.today().date()
        cursor.execute('Select HABIT_CURRENT_STREAK from HABITS where HABIT_CHECK_OFF_NEXT < date(?) = TRUE', (today,))
        results = cursor.fetchall()
        self.assertTrue(x=='0,' for x in results)
        cursor.close()

if __name__ == '__main__':
    unittest.main()