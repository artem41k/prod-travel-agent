from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from utils import msgs, keyboards, api
from utils.callbacks import TripCallback

router = Router()


@router.callback_query(TripCallback.filter(F.action == 'list'))
async def handle_trip_list(
        call: types.CallbackQuery, callback_data: TripCallback):
    trips_list, status_code = api.API(call.from_user.id).get_trips()

    if status_code == 200:
        buttons = [
            (msgs.add_trip_button, TripCallback(action='create')),
            *[
                (trip['name'], TripCallback(action='view', id=trip['id']))
                for trip in trips_list
            ],
            keyboards.MENU_BUTTON,
        ]
        markup = keyboards.build_inline_markup(buttons)
        await call.answer()
        await call.message.edit_text(
            msgs.trips_header, reply_markup=markup
        )
    else:
        await call.answer(msgs.internal_error)


async def trip_view(event: types.Message | types.CallbackQuery,
                    trip_id: int,
                    provided_user_id: int | None = None):
    if isinstance(event, types.Message):
        message = event
        user_id = message.from_user.id
        call = False
    elif isinstance(event, types.CallbackQuery):
        message = event.message
        user_id = event.from_user.id
        call = True
    else:
        raise TypeError

    if provided_user_id:
        user_id = provided_user_id

    trip, status_code = api.API(user_id).get_trip(trip_id)

    if status_code == 200:
        if len(trip['locations']) > 0:
            buttons = [
                (msgs.route_button, TripCallback(action='route', id=trip_id)),
                (
                    msgs.edit_locations_button,
                    TripCallback(action='edit_locations', id=trip_id)
                )
            ]
        else:
            buttons = [
                (
                    msgs.add_locations_button,
                    TripCallback(action='add_locations', id=trip_id)
                )
            ]

        buttons += [
            (
                msgs.delete_trip_button,
                TripCallback(action='delete', id=trip_id)
            ),
            (msgs.edit_trip_button, TripCallback(action='edit', id=trip_id)),
            keyboards.MENU_BUTTON,
        ]

        markup = keyboards.build_inline_markup(buttons)

        if call:
            await message.edit_text(
                msgs.get_trip_msg(trip), reply_markup=markup
            )
        else:
            await message.answer(
                msgs.get_trip_msg(trip), reply_markup=markup
            )
    else:
        await event.answer(msgs.internal_error)


@router.callback_query(TripCallback.filter(F.action == 'view'))
async def handle_trip_view(
        call: types.CallbackQuery, callback_data: TripCallback):
    await trip_view(call, callback_data.id)


@router.callback_query(TripCallback.filter(F.action == 'show'))
async def handle_trip_show(
        call: types.CallbackQuery, callback_data: TripCallback):
    await trip_view(
        call.message, callback_data.id,
        provided_user_id=call.from_user.id
    )


class CreateTrip(StatesGroup):
    name = State()
    description = State()


@router.callback_query(TripCallback.filter(F.action == 'create'))
async def handle_trip_create(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.edit_text(msgs.create_trip)
    await state.set_state(CreateTrip.name)


@router.message(CreateTrip.name)
async def handle_trip_name(message: types.Message, state: FSMContext):
    text = message.text.strip()

    if len(text) > 64:
        await message.answer(msgs.max_length_error)
        return

    await state.update_data(name=text)
    await state.set_state(CreateTrip.description)
    await message.answer(
        msgs.ask_for_description, reply_markup=keyboards.skip_markup()
    )


@router.message(CreateTrip.description)
async def handle_trip_description(message: types.Message, state: FSMContext):
    text = message.text.strip()

    if text != msgs.skip:
        await state.update_data(description=text)

    data = await state.get_data()

    new_trip, status_code = api.API(message.from_user.id).create_trip(**data)

    await state.clear()

    if status_code == 201:
        await message.answer(msgs.trip_created)
        await trip_view(message, new_trip['id'])
    else:
        await message.answer(msgs.internal_error)


@router.callback_query(TripCallback.filter(F.action == 'route'))
async def handle_trip_route(call: types.CallbackQuery,
                            callback_data: TripCallback):
    trip_id = callback_data.id
    route_img_bytes, status_code = api.API(
        call.from_user.id
    ).get_route(trip_id)
    await call.answer()

    if status_code == 200:
        buttons = [
            (msgs.show_trip, TripCallback(action='show', id=trip_id))
        ]
        markup = keyboards.build_inline_markup(buttons)
        await call.message.edit_reply_markup(None)
        await call.message.answer_photo(
            types.BufferedInputFile(
                route_img_bytes, filename='route.jpg'
            ),
            caption=msgs.drive_by_car_time % 0,
            reply_markup=markup
        )
    elif status_code == 400 and route_img_bytes['detail'] == '2004':
        await call.message.answer(msgs.sad_2004_error)
    else:
        await call.answer(msgs.internal_error)
