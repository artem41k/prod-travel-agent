from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram import F, Router, types
from aiogram.filters import CommandStart

from utils import msgs, keyboards, api

router = Router()


class Registration(StatesGroup):
    name = State()
    age = State()
    bio = State()
    interests = State()
    location = State()


@router.message(CommandStart())
async def handle_start(message: types.Message, state: FSMContext):
    api_instance = api.API(message.from_user.id)
    profile, status_code = api_instance.get_profile()

    if status_code == 200:  # If user profile has been found
        await message.answer(
            msgs.hello_again % profile['first_name'],
            reply_markup=keyboards.CLEAR
        )
    else:
        await state.set_state(Registration.name)
        await state.update_data(api_instance=api_instance)
        await message.answer(msgs.start_msg)
        reply_markup = keyboards.skip_markup()
        await message.answer(msgs.ask_for_name, reply_markup=reply_markup)


@router.message(Registration.name)
async def handle_name(message: types.Message, state: FSMContext):
    name = message.text.strip()
    if name == msgs.skip:
        first_name = message.from_user.first_name
        last_name = message.from_user.last_name  # may be None
    else:
        spl = name.split()
        first_name = spl[0]
        last_name = spl[1] if len(spl) > 1 else None

    await state.update_data(first_name=first_name, last_name=last_name)
    await state.set_state(Registration.age)

    reply_markup = keyboards.skip_markup()
    await message.answer(msgs.ask_for_age, reply_markup=reply_markup)


@router.message(Registration.age)
async def handle_age(message: types.Message, state: FSMContext):
    reply_markup = keyboards.skip_markup()
    text = message.text.strip()

    if text == msgs.skip:
        await state.set_state(Registration.bio)
        await message.answer(
            msgs.ask_for_bio, reply_markup=reply_markup
        )
        return

    if not text.isdigit():
        await message.answer(msgs.age_parse_error, reply_markup=reply_markup)
        return

    age = int(text)

    if age > 100:
        await message.answer(
            msgs.try_again % msgs.i_dont_believe,
            reply_markup=reply_markup
        )
        return

    await state.update_data(age=age)
    await state.set_state(Registration.bio)

    await message.answer(
        msgs.ask_for_bio, reply_markup=reply_markup
    )


@router.message(Registration.bio)
async def handle_bio(message: types.Message, state: FSMContext):
    text = message.text.strip()

    if text != msgs.skip:
        await state.update_data(bio=text)
    await state.set_state(Registration.location)
    await message.answer(
        msgs.ask_for_location,
        reply_markup=keyboards.request_location_markup()
    )


@router.message(Registration.location, F.location)
async def handle_location(
        message: types.Message, state: FSMContext):
    location = message.location

    await state.update_data(lat=location.latitude, lon=location.longitude)
    await end_registration(message, state)


@router.message(Registration.location)
async def handle_text_location(
        message: types.Message, state: FSMContext):
    text = message.text.strip()

    if len(text.split(", ")) != 2:
        await message.answer(msgs.wrong_location)
        return

    await state.update_data(location=text)
    await end_registration(message, state)


async def end_registration(message: types.Message, state: FSMContext):
    data = await state.get_data()

    api_instance = data.pop('api_instance')

    new_profile, status_code = api_instance.create_user(**data)

    if status_code in (400, 404):
        await message.answer(msgs.location_not_found)
    else:
        await state.clear()

        await message.answer(msgs.profile_is_ready)
        await message.answer(msgs.get_profile_msg(**new_profile))
