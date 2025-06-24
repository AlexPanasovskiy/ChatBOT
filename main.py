import asyncio

from aiogram import Bot, Dispatcher
from app.handlers import router


async def main():
    bot = Bot(token='7758971853:AAH9iINPtDHoeZ1lW9HXrk5-nK3aITQIU30')
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот завершил работу.')