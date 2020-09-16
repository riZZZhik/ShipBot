# Aiogram imports
from aiogram import types

# Module imports
from ..config import database_file, groups_dict
from ..database import Database
from ..texts import new_user, left_user, no_username


async def new_member(msg: types.Message):
    database = Database(database_file)
    group_name = groups_dict[msg.chat.id]

    if msg.new_chat_members[0].username:
        database.add_user(group_name, msg.new_chat_members[0].id,
                          msg.new_chat_members[0].username,
                          msg.new_chat_members[0].full_name)

        await msg.reply(new_user.format(msg.new_chat_members[0].full_name))
    else:
        await msg.reply(no_username.format(msg.new_chat_members[0].full_name))


async def member_left(msg: types.Message):
    database = Database(database_file)
    group_name = groups_dict[msg.chat.id]

    database.delete_user(group_name, msg.left_chat_member.id, msg.left_chat_member.username)

    await msg.reply(left_user)


async def new_member_from_msg(msg: types.Message):
    database = Database(database_file)
    group_name = "expresses"

    if msg.forward_from.username:
        database.add_user(group_name, msg.forward_from.id,
                          msg.forward_from.username,
                          msg.forward_from.full_name)
        await msg.reply(new_user.format(msg.forward_from.username))
    else:
        await msg.reply(no_username.format(msg.forward_from.full_name))

