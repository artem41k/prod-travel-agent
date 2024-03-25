from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from utils import msgs, callbacks, keyboards, api

router = Router()

# TODO: Add current trip button and info about the next trip


async def get_menu(user_id: int) -> tuple[str, types.InlineKeyboardMarkup]:
    buttons = [
        (msgs.trips_button, callbacks.TripCallback(action='list')),
        (msgs.profile_button, callbacks.ProfileCallback(action='view')),
    ]
    trips, status_code = api.API(user_id).get_trips()
    if status_code == 200:
        if len(trips) > 0:
            soonest = sorted(trips, key=lambda trip: trip['start_date'])[0]
            buttons.insert(
                0,
                (
                    msgs.soonest_trip_button,
                    callbacks.TripCallback(action='view', id=soonest['id'])
                )
            )
    markup = keyboards.build_inline_markup(buttons)
    return msgs.main_menu_text, markup


@router.message(Command('menu'))
@router.message(F.text == msgs.menu_button_text)
async def handle_menu_message(message: types.Message, state: FSMContext):
    await state.clear()
    text, markup = await get_menu(message.from_user.id)
    await message.answer(text, reply_markup=markup)


@router.callback_query(callbacks.MenuCallback.filter())
async def handle_menu_call(call: types.CallbackQuery, state: FSMContext):
    await state.clear()
    text, markup = await get_menu(call.from_user.id)
    await call.answer()
    await call.message.edit_text(text, reply_markup=markup)
