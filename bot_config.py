from aiogram import Bot, Dispatcher
from dotenv import dotenv_values
from databases.database import Database


token = dotenv_values(".env")["BOT_TOKEN"]
bot = Bot(token=token)
dp = Dispatcher()
database = Database("databases/database.db")
