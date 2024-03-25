from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from utils import msgs, keyboards, api
from utils.callbacks import ProfileCallback

router = Router()


@router.callback_query(ProfileCallback.filter(F.action == 'view'))
async def handle_profile_view(call: types.CallbackQuery,
                              state: FSMContext):
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
        await message.answer(
            msgs.get_profile_msg(**profile),
            reply_markup=keyboards.build_inline_markup([keyboards.MENU_BUTTON])
        )


@router.callback_query(
    ProfileCallback.filter(F.action == 'edit' and F.field == 'name')
)
async def handle_name_edit_call(call: types.CallbackQuery,
                                callback_data: ProfileCallback,
                                state: FSMContext):
    await call.answer()
    await call.message.answer(
        msgs.ask_for_name, reply_markup=keyboards.skip_markup()
    )
    await state.set_state(ProfileEdit.name)


@router.message(ProfileEdit.name)
async def handle_name(message: types.Message, state: FSMContext):
    name = message.text.strip()
    if name == msgs.skip:
        first_name = message.from_user.first_name
        last_name = message.from_user.last_name  # may be None
    else:
        spl = name.split()
        first_name = spl[0]
        last_name = spl[1] if len(spl) > 1 else None

    profile, status_code = api.API(
        message.from_user.id
    ).update_user(first_name=first_name, last_name=last_name)

    if status_code == 200:
        await message.answer(msgs.name_edited, reply_markup=keyboards.CLEAR)
        await state.clear()
        await message.answer(
            msgs.get_profile_msg(**profile),
            reply_markup=keyboards.build_inline_markup([keyboards.MENU_BUTTON])
        )


@router.callback_query(
    ProfileCallback.filter(F.action == 'edit' and F.field == 'age')
)
async def handle_age_edit_call(call: types.CallbackQuery,
                               callback_data: ProfileCallback,
                               state: FSMContext):
    await call.answer()
    await call.message.answer(
        msgs.ask_for_age, reply_markup=keyboards.CLEAR
    )
    await state.set_state(ProfileEdit.age)


@router.message(ProfileEdit.age)
async def handle_age(message: types.Message, state: FSMContext):
    text = message.text.strip()
    if text == msgs.skip:
        age = None
    else:
        if not text.isdigit():
            await message.answer(msgs.age_parse_error)
            return

        age = int(text)

        if age > 100:
            await message.answer(msgs.try_again % msgs.i_dont_believe)
            return

    profile, status_code = api.API(
        message.from_user.id
    ).update_user(age=age)

    if status_code == 200:
        await message.answer(msgs.age_edited, reply_markup=keyboards.CLEAR)
        await state.clear()
        await message.answer(
            msgs.get_profile_msg(**profile),
            reply_markup=keyboards.build_inline_markup([keyboards.MENU_BUTTON])
        )


@router.callback_query(
    ProfileCallback.filter(F.action == 'edit' and F.field == 'bio')
)
async def handle_bio_edit_call(call: types.CallbackQuery,
                               callback_data: ProfileCallback,
                               state: FSMContext):
    await call.answer()
    await call.message.answer(
        msgs.ask_for_bio, reply_markup=keyboards.skip_markup()
    )
    await state.set_state(ProfileEdit.bio)


@router.message(ProfileEdit.bio)
async def handle_bio(message: types.Message, state: FSMContext):
    text = message.text.strip()

    if text != msgs.skip:
        bio = text
    else:
        bio = None

    profile, status_code = api.API(
        message.from_user.id
    ).update_user(bio=bio)

    if status_code == 200:
        await message.answer(msgs.bio_edited, reply_markup=keyboards.CLEAR)
        await state.clear()
        await message.answer(
            msgs.get_profile_msg(**profile),
            reply_markup=keyboards.build_inline_markup([keyboards.MENU_BUTTON])
        )
