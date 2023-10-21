# Aiogram imports
# Other imports
from random import sample

# Import time humanizer
import humanize
from aiogram import types

# Module imports
from ..config import database_file, groups_dict
from ..database import Database
from ..texts import NEW_COUPLE_STRING, OLD_COUPLE_STRING

# Initialize time humanizer language
humanize.i18n.activate("ru_RU")


# Reply with random couple
async def make_couple(msg: types.Message):
    database = Database(database_file)
    group_name = groups_dict[msg.chat.id]

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
