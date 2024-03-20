from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram import F, Router, types
from aiogram.filters import CommandStart

from utils import msgs, keyboards

router = Router()


class Registration(StatesGroup):
    name = State()
    age = State()
    city_and_country = State()
    bio = State()
    interests = State()


@router.message(CommandStart())
async def handle_start(message: types.Message, state: FSMContext):
    await state.set_state(Registration.name)
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
        await state.set_state(Registration.city_and_country)
        await message.answer(
            msgs.ask_for_city_and_country, reply_markup=keyboards.CLEAR
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
    await state.set_state(Registration.city_and_country)

    await message.answer(
        msgs.ask_for_city_and_country, reply_markup=keyboards.CLEAR
    )


@router.message(Registration.city_and_country, F.location)
async def handle_location_city_and_country(
        message: types.Message, state: FSMContext):
    location = message.location

    reply_markup = keyboards.skip_markup()

    await state.update_data(location=location)
    await state.set_state(Registration.bio)
    await message.answer(msgs.ask_for_bio, reply_markup=reply_markup)


@router.message(Registration.city_and_country)
async def handle_city_and_country(
        message: types.Message, state: FSMContext):
    spl = message.text.strip().split(", ")

    reply_markup = keyboards.skip_markup()

    if len(spl) != 2:
        await message.answer(
            msgs.wrong_city_and_country, reply_markup=reply_markup
        )
        return

    # validate_city_and_country

    await state.set_state(Registration.bio)
    await message.answer(msgs.ask_for_bio, reply_markup=reply_markup)


@router.message(Registration.bio)
async def handle_bio(message: types.Message, state: FSMContext):
    text = message.text.strip()

    if text != msgs.skip:
        await state.update_data(bio=text)
    await end_registration(message, state)


async def end_registration(message: types.message, state: FSMContext):
    data = await state.get_data()

    print(data)  # For debug

    # call api to create a user
