import config
from aiogram import Bot, Dispatcher, executor
from src import on_shutdown, setup

# Initialize ShipBot and dispatcher
bot = Bot(token=config.API_TOKEN)
dp = Dispatcher(bot)

# Initialize handlers
setup(dp)

# Run executor
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_shutdown=on_shutdown)
