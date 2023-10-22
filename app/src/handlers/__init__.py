"""Handlers for bot."""
from aiogram import Dispatcher, types

from .admin_funcs import get_base, info
from .couple_func import make_couple
from .info_funcs import get_group_info, get_user_info
from .start_func import start
from .user_log_funcs import add_user, new_member, remove_user, user_left


def setup(dp: Dispatcher) -> None:
    """Register handlers.

    Args:
        dp: aiogram Dispatcher.
    """
    custom_filter = lambda msg: not msg.from_user.is_bot and msg.chat.type != "private"

    dp.register_message_handler(start, commands=["start"])
    dp.register_message_handler(make_couple, custom_filter, commands=["makecouple"])

    dp.register_message_handler(info, commands=["info"])
    dp.register_message_handler(get_base, custom_filter, commands=["get_base"], is_chat_admin=True)

    dp.register_message_handler(get_user_info, custom_filter, commands=["mystat"])
    dp.register_message_handler(get_group_info, custom_filter, commands=["allstat"])

    dp.register_message_handler(remove_user, custom_filter, commands=["remove"], is_chat_admin=True)

    dp.register_message_handler(
        new_member, custom_filter, content_types=types.ContentType.NEW_CHAT_MEMBERS
    )
    dp.register_message_handler(
        user_left, custom_filter, content_types=types.ContentType.LEFT_CHAT_MEMBER
    )
    dp.register_message_handler(add_user, custom_filter)
