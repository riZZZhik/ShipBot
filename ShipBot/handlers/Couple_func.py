# Other imports
from random import sample

# Aiogram imports
from aiogram import types

# Import time humanizer
import humanize
humanize.i18n.activate("ru")

# Module imports
from ..config import groups_dict
from ..database import Database
from ..texts import NEW_COUPLE_STRING, OLD_COUPLE_STRING


# TODO: Timer
# TODO: Reply before timer
async def make_couple(msg: types.Message):
    # Get couple
    database = Database("Couples.sqlite")
    group_name = groups_dict[msg.chat.id]

    td = database.update_time(group_name)
    if not td:
        usernames = database.get_usernames(group_name)
        couple = sample(usernames, 2)

        await msg.reply(NEW_COUPLE_STRING.format(couple[0], couple[1]))
    else:
        td_string = humanize.naturaltime(td)
        await msg.reply(OLD_COUPLE_STRING.format("T1", "T2", td_string))
