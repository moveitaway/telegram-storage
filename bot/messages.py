import os.path

from utils import human_size


def HELLO() -> str:
    return ("<b>[Telegram File Storage bot]</b>\n\n" +
            "Welcome to Telegram File Storage bot. " +
            "To use this bot just me the file that you want to upload to my server.")


def UNSUPPORTED_MESSAGE() -> str:
    return ("<b>[Unsupported content]</b>\n\n" +
            "Oh no! It seems I cannot handle this message right now.\n\n" +
            "At this moment I only accept animations, photos, audios, videos, voices and documents.")


def UNEXPECTED_ERROR() -> str:
    return ("<b>[Unexpected error]</b>\n\n" +
            "Oh no! Something went wrong. Please try again.")


def SAVED(file_path: str, file_size: int, need_preview: bool) -> str:
    return ("<b>[Successfully saved]</b>\n\n"
            f"<b>📁 Location</b>: Inbox\n"
            f"<b>🗒 Name</b>: <code>{os.path.basename(file_path)}</code>\n"
            f"<b>🔢 Size</b>: {human_size(file_size)}\n\n"
            f"<code>{file_path}</code>\n\n"
            "⏱ this message (not file) will be deleted after 30 seconds of inactivity"
            + (f"<a href=\"{file_path}\">ㅤ</a>" if need_preview else ""))
