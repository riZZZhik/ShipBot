from config import API_TOKEN

# Aiogram imports
from aiogram import Bot, Dispatcher, executor

# Import ShipBot module
import ShipBot
# Import database library
from ShipBot import database_file
from ShipBot.database import Database

# Initialize sqlite database
database = Database(database_file)
# Initialize ShipBot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Initialize handlers
ShipBot.setup(dp)

# Run executor
if __name__ == '__main__':
    # dp.middleware.setup(ThrottlingMiddleware())
    executor.start_polling(dp, skip_updates=True, on_shutdown=ShipBot.on_shutdown)
