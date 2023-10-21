# Aiogram imports
from aiogram import Dispatcher, types

from .admin_funcs import get_base, info
from .couple_func import make_couple
from .info_funcs import get_group_info, get_user_info

# Imports functions
from .start_func import start
from .user_log_funcs import add_user, new_member, remove_user, user_left


# Initialize handlers
def setup(dp: Dispatcher):
    dp.register_message_handler(start, commands=["start"])
    dp.register_message_handler(make_couple, commands=["makecouple"])

    dp.register_message_handler(info, commands=["info"], is_chat_admin=True)
    dp.register_message_handler(get_base, commands=["base"], is_chat_admin=True)

    dp.register_message_handler(get_user_info, commands=["mystat"])
    dp.register_message_handler(get_group_info, commands=["allstat"])

    dp.register_message_handler(remove_user, commands=["remove"], is_chat_admin=True)

    dp.register_message_handler(
        new_member,
        lambda msg: not msg.new_chat_members[0].is_bot,
        content_types=types.ContentType.NEW_CHAT_MEMBERS,
    )
    dp.register_message_handler(
        user_left,
        lambda msg: not msg.left_chat_member.is_bot,
        content_types=types.ContentType.LEFT_CHAT_MEMBER,
    )
    dp.register_message_handler(add_user, lambda msg: not msg.from_user.is_bot)
