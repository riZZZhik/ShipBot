# Aiogram imports
from aiogram import types

# Module imports
from ..config import groups_dict
from ..database import Database


async def info(msg: types.Message):
    await msg.reply(msg)


# Reply with a list of users
async def get_base(msg: types.Message):
    database = Database("Couples.sqlite")
    group_name = groups_dict[msg.chat.id]

    msg_text = "Список купидона:\n"
    for user in database.get_base(group_name):
        user = [str(x) for x in user]
        msg_text += ", ".join(user)
        msg_text += "\n"

    await msg.reply(str(msg_text))
