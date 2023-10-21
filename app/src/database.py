"""Database module."""
import sqlite3
from datetime import datetime, timedelta
from typing import Any, Literal

from .config import couples_delta
from .logger import log


class Database:
    """Class to interact with sqlite3 database."""

    def __init__(self, file: str = "database.db") -> None:
        """Initialize database.

        Args:
            file: Path to database file.
        """
        self.connect = sqlite3.connect(file)
        self.cursor = self.connect.cursor()

    def get_base(self, group_name: str) -> list[Any]:
        """Return whole database.

        Args:
            group_name: Name of group.

        Returns:
            List of tuples with database info.
        """
        self.cursor.execute(f"SELECT * FROM {group_name}")
        return self.cursor.fetchall()

    def get_info(self, group_name: str, user_id: int = 0) -> Any | list[Any]:
        """Return user info from database.

        Args:
            group_name: Name of group.
            user_id: User id.

        Returns:
            Tuple with user info or list of tuples with database info.
        """
        if user_id:
            self.cursor.execute(f"SELECT count FROM {group_name} WHERE user_id={user_id}")
            return self.cursor.fetchone()
        else:
            self.cursor.execute(
                f"SELECT username, count FROM {group_name} WHERE count != 0 ORDER BY count DESC"
            )
            return self.cursor.fetchall()

    def get_usernames(self, group_name: str) -> list[str]:
        """Return list of usernames from database.

        Args:
            group_name: Name of group.

        Returns:
            List of usernames registered in given group.
        """
        self.cursor.execute(f"SELECT username FROM {group_name}")
        result = self.cursor.fetchall()
        return ["".join(x) for x in result]

    def add_user(
        self, group_name: str, user_id: int, username: str, name: str
    ) -> bool:  # TODO: Update usernames
        """Add user to database.

        Args:
            group_name: Name of group.
            user_id: User id.
            username: User username.
            name: User name.

        Returns:
            True if user added, False if user already in database.
        """
        self.cursor.execute(f"SELECT * FROM {group_name} WHERE user_id={user_id}")
        if not self.cursor.fetchone():
            self.cursor.execute(f"SELECT * FROM black_list WHERE user_id={user_id}")
            if not self.cursor.fetchone():
                self.cursor.execute(
                    f'INSERT INTO {group_name} VALUES ({user_id}, "{username}", "{name}", 0)'
                )
                self.cursor.execute("SELECT * FROM expresses ORDER BY username")
                log.info(f"Added @{username} to {group_name} table")
                self.save_database()

                return True
        return False

    def delete_user(self, group_name: str, user_id: int, username: str) -> None:
        """Delete user from database.

        Args:
            group_name: Name of group.
            user_id: User id.
            username: User username.
        """
        self.cursor.execute(f"DELETE FROM {group_name} WHERE user_id={user_id}")
        log.info(f"removed @{username} from {group_name} table")
        self.cursor.execute(f"INSERT INTO black_list VALUES ({user_id})")
        self.save_database()

    def update_time(self, group_name: str) -> timedelta | Literal[False]:
        """Update time in database.

        Args:
            group_name: Name of group.

        Returns:
            Time delta if time difference is more than couples_delta, False otherwise.
        """
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

        return timedelta(seconds=td - couples_delta)

    def update_couple(self, group_name: str, couple: list[str]) -> None:
        """Update couple in database.

        Args:
            group_name: Name of group.
            couple: List of usernames.
        """
        self.cursor.execute(
            "UPDATE expresses SET count = count + 1 "
            f'WHERE username IN ("{couple[0]}", "{couple[1]}")'
        )

        self.cursor.execute(f'UPDATE COUPLES SET {group_name} = "{",".join(couple)}"')
        self.save_database()

    def last_couple(self, group_name: str) -> list[Any]:
        """Get last couple from database.

        Args:
            group_name: Name of group.
        """
        self.cursor.execute(f"SELECT {group_name} from COUPLES")
        couple = self.cursor.fetchone()[0]
        couple = list(couple.split(","))
        return couple

    def save_database(self) -> None:
        """Save database and close connection."""
        self.cursor.execute("SELECT * FROM expresses ORDER BY username")
        self.connect.commit()
        log.info("Database saved")

    def delete_duplicate(self) -> None:
        """Delete duplicate users from database."""
        self.cursor.execute(
            "DELETE FROM expresses WHERE rowid NOT IN "
            "(SELECT min(rowid) FROM expresses GROUP BY user_id);"
        )
