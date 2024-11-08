import aiohttp
import asyncio

from aiogram import Bot, Dispatcher

from config import TG_TOKEN
from middlewares.db import DataBaseSession
from database.engine import create_db, session_maker
from handlers.user_private import router as user_private_router

bot = Bot(TG_TOKEN)
dp = Dispatcher()
dp.include_router(user_private_router)


async def on_startup():
    # await drop_db()
    await create_db()
    dp.http_session = aiohttp.ClientSession()

async def on_shutdown():
    await dp.http_session.close()
    await bot.session.close()


async def main():
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)    
    dp.update.middleware(DataBaseSession(session_poll=session_maker))

    try:
    #   await bot.set_my_commands(commands=private, scope=BotCommandScopeAllPrivateChats())
      await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
      dp.http_session = aiohttp.ClientSession()
    except KeyboardInterrupt:
        
        await bot.session.close()
        print("bot dont active")


if __name__ == "__main__":
    asyncio.run(main())

