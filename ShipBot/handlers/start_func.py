# Aiogram imports
from aiogram import types

# Module imports
from ..config import database_file
from ..database import Database
from ..texts import NEW_USER, OLD_USER


async def start(msg: types.Message):
    database = Database(database_file)
    if database.check_new_user(msg.from_user.id, msg.from_user.username, msg.from_user.full_name):
        await msg.answer(NEW_USER)
    else:
        await msg.answer(OLD_USER)