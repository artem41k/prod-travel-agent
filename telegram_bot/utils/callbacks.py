from aiogram.filters.callback_data import CallbackData
from typing import Optional


class TripCallback(CallbackData, prefix='trips'):
    action: str
    id: Optional[int] = None


class ProfileCallback(CallbackData, prefix='profile'):
    action: str
    field: Optional[str] = None


class MenuCallback(CallbackData, prefix='menu'):
    pass
