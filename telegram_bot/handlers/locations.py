from aiogram import F, Router, types, html
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from utils import msgs, keyboards, api
from utils.callbacks import TripCallback

from .trips import trip_view

router = Router()


class AddLocations(StatesGroup):
    add_location = State()


@router.callback_query(TripCallback.filter(F.action == 'add_locations'))
async def handle_add_locations(call: types.CallbackQuery,
                               callback_data: TripCallback,
                               state: FSMContext):
    api_inst = api.API(call.from_user.id)
    trip, status_code = api_inst.get_trip(callback_data.id)

    if status_code == 200:
        await state.set_state(AddLocations.add_location)
        await state.update_data(api_inst=api_inst, trip=trip, num=0)
        await call.answer()
        await call.message.edit_text(html.bold(trip['name']))
        await call.message.answer(
            msgs.add_location_msg, reply_markup=keyboards.stop_markup()
        )
    else:
        await call.answer(msgs.internal_error)


@router.message(AddLocations.add_location)
async def handle_new_location_msg(message: types.Message, state: FSMContext):
    text = message.text.strip()
    data = await state.get_data()
    if text == msgs.stop:
        await state.clear()
        await message.answer(
            msgs.added_num_locations % data['num'],
            reply_markup=keyboards.CLEAR
        )
        await trip_view(message, data['trip']['id'])
        return

    spl = text.split('\n')
    if len(spl) != 2:
        await message.answer(msgs.wrong_add_location)
        return
    dates = spl[1].split('-')
    if len(dates) != 2:
        await message.answer(msgs.wrong_add_location)
        return

    new_location, status_code = data['api_inst'].add_location(
        query=spl[0],
        trip_id=data['trip']['id'],
        start_date=dates[0].strip(),
        end_date=dates[1].strip()
    )

    if status_code == 201:
        await state.update_data(num=data['num'] + 1)
        await message.answer(msgs.location_added % new_location['name'])
    elif status_code == 404:
        await message.answer(msgs.location_not_found)
    else:
        await message.answer(msgs.internal_error)


@router.callback_query(TripCallback.filter(F.action == 'edit_locations'))
async def handle_edit_locations(call: types.CallbackQuery,
                                callback_data: TripCallback,
                                state: FSMContext):
    trip, status_code = api.API(call.from_user.id).get_trip(callback_data.id)

    if status_code == 200:
        buttons = [
            (
                msgs.add_button,
                TripCallback(action='add_locations', id=trip['id'])
            ),
            (
                msgs.delete_some_button,
                TripCallback(action='delete_locations', id=trip['id'])
            ),
            keyboards.MENU_BUTTON,
        ]
        markup = keyboards.build_inline_markup(buttons)

        await call.answer()
        await call.message.edit_text(
            msgs.get_locations_msg(
                trip['name'], trip['locations'], msgs.choose_action
            ), reply_markup=markup
        )


class DeleteLocations(StatesGroup):
    delete_ids = State()


@router.callback_query(TripCallback.filter(F.action == 'delete_locations'))
async def handle_delete_locations(call: types.CallbackQuery,
                                  callback_data: TripCallback,
                                  state: FSMContext):
    api_inst = api.API(call.from_user.id)
    trip, status_code = api_inst.get_trip(callback_data.id)

    if status_code == 200:
        await call.answer()
        await state.set_state(DeleteLocations.delete_ids)
        numerated_ids = {
            index + 1: loc['id'] for index, loc in enumerate(trip['locations'])
        }
        await state.update_data(
            api_inst=api_inst, numerated_ids=numerated_ids, trip_id=trip['id']
        )
        await call.message.edit_text(
            msgs.get_locations_msg(
                trip['name'], trip['locations'], msgs.delete_locations_text
            )
        )


@router.message(DeleteLocations.delete_ids)
async def handle_delete_ids(message: types.Message, state: FSMContext):
    text = message.text.strip()
    if not text.isdigit():
        await message.answer(msgs.not_digits)
        return

    data = await state.get_data()
    api_inst = data['api_inst']

    successful = []
    werent_in_list = []

    for id in map(int, text.split()):
        location_id = data['numerated_ids'].get(id)
        if location_id:
            deleted, status_code = api_inst.delete_location(
                trip_id=data['trip_id'], location_id=location_id
            )
            if status_code == 200:
                successful.append(deleted)
        else:
            werent_in_list.append(id)

    await state.clear()
    await message.answer(
        msgs.deleted_locations_msg(successful, werent_in_list)
    )
    await trip_view(message, data['trip_id'])
