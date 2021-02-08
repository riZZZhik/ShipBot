# Aiogram imports
from aiogram import types

# Module imports
from ..logger import log

from ..config import database_file, groups_dict
from ..database import Database
from ..texts import new_user, left_user, no_username, removed_user, remove_user_no_reply, unknown_chat


async def add_user(msg: types.Message):
    database = Database(database_file)
    try:
        group_name = groups_dict[msg.chat.id]
    except KeyError:
        await msg.reply(unknown_chat)
        log.info(f"Unknown group chat with id: {msg.chat.id}")

    if not msg.from_user.is_bot:
        if msg.from_user.username:
            database.add_user(group_name, msg.from_user.id,
                              msg.from_user.username,
                              msg.from_user.full_name)
        else:
            await msg.reply(no_username.format(msg.from_user.full_name))


async def remove_user(msg: types.Message):  # TODO: BlackList
    database = Database(database_file)
    group_name = groups_dict[msg.chat.id]

    if msg.reply_to_message:
        database.delete_user(group_name, msg.reply_to_message.from_user.id, msg.reply_to_message.from_user.username)
        await msg.reply(removed_user.format(msg.reply_to_message.from_user.username))
    else:
        await msg.reply(remove_user_no_reply)


async def new_member(msg: types.Message):
    database = Database(database_file)
    group_name = "expresses"
    for user in msg.new_chat_members:
        if not user.is_bot:
            if user.username:
                database.add_user(group_name, user.id,
                                  user.username,
                                  user.full_name)
                await msg.reply(new_user.format(user.username))
            else:
                await msg.reply(no_username.format(msg.from_user.full_name))


async def user_left(msg: types.Message):
    database = Database(database_file)
    group_name = groups_dict[msg.chat.id]

    database.delete_user(group_name, msg.left_chat_member.id, msg.left_chat_member.username)

    await msg.reply(left_user)
