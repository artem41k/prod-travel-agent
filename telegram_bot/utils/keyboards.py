from aiogram import types
from aiogram.filters.callback_data import CallbackData

from . import msgs, callbacks

CLEAR = types.ReplyKeyboardRemove()
MENU_BUTTON = (msgs.menu_button_text, callbacks.MenuCallback())


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


def request_location_markup() -> types.ReplyKeyboardMarkup:
    return types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(
                text=msgs.share_location_button, request_location=True
            )]
        ]
    )


def stop_markup() -> types.ReplyKeyboardMarkup:
    return build_reply_markup([msgs.stop])


def extract_cb_data(data: CallbackData | str) -> str:
    return data.pack() if isinstance(data, CallbackData) else data


def build_inline_markup(buttons: list) -> types.InlineKeyboardMarkup:
    kb = []
    for item in buttons:
        if isinstance(item, list):
            kb.append(
                [
                    types.InlineKeyboardButton(
                        text=text, callback_data=extract_cb_data(data)
                    )
                    for text, data in item
                ]
            )
        else:
            kb.append([
                types.InlineKeyboardButton(
                    text=item[0], callback_data=extract_cb_data(item[1])
                )
            ])
    return types.InlineKeyboardMarkup(inline_keyboard=kb)
