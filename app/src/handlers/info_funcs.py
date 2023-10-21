"""Database info functions."""
from aiogram import types

from ..config import database_file, groups_dict
from ..database import Database
from ..texts import allstat, allstat_user, mystat, no_allstat


async def get_user_info(msg: types.Message) -> None:
    """Reply with user info.

    Args:
        msg: aiogram Message.
    """
    database = Database(database_file)
    group_name = groups_dict[msg.chat.id]

    data = database.get_info(group_name, msg.from_user.id)
    await msg.reply(mystat.format(*data))


async def get_group_info(msg: types.Message) -> None:
    """Reply with group info.

    Args:
        msg: aiogram Message.
    """
    database = Database(database_file)
    group_name = groups_dict[msg.chat.id]

    data = database.get_info(group_name)
    if data:
        message = allstat
        for name, count in data:
            message += allstat_user.format(name, count)
        await msg.reply(message)
    else:
        await msg.reply(no_allstat)
