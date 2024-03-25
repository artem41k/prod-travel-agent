from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from utils import msgs, keyboards, api
from utils.callbacks import ProfileCallback

router = Router()


@router.callback_query(ProfileCallback.filter(F.action == 'view'))
async def handle_profile_view(call: types.CallbackQuery,
                              state: FSMContext):
    print(state, type(state))
    profile, status_code = api.API(call.from_user.id).get_profile()
    if status_code == 200:
        buttons = [
            (msgs.choose_what_to_edit, 'none'),
            [
                (
                    msgs.profile_labels['name'],
                    ProfileCallback(action='edit', field='name')
                ),
                (
                    msgs.profile_labels['age'],
                    ProfileCallback(action='edit', field='age')
                ),
            ],
            [
                (
                    msgs.profile_labels['location'],
                    ProfileCallback(action='edit', field='location')
                ),
                (
                    msgs.profile_labels['bio'],
                    ProfileCallback(action='edit', field='bio')
                ),
            ],
            keyboards.MENU_BUTTON,
        ]
        markup = keyboards.build_inline_markup(buttons)

        await call.answer()
        await call.message.edit_text(
            msgs.get_profile_msg(**profile),
            reply_markup=markup
        )
    else:
        await call.answer(msgs.internal_error)


class ProfileEdit(StatesGroup):
    name = State()
    age = State()
    location = State()
    bio = State()


@router.callback_query(
    ProfileCallback.filter(F.action == 'edit' and F.field == 'location')
)
async def handle_location_edit_call(call: types.CallbackQuery,
                                    callback_data: ProfileCallback,
                                    state: FSMContext):
    await call.answer()
    await call.message.answer(
        msgs.ask_for_location, reply_markup=keyboards.request_location_markup()
    )
    await state.set_state(ProfileEdit.location)


@router.message(ProfileEdit.location, F.location)
async def handle_location(
        message: types.Message, state: FSMContext):
    location = message.location

    await state.update_data(lat=location.latitude, lon=location.longitude)
    await update_location(message, state)


@router.message(ProfileEdit.location)
async def handle_text_location(
        message: types.Message, state: FSMContext):
    text = message.text.strip()

    if len(text.split(", ")) != 2:
        await message.answer(msgs.wrong_location)
        return

    await state.update_data(location=text)
    await update_location(message, state)


async def update_location(message: types.Message, state: FSMContext):
    api_inst = api.API(message.from_user.id)
    data = await state.get_data()

    profile, status_code = api_inst.update_user(**data)

    if status_code in (400, 404):
        await message.answer(msgs.location_not_found)
    else:
        await state.clear()
        await message.answer(msgs.get_profile_msg(**profile))
