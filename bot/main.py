import asyncio
import sys

from aiogram import Bot, Dispatcher, types
from aiogram.bot.api import TelegramAPIServer

from bot.handlers import Handlers
from common.settings import async_session
from bot.settings import BOT_TOKEN, TELEGRAM_LOCAL_API, SUPPORTED_CONTENT_TYPES

if not BOT_TOKEN:
    print("[err] TELEGRAM_BOT_TOKEN missing")
    sys.exit(1)

local_server = TelegramAPIServer.from_base(TELEGRAM_LOCAL_API)
bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML, server=local_server)


async def main():
    try:
        async with async_session() as session:
            async with session.begin():
                handlers = Handlers(bot=bot, session=session)

        disp = Dispatcher(bot=bot)
        disp.register_message_handler(handlers.start_handler, commands={"start"})
        disp.register_message_handler(handlers.message_handler)
        disp.register_message_handler(handlers.message_handler, content_types=SUPPORTED_CONTENT_TYPES)
        await disp.start_polling()
    finally:
        await bot.close()


if __name__ == '__main__':
    asyncio.run(main())
