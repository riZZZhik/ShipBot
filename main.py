# Aiogram imports
from aiogram import Bot, Dispatcher, executor

# Import ShipBot module
import app
from config import API_TOKEN

# Initialize ShipBot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Initialize handlers
app.setup(dp)

# Run executor
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_shutdown=app.on_shutdown)
