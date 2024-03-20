from aiogram import types

from . import msgs

CLEAR = types.ReplyKeyboardRemove()


def build_reply_markup(buttons: list) -> types.ReplyKeyboardMarkup:
    kb = []
    for item in buttons:
        if isinstance(item, list):
            kb.append([types.KeyboardButton(text=str(b)) for b in item])
        else:
            kb.append([types.KeyboardButton(text=str(item))])
    return types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)


def skip_markup() -> types.ReplyKeyboardMarkup:
    return build_reply_markup([msgs.skip])
