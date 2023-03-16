from os import getenv

from aiogram.types import ContentType
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_LOCAL_API = getenv('TELEGRAM_LOCAL_API', 'http://localhost:8081')

SUPPORTED_CONTENT_TYPES = [ContentType.PHOTO, ContentType.DOCUMENT, ContentType.AUDIO, ContentType.ANIMATION,
                           ContentType.VIDEO, ContentType.VOICE]
UPLOAD_DIRECTORY = getenv('UPLOAD_DIRECTORY', '../uploads')
PUBLIC_URL_PREFIX = getenv('PUBLIC_URL_PREFIX', 'https://example.com/')
