"""Database module."""
import sqlite3
from datetime import datetime, timedelta
from typing import Any, Literal

from .config import config
from .logger import log


class Database:
    """Class to interact with sqlite3 database."""

    def __init__(self, file: str = "database.db") -> None:
        """Initialize database.

        Args:
            file: Path to database file.
        """
        # check if file exists
        try:
            with open(file, "r"):
                pass
            self.connect = sqlite3.connect(file)
            self.cursor = self.connect.cursor()
        except FileNotFoundError:
            log.info("Database file not found, creating new one")
            self.connect = sqlite3.connect(file)
            self.cursor = self.connect.cursor()
            self.cursor.execute("CREATE TABLE times (chat_id string, time real)")
            self.cursor.execute("CREATE TABLE couples (chat_id string, couple string)")
            self.cursor.execute("CREATE TABLE black_list (user_id int)")

            self.save_database()

    def get_base(self, chat_id: int) -> list[Any]:
        """Return whole database.

        Args:
            chat_id: Chat id.

        Returns:
            List of tuples with database info.
        """
        self.cursor.execute(f"SELECT * FROM {chat_id}")
        return self.cursor.fetchall()

    def get_info(self, chat_id: int, user_id: int = 0) -> Any | list[Any]:
        """Return user info from database.

        Args:
            chat_id: Chat id.
            user_id: User id.

        Returns:
            Tuple with user info or list of tuples with database info.
        """
        if user_id:
            self.cursor.execute(f'SELECT count FROM "{chat_id}" WHERE user_id={user_id}')
            return self.cursor.fetchone()
        else:
            self.cursor.execute(
                f'SELECT username, count FROM "{chat_id}" WHERE count != 0 ORDER BY count DESC'
            )
            return self.cursor.fetchall()

    def get_usernames(self, chat_id: int) -> list[str]:
        """Return list of usernames from database.

        Args:
            chat_id: Chat id.

        Returns:
            List of usernames registered in given group.
        """
        self.cursor.execute(f'SELECT username FROM "{chat_id}"')
        result = self.cursor.fetchall()
        return ["".join(x) for x in result]

    def add_user(self, chat_id: int, user_id: int, username: str, name: str) -> bool:
        """Add user to database.

        Args:
            chat_id: Chat id.
            user_id: User id.
            username: User username.
            name: User name.

        Returns:
            True if user added, False if user already in database.
        """
        if not self._check_table_exist(chat_id):
            self.cursor.execute(
                f'CREATE TABLE "{chat_id}" (user_id int, username string, name string, count int)'
            )

        self.cursor.execute(f'SELECT * FROM "{chat_id}" WHERE user_id={user_id}')
        if not self.cursor.fetchone():
            self.cursor.execute(f"SELECT * FROM black_list WHERE user_id={user_id}")
            if not self.cursor.fetchone():
                self.cursor.execute(
                    f'INSERT INTO "{chat_id}" VALUES ({user_id}, "{username}", "{name}", 0)'
                )
                log.info(f'Added @{username} to "{chat_id}" table')
                self.save_database()

                return True

        return False

    def delete_user(self, chat_id: int, user_id: int, username: str) -> None:
        """Delete user from database.

        Args:
            chat_id: Chat id.
            user_id: User id.
            username: User username.
        """
        self.cursor.execute(f'DELETE FROM "{chat_id}" WHERE user_id={user_id}')
        log.info(f"removed @{username} from {chat_id} table")
        self.cursor.execute(f"INSERT INTO black_list VALUES ({user_id})")
        self.save_database()

    def update_time(self, chat_id: int) -> timedelta | Literal[False]:
        """Update time in database.

        Args:
            chat_id: Chat id.

        Returns:
            Time delta if time difference is more than couples_delta, False otherwise.
        """
        # Get current time
        cur_time = datetime.now().timestamp()

        # Get last couple time
        self.cursor.execute(f'SELECT time FROM times WHERE chat_id="{chat_id}"')
        last_couple_time = self.cursor.fetchone()

        # Check case when there is no last couple
        if not last_couple_time:
            self.cursor.execute(f'INSERT INTO times VALUES ("{chat_id}", {cur_time})')
            self.save_database()

            return False

        # Get time difference between now and last couple
        td = cur_time - last_couple_time[0]

        # Update delta or return old one
        if td > config.couples_delta:
            self.cursor.execute(f'UPDATE times SET time = {cur_time} WHERE chat_id="{chat_id}"')
            self.save_database()

            return False

        return timedelta(seconds=td - config.couples_delta)

    def update_couple(self, chat_id: int, couple: list[str]) -> None:
        """Update couple in database.

        Args:
            chat_id: Chat id.
            couple: List of usernames.
        """
        self.cursor.execute(
            f'UPDATE "{chat_id}" SET count = count + 1 '
            f'WHERE username IN ("{couple[0]}", "{couple[1]}")'
        )

        self.cursor.execute(f'SELECT couple FROM couples WHERE chat_id="{chat_id}"')
        if not self.cursor.fetchone():
            self.cursor.execute(f'INSERT INTO couples VALUES ("{chat_id}", "{",".join(couple)}")')
        else:
            self.cursor.execute(
                f'UPDATE couples SET couple = "{",".join(couple)}" WHERE chat_id="{chat_id}"'
            )

        self.save_database()

    def last_couple(self, chat_id: int) -> list[str] | Literal[False]:
        """Get last couple from database.

        Args:
            chat_id: Chat id.

        Returns:
            List of tuples with last couple info.
        """
        self.cursor.execute(f'SELECT couple FROM couples WHERE chat_id="{chat_id}"')
        couple = self.cursor.fetchone()
        if not couple:
            return False

        return list(couple[0].split(","))

    def save_database(self) -> None:
        """Save database and close connection."""
        self.connect.commit()
        log.info("Database saved")

    def _check_table_exist(self, table_name: str) -> bool:
        """Check if table exists in database.

        Args:
            table_name: Table name.

        Returns:
            True if table exists, False otherwise.
        """
        self.cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
            (table_name,),
        )
        return bool(self.cursor.fetchone())
