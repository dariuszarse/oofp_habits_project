import unittest
import sqlite3

class Test(unittest.TestCase):
    def test_insert_dummy_data(self):
        '''this test succeeds if and only if the table HABITS in the database habits.db is successfully filled with 5 habits (the dummy data)'''
        connection = sqlite3.connect('habits.db')
        self.assertIsNot(connection, 0)
        cursor = connection.cursor()
        cursor.execute('Select HABIT_NAME from HABITS')
        results = cursor.fetchall()
        self.assertEqual(len(results), 5)
        cursor.close()
    
    def test_streak_broken(self):
        '''dummy data includes habits which are still marked with active streaks but an attribute check_off_last that is older than today.
        this test succeeds if the current streak is successfully set to 0'''


if __name__ == '__main__':
    unittest.main()