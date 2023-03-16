import asyncio

from aiogram import types, Bot
from aiogram.types import User as TgUser
from sqlalchemy.ext.asyncio import AsyncSession

from bot import messages
from bot.keyboards import file_link_markup
from bot.messages import HELLO
from bot.utils import find_biggest_photo, download_file, get_public_file_link
from common.crud import UsersCrud, FilesCrud
from common.models import User, File, FILE_TYPE_IMAGE, FILE_TYPE_DOCUMENT, FILE_TYPE_AUDIO, FILE_TYPE_GIF, \
    FILE_TYPE_VIDEO


class Handlers:
    def __init__(self, bot: Bot, session: AsyncSession):
        self.bot = bot
        self.users_crud = UsersCrud(session)
        self.files_crud = FilesCrud(session)

    async def start_handler(self, event: types.Message):
        user = await self._get_or_create_user(event.from_user)
        return await self.bot.send_photo(chat_id=user.telegram_id, caption=HELLO(),
                                         photo=types.InputFile("assets/telegram_logo.jpg"), )

    async def message_handler(self, message: types.Message):
        if not any(bool(v) for v in
                   [message.photo, message.document, message.audio, message.animation, message.video, message.voice]):
            return await message.reply(messages.UNSUPPORTED_MESSAGE())

        need_preview = False
        if bool(message.photo):
            photo_to_download = find_biggest_photo(message.photo)
            if not photo_to_download:
                raise RuntimeError('This code should not be reached')
            file_id = photo_to_download.file_id
            file_type = FILE_TYPE_IMAGE
            need_preview = True
        elif message.document is not None:
            file_id = message.document.file_id
            file_type = FILE_TYPE_DOCUMENT
            need_preview = True
        elif message.audio is not None:
            file_id = message.audio.file_id
            file_type = FILE_TYPE_AUDIO
        elif message.animation is not None:
            file_id = message.animation.file_id
            file_type = FILE_TYPE_GIF
            need_preview = True
        elif message.video is not None:
            file_id = message.video.file_id
            file_type = FILE_TYPE_VIDEO
            need_preview = True
        elif message.voice is not None:
            file_id = message.voice.file_id
            file_type = FILE_TYPE_AUDIO
        else:
            raise RuntimeError('This code should not be reached')

        file_info = await self.bot.get_file(file_id)
        uploaded_file = await download_file(file_info.file_path)
        if not uploaded_file:
            return await message.reply(messages.UNEXPECTED_ERROR())
        public_file_path = get_public_file_link(uploaded_file.public_path)

        user = await self._get_or_create_user(message.from_user)
        inbox = await self.files_crud.get_or_create_inbox_folder(user)
        file = File(user_id=user.id, type=file_type, name=uploaded_file.name, path=f"{inbox.path}.{inbox.id}",
                    size=uploaded_file.size,
                    location=uploaded_file.public_path)
        await self.files_crud.persist(file)

        answer = await message.answer(messages.SAVED(public_file_path, uploaded_file.size, need_preview),
                                      reply_markup=file_link_markup(public_file_path), disable_web_page_preview=False)
        await asyncio.sleep(delay=3)
        await message.delete()
        await asyncio.sleep(delay=27)
        return await answer.delete()  # todo move this logic to async worker

    async def _get_or_create_user(self, tg_user: TgUser) -> User:
        user = await self.users_crud.find_by_telegram_id(tg_user.id)
        if not user:
            user = User(telegram_id=tg_user.id, extra={"full_name": tg_user.full_name, "username": tg_user.username})
            user = await self.users_crud.persist(user)
            await self.files_crud.get_or_create_inbox_folder(user)

        return user
