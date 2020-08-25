# Aiogram imports
from aiogram import types

# Module imports
from ..database import Database


async def get_base(msg: types.Message):
    database = Database("Couples.sqlite")

    msg_text = ""
    for user in database.get_base():
        user = [str(x) for x in user]
        msg_text += ", ".join(user)
        msg_text += "\n"

    await msg.reply(str(msg_text))
