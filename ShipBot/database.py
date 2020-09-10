# Import logging
from ShipBot import log

# import database library
import sqlite3

# Import datetime module
from datetime import datetime, timedelta

# Module imports
from .config import couples_delta


# TODO: multigroup
class Database:
    """
    Class to interact with sqlite3 database
    """

    def __init__(self, file='database.db'):
        self.connect = sqlite3.connect(file)
        self.cursor = self.connect.cursor()

    # Return list of table values
    def get_base(self, group_name):
        self.cursor.execute(f"SELECT * FROM {group_name}")
        return self.cursor.fetchall()

    # Return list of usernames
    def get_usernames(self, group_name):
        self.cursor.execute(f"SELECT username FROM {group_name}")
        result = self.cursor.fetchall()
        return ["".join(x) for x in result]

    # Check and add new user if needed
    def check_new_user(self, group_name, user_id, username, name):  # TODO: Update usernames
        self.cursor.execute(f"SELECT * FROM {group_name} WHERE user_id={user_id}")
        if not self.cursor.fetchone():
            self.cursor.execute(f"INSERT INTO {group_name} VALUES ({user_id}, {username}, {name}, 0")
            log.info(f"Added {username} to table")
            self.save_database()

            return True
        else:
            return False

    # Check new couple time delta
    def update_time(self, group_name):
        # Get current time
        cur_time = datetime.now().timestamp()

        # Get last couple time
        self.cursor.execute(f"SELECT {group_name} from TIME")
        last_couple_time = self.cursor.fetchone()[0]

        # Get time difference between now and last couple
        td = cur_time - last_couple_time

        if td > couples_delta:
            self.cursor.execute(f"UPDATE TIME SET {group_name} = {cur_time} WHERE TRUE")
            self.connect.commit()

            return False
        else:
            return timedelta(seconds=td - couples_delta)

    # Save and close database
    def save_database(self):
        self.connect.commit()
        self.connect.close()
        log.info("Database saved")
