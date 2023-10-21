"""Start function."""
from aiogram import types


async def start(msg: types.Message) -> None:
    """Reply with start message.

    Args:
        msg: aiogram Message.
    """
    await msg.reply(
        "Hi. I'm Cupid bot. I can make couples in your chat."
        " Add me to your group and use /makecouple command."
    )
