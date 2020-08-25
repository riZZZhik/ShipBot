# Aiogram imports
from aiogram import types

# Imports functions
from .start_func import start
from .Couple_func import make_couple
from .admin_funcs import get_base


def setup(dp):
    # Initialize handlers
    dp.register_message_handler(start, types.ChatType.is_private, commands=['start'])
    dp.register_message_handler(get_base, commands=['secret'])
    dp.register_message_handler(make_couple, commands=['MakeCouple'])
