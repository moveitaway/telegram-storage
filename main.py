import asyncio
import os
import sys
from os import getenv
from secrets import token_hex

from aiogram import Bot, Dispatcher, types
from aiogram.bot.api import TelegramAPIServer
from aiogram.types import ContentType
from aioshutil import move

import messages
from utils import find_biggest_photo

BOT_TOKEN = getenv('TELEGRAM_BOT_TOKEN')
if not BOT_TOKEN:
    print("[err] TELEGRAM_BOT_TOKEN missing")
    sys.exit(1)

TELEGRAM_LOCAL_API = getenv('TELEGRAM_LOCAL_API', 'http://localhost:8081')

SUPPORTED_CONTENT_TYPES = [ContentType.PHOTO, ContentType.DOCUMENT, ContentType.AUDIO, ContentType.ANIMATION,
                           ContentType.VIDEO, ContentType.VOICE]
UPLOAD_DIRECTORY = getenv('UPLOAD_DIRECTORY', 'uploads')
PUBLIC_URL_PREFIX = getenv('PUBLIC_URL_PREFIX', 'https://example.com/')

local_server = TelegramAPIServer.from_base(TELEGRAM_LOCAL_API)
bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML, server=local_server)


async def download_file(file_path: str) -> str | None:
    # we have to have telegram-bot-api mounted to bot container
    local_file_path = file_path.replace('/var/lib/telegram-bot-api', 'telegram-bot-api-data')

    extension = f'.{local_file_path[-3:]}' if '.' in local_file_path else ''
    file_name = token_hex(32)
    os.makedirs(os.path.join(UPLOAD_DIRECTORY, file_name[0], file_name[1], file_name[2]))
    output_file_name = os.path.join(UPLOAD_DIRECTORY, file_name[0], file_name[1], file_name[2],
                                    f'{file_name}{extension}')
    await move(local_file_path, output_file_name)

    return output_file_name.replace(UPLOAD_DIRECTORY, '')[1:]


def get_public_file_link(file_name: str) -> str:
    return os.path.join(PUBLIC_URL_PREFIX, file_name)


def file_link_markup(public_file_path: str) -> types.InlineKeyboardMarkup:
    reply_markup = types.InlineKeyboardMarkup()
    reply_markup.row(
        types.InlineKeyboardButton('Download file', url=public_file_path))

    return reply_markup


async def start_handler(event: types.Message):
    await event.answer(
        messages.HELLO(),
        parse_mode=types.ParseMode.HTML,
    )


async def message_handler(message: types.Message):
    if not any(bool(v) for v in
               [message.photo, message.document, message.audio, message.animation, message.video, message.voice]):
        return await message.reply(messages.UNSUPPORTED_MESSAGE())

    if bool(message.photo):
        photo_to_download = find_biggest_photo(message.photo)
        if not photo_to_download:
            raise RuntimeError('This code should not be reacted')
        file_id = photo_to_download.file_id
    elif message.document is not None:
        file_id = message.document.file_id
    elif message.audio is not None:
        file_id = message.audio.file_id
    elif message.animation is not None:
        file_id = message.animation.file_id
    elif message.video is not None:
        file_id = message.video.file_id
    elif message.voice is not None:
        file_id = message.voice.file_id
    else:
        raise RuntimeError('This code should not be reached')

    file_info = await bot.get_file(file_id)
    downloaded_file_path = await download_file(file_info.file_path)
    if not downloaded_file_path:
        return await message.reply(messages.UNEXPECTED_ERROR())
    public_file_path = get_public_file_link(downloaded_file_path)

    return await message.reply(messages.SAVED(public_file_path),
                               reply_markup=file_link_markup(public_file_path))


async def main():
    try:
        disp = Dispatcher(bot=bot)
        disp.register_message_handler(start_handler, commands={"start"})
        disp.register_message_handler(message_handler)
        disp.register_message_handler(message_handler, content_types=SUPPORTED_CONTENT_TYPES)
        await disp.start_polling()
    finally:
        await bot.close()


if __name__ == '__main__':
    asyncio.run(main())
