from aiogram import F, Router, types
from aiogram.filters import Command

from utils import msgs, callbacks, keyboards

router = Router()

# TODO: Add current trip button and info about the next trip


async def get_menu(user_id: int) -> tuple[str, types.InlineKeyboardMarkup]:
    buttons = [
        (msgs.trips_button, callbacks.TripCallback(action='list')),
        (msgs.profile_button, callbacks.ProfileCallback(action='view')),
    ]
    markup = keyboards.build_inline_markup(buttons)
    return msgs.main_menu_text, markup


@router.message(Command('menu'))
@router.message(F.text == msgs.menu_button_text)
async def handle_menu_message(message: types.Message):
    text, markup = await get_menu(message.from_user.id)
    await message.answer(text, reply_markup=markup)


@router.callback_query(callbacks.MenuCallback.filter())
async def handle_menu_call(call: types.CallbackQuery):
    text, markup = await get_menu(call.from_user.id)
    await call.answer()
    await call.message.edit_text(text, reply_markup=markup)
