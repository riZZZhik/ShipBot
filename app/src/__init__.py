"""Package with all handlers and setup function for dispatcher."""


def setup(dp) -> None:
    """Set up handlers."""
    from . import handlers

    handlers.setup(dp)


async def on_shutdown(_) -> None:
    """Graceful shutdown with saving database."""
    from .config import database_file
    from .database import Database

    db = Database(database_file)
    db.save_database()
    db.cursor.close()
