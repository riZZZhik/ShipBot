# Aiogram imports
from aiogram import types


async def start(msg: types.Message):
    await msg.reply("Hi")
