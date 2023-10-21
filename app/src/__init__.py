# Setup handlers
def setup(dp):
    from . import handlers

    handlers.setup(dp)


# Save Database on shutdown
async def on_shutdown(_):
    from .config import database_file
    from .database import Database

    db = Database(database_file)
    db.save_database()
    db.cursor.close()
