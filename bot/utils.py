import dataclasses
import os
import pathlib

from aioshutil import move
from typing import List

from aiogram.types import PhotoSize
from shortuuid import uuid

from bot.settings import UPLOAD_DIRECTORY, PUBLIC_URL_PREFIX


@dataclasses.dataclass
class UploadedFile:
    public_path: str
    fs_path: str
    name: str
    size: int


async def download_file(file_path: str) -> UploadedFile | None:
    # we have to have telegram-bot-api mounted to bot container
    local_file_path = file_path.replace('/var/lib/telegram-bot-api', 'telegram-bot-api-data')

    extension = pathlib.Path(local_file_path).suffix if '.' in local_file_path else ''
    file_name = uuid()
    os.makedirs(os.path.join(UPLOAD_DIRECTORY, file_name[0], file_name[1]))
    os.chmod(os.path.join(UPLOAD_DIRECTORY, file_name[0]), 0o2755)
    os.chmod(os.path.join(UPLOAD_DIRECTORY, file_name[0], file_name[1]), 0o2755)
    output_file_name = os.path.join(UPLOAD_DIRECTORY, file_name[0], file_name[1],
                                    f'{file_name}{extension}')
    await move(local_file_path, output_file_name)
    os.chmod(output_file_name, mode=0o644)

    return UploadedFile(
        public_path=output_file_name.replace(UPLOAD_DIRECTORY, '')[1:],
        fs_path=output_file_name,
        name=os.path.basename(output_file_name),
        size=os.stat(output_file_name).st_size
    )


def get_public_file_link(file_name: str) -> str:
    return os.path.join(PUBLIC_URL_PREFIX, file_name)


def find_biggest_photo(photos: List[PhotoSize]) -> PhotoSize | None:
    if not photos:
        return None

    biggest = photos[0]
    for photo in photos:
        if biggest.width * biggest.height < photo.width * photo.height:
            biggest = photo

    return biggest


def human_size(bytes_: int, units: list | None = None) -> str:
    """ Returns a human-readable string representation of bytes """
    if units is None:
        units = [' bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB']
    return str(bytes_) + units[0] if bytes_ < 1024 else human_size(bytes_ >> 10, units[1:])
