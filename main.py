import asyncio
import logging
from bot_config import bot, dp, database


from handlers.start import start_router
from handlers.homework import homework_router


async def on_startup():
    print("Бот запустился")
    database.create_tables()


async def main():
    dp.include_router(start_router)
    dp.include_router(homework_router)
    await on_startup()
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())