def HELLO() -> str:
    return ("<b>[Telegram File Storage bot]</b>\n\n" +
            "Welcome to Telegram File Storage bot." +
            "To use this bot just me the file that you want to upload to my server.")


def UNSUPPORTED_MESSAGE() -> str:
    return ("<b>[Unsupported content]</b>\n\n" +
            "Oh no! It seems I cannot handle this message right now.\n\n" +
            "At this moment I only accept animations, photos, audios, videos, voices and documents.")


def UNEXPECTED_ERROR() -> str:
    return ("<b>[Unexpected error]</b>\n\n" +
            "Oh no! Something went wrong. Please try again.")


def SAVED(file_path: str) -> str:
    return ("<b>[Successfully saved]</b>\n\n" +
            "File successfully saved. You can download it using following link:\n\n" +
            f"<code>{file_path}</code>")
