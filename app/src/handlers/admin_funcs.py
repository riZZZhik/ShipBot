"""Admin functions."""
from aiogram import types

from ..config import config
from ..database import Database


async def info(msg: types.Message) -> None:
    """Reply with message info.

    Args:
        msg: aiogram Message.
    """
    await msg.reply(msg)


async def get_base(msg: types.Message) -> None:
    """Reply with database info.

    Args:
        msg: aiogram Message.
    """
    database = Database("Couples.sqlite")
    group_name = config.groups_dict[msg.chat.id]

    msg_text = "Список купидона:\n"
    for user in database.get_base(group_name):
        user = [str(x) for x in user]
        msg_text += ", ".join(user)
        msg_text += "\n"

    await msg.reply(msg_text)
