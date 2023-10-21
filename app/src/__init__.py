"""Package with all handlers and setup function for dispatcher."""
from .config import config


def setup(dp) -> None:
    """Set up handlers."""
    from . import handlers

    handlers.setup(dp)


async def on_shutdown(_) -> None:
    """Graceful shutdown with saving database."""
    from .database import Database

    db = Database(config.database_file)
    db.save_database()
    db.cursor.close()


__all__ = ["config", "setup", "on_shutdown"]
