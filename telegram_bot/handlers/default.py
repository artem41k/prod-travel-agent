from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from utils import msgs, keyboards

router = Router()


@router.callback_query(F.data == 'none')
async def handle_none(call: types.CallbackQuery):
    await call.answer()


@router.message(Command('cancel'))
async def handle_cancel(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(
        msgs.operation_cancelled,
        reply_markup=keyboards.CLEAR
    )
