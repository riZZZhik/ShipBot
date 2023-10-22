"""User log functions."""
from aiogram import types

from ..config import config
from ..database import Database
from ..logger import log
from ..texts import left_user, new_user, no_username, remove_user_no_reply, removed_user


async def add_user(msg: types.Message) -> None:
    """Add user to database.

    Args:
        msg: aiogram Message.
    """
    database = Database(config.database_file)

    if not msg.from_user.is_bot:
        if msg.from_user.username:
            database.add_user(
                msg.chat.id,
                msg.from_user.id,
                msg.from_user.username,
                msg.from_user.full_name,
            )
        else:
            await msg.reply(no_username.format(msg.from_user.full_name))


async def remove_user(msg: types.Message) -> None:
    """Remove user from database.

    Args:
        msg: aiogram Message.
    """
    database = Database(config.database_file)

    if msg.reply_to_message:
        database.delete_user(
            msg.chat.id,
            msg.reply_to_message.from_user.id,
            msg.reply_to_message.from_user.username,
        )
        await msg.reply(removed_user.format(msg.reply_to_message.from_user.username))
    else:
        await msg.reply(remove_user_no_reply)


async def new_member(msg: types.Message) -> None:
    """Add new member to database.

    Args:
        msg: aiogram Message.
    """
    database = Database(config.database_file)
    for user in msg.new_chat_members:
        if not user.is_bot:
            if user.username:
                database.add_user(msg.chat.id, user.id, user.username, user.full_name)
                await msg.reply(new_user.format(user.username))
            else:
                await msg.reply(no_username.format(msg.from_user.full_name))


async def user_left(msg: types.Message) -> None:
    """Remove user from database.

    Args:
        msg: aiogram Message.
    """
    database = Database(config.database_file)

    database.delete_user(msg.chat.id, msg.left_chat_member.id, msg.left_chat_member.username)

    await msg.reply(left_user)
