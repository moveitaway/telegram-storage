from typing import List

from aiogram.types import PhotoSize


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
