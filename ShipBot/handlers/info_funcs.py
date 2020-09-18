# Aiogram imports
from aiogram import types

# Module imports
from ..config import database_file, groups_dict
from ..database import Database
from ..texts import mystat, allstat, allstat_user, no_allstat


# Reply user stats
async def get_user_info(msg: types.Message):
    database = Database(database_file)
    group_name = groups_dict[msg.chat.id]

    data = database.get_info(group_name, msg.from_user.id)
    await msg.reply(mystat.format(*data))


# Reply group stats
async def get_group_info(msg: types.Message):
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
