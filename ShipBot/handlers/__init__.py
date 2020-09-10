# Aiogram imports
from aiogram import types

# Imports functions
from .start_func import start
from .Couple_func import make_couple
from .admin_funcs import get_base, get_info
from .user_log_funcs import new_member, member_left


def setup(dp):
    # Initialize handlers
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(make_couple, commands=['MakeCouple'])

    dp.register_message_handler(get_base, commands=['secret'])
    dp.register_message_handler(get_info, commands=['info'])

    dp.register_message_handler(new_member, lambda msg: not msg.new_chat_members[0].is_bot,
                                content_types=types.ContentType.NEW_CHAT_MEMBERS)
    dp.register_message_handler(member_left, lambda msg: not msg.left_chat_member.is_bot,
                                content_types=types.ContentType.LEFT_CHAT_MEMBER)
