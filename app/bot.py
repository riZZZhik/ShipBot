"""Telegram Ship bot."""
from aiogram import Bot, Dispatcher, executor
from src import config, on_shutdown, setup


def run_bot():
    # Initialize ShipBot and dispatcher
    bot = Bot(token=config.TOKEN)
    dp = Dispatcher(bot)

    # Initialize handlers
    setup(dp)

    # Run bot
    executor.start_polling(dp, skip_updates=True, on_shutdown=on_shutdown)


# Run executor
if __name__ == "__main__":
    run_bot()
