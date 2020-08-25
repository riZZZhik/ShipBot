# Import logging
from ShipBot import log

# import database library
import sqlite3


# TODO: multigroup
class Database:
    """
    Class to interact with sqlite3 database
    """

    def __init__(self, file='database.db'):
        self.connect = sqlite3.connect(file)
        self.cursor = self.connect.cursor()

    # Return list of table values
    def get_base(self):
        self.cursor.execute("SELECT * FROM expresses")
        return self.cursor.fetchall()

    # Return list of usernames
    def get_usernames(self):
        self.cursor.execute("SELECT username FROM expresses")
        return ["".join(x) for x in self.cursor.fetchall()]  # FIXME: MAYBE

    # Check and add new user if needed
    def check_new_user(self, user_id, username, name):  # TODO: Update usernames
        self.cursor.execute("SELECT * FROM expresses WHERE user_id=?", (user_id,))
        if not self.cursor.fetchone():
            self.cursor.execute("INSERT INTO expresses VALUES (?, ?, ?, ?)", (user_id, username, name, 0))
            log.info(f"Added {username} to table")
            self.save_database()

            return True
        else:
            return False

    # Save and close database
    def save_database(self):
        self.connect.commit()
        self.connect.close()
        log.info("Database saved")
