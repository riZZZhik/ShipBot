# Setup handlers
def setup(dp):
    from . import handlers

    handlers.setup(dp)


# Save Database on shutdown
async def on_shutdown(_):
    from .database import Database
    from .config import database_file

    db = Database(database_file)
    db.save_database()
    db.cursor.close()
