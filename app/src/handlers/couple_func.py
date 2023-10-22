"""Make couple function."""
from random import sample

import humanize
from aiogram import types

from ..config import config
from ..database import Database
from ..texts import new_couple_string, not_enough_users, old_couple_string

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

    # Check if time delta is less than couples_delta
    td = database.update_time(msg.chat.id)
    old_couple = database.last_couple(msg.chat.id)
    if td and old_couple:
        td_string = humanize.naturaltime(td)
        await msg.reply(old_couple_string.format(old_couple[0], old_couple[1], td_string))
        return

    # Check if there is enough users
    usernames = database.get_usernames(msg.chat.id)
    if len(usernames) < config.min_users:
        await msg.reply(not_enough_users.format(config.min_users))
        return

    # Make new couple
    couple = sample(usernames, 2)
    database.update_couple(msg.chat.id, couple)
    await msg.reply(new_couple_string.format(couple[0], couple[1]))
