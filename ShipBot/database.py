# Import logging
from .logger import log

# import database library
import sqlite3

# Import datetime module
from datetime import datetime, timedelta

# Module imports
from .config import couples_delta


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

    # Return data for couple statistics
    def get_info(self, group_name, user_id=0):
        if user_id:
            self.cursor.execute(f"SELECT count FROM {group_name} WHERE user_id={user_id}")
            return self.cursor.fetchone()
        else:
            self.cursor.execute(f"SELECT username, count FROM {group_name} WHERE count != 0 ORDER BY count DESC")
            return self.cursor.fetchall()

    # Return list of usernames
    def get_usernames(self, group_name):
        self.cursor.execute(f"SELECT username FROM {group_name}")
        result = self.cursor.fetchall()
        return ["".join(x) for x in result]

    # Add new user to database
    def add_user(self, group_name, user_id, username, name):  # TODO: Update usernames
        self.cursor.execute(f"SELECT * FROM {group_name} WHERE user_id={user_id}")
        if not self.cursor.fetchone():
            self.cursor.execute(f"SELECT * FROM black_list WHERE user_id={user_id}")
            if not self.cursor.fetchone():
                self.cursor.execute(f"INSERT INTO {group_name} VALUES ({user_id}, \"{username}\", \"{name}\", 0)")
                self.cursor.execute("SELECT * FROM expresses ORDER BY username")
                log.info(f"Added @{username} to {group_name} table")
                self.save_database()

                return True
        return False

    # Remove user from database
    def delete_user(self, group_name, user_id, username):
        self.cursor.execute(f"DELETE FROM {group_name} WHERE user_id={user_id}")
        log.info(f"removed @{username} from {group_name} table")
        self.cursor.execute(f"INSERT INTO black_list VALUES ({user_id})")
        self.save_database()

    # Check new couple time delta
    def update_time(self, group_name):
        # Get current time
        cur_time = datetime.now().timestamp()

        # Get last couple time
        self.cursor.execute(f"SELECT {group_name} from TIME")
        last_couple_time = self.cursor.fetchone()[0]

        # Get time difference between now and last couple
        td = cur_time - last_couple_time

        # Update delta or return old one
        if td > couples_delta:
            self.cursor.execute(f"UPDATE TIME SET {group_name} = {cur_time} WHERE TRUE")
            self.save_database()

            return False
        else:
            return timedelta(seconds=td - couples_delta)

    # Update couple
    def update_couple(self, group_name, couple):
        self.cursor.execute("UPDATE expresses SET count = count + 1 "
                            f"WHERE username IN (\"{couple[0]}\", \"{couple[1]}\")")

        couple = ",".join(couple)
        self.cursor.execute(f"UPDATE COUPLES SET {group_name} = \"{couple}\"")
        self.save_database()

    # Get last couple
    def last_couple(self, group_name):
        self.cursor.execute(f"SELECT {group_name} from COUPLES")
        couple = self.cursor.fetchone()[0]
        couple = [x for x in couple.split(",")]
        return couple

    # Save and close database
    def save_database(self):
        self.cursor.execute("SELECT * FROM expresses ORDER BY username")
        self.connect.commit()
        log.info("Database saved")

    # Delete duplicate users
    def delete_duplicate(self):
        self.cursor.execute("DELETE FROM expresses WHERE rowid NOT IN "
                            f"(SELECT min(rowid) FROM expresses GROUP BY user_id);")
