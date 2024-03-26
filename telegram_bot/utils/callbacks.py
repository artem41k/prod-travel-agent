from aiogram.filters.callback_data import CallbackData
from typing import Optional


class TripCallback(CallbackData, prefix='trips'):
    action: str
    field: Optional[str] = None
    id: Optional[int] = None
    name: Optional[str] = None
    confirm: Optional[str] = None


class ProfileCallback(CallbackData, prefix='profile'):
    action: str
    field: Optional[str] = None


class MenuCallback(CallbackData, prefix='menu'):
    pass
