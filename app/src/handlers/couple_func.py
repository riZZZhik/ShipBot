"""Make couple function."""
from random import sample

import humanize
from aiogram import types

from ..config import config
from ..database import Database
from ..texts import NEW_COUPLE_STRING, OLD_COUPLE_STRING

# Initialize time humanizer language
humanize.i18n.activate("ru_RU")


async def make_couple(msg: types.Message) -> None:
    """Make new couple.

    If time delta is less than couples_delta, replies with old couple.
    Else, makes new couple and replies with it.

    Args:
        msg: aiogram Message.
    """
    database = Database(config.database_file)
    group_name = config.groups[msg.chat.id]

    td = database.update_time(group_name)
    # Check time delta
    if not td:
        usernames = database.get_usernames(group_name)
        couple = sample(usernames, 2)
        database.update_couple(group_name, couple)

        await msg.reply(NEW_COUPLE_STRING.format(couple[0], couple[1]))
    else:
        couple = database.last_couple(group_name)
        td_string = humanize.naturaltime(td)
        await msg.reply(OLD_COUPLE_STRING.format(couple[0], couple[1], td_string))
