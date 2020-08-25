# Import logger
from .logger import log

# Import config file
from .config import *

# Import modules
from . import database
from . import handlers


def setup(dp):
    handlers.setup(dp)


async def on_shutdown(_):
    db = database.Database(database_file
    db.save_database()
