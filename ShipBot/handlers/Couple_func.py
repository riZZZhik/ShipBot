# Other imports
from random import sample

# Aiogram imports
from aiogram import types

# Module imports
from ..database import Database
from ..texts import COUPLE_STRING


# TODO: Timer
# TODO: Reply before timer
async def make_couple(msg: types.Message):
    database = Database("Couples.sqlite")
    usernames = database.get_usernames()
    couple = sample(usernames, 2)
    await msg.reply(COUPLE_STRING.format(couple[0], couple[1]))
