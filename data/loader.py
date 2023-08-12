from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from database.database import DataBase
bot = Bot('6037875681:AAFTM0bUFC_Y4wMQyA0SaLw_OSw-ZXjgpKw', parse_mode='HTML')
db = DataBase()
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


