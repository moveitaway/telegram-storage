from aiogram import types


def file_link_markup(public_file_path: str) -> types.InlineKeyboardMarkup:
    reply_markup = types.InlineKeyboardMarkup()
    reply_markup.row(types.InlineKeyboardButton('🌎 Open in Browser', url=public_file_path))
    # reply_markup.row(types.InlineKeyboardButton('📁 Move to Folder', callback_data='move_to_folder'))
    # reply_markup.row(types.InlineKeyboardButton('🗒 Add Note', callback_data='add_note'))

    return reply_markup
