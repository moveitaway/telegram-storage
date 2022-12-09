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
