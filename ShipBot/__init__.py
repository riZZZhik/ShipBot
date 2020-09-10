# Import logger
from .logger import log

# Import config file
from .config import *

# Import modules
from .database import Database
from . import handlers


def setup(dp):
    handlers.setup(dp)


async def on_shutdown(_):
    db = Database(groups_dict, database_file)
    db.save_database()
