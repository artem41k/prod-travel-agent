from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware, types


class FilterIdMiddleware(BaseMiddleware):
    def __init__(self, filter_id: int) -> None:
        self.filter_id = filter_id

    async def __call__(
        self,
        handler: Callable[[types.Message, Dict[str, Any]], Awaitable[Any]],
        event: types.Message,
        data: Dict[str, Any]
    ) -> Any:
        if event.from_user.id == self.filter_id:
            return await handler(event, data)
