from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
import asyncio
import os

from handlers import (registration, main_menu, trips, locations, profile,
                      default)
from utils.middlewares import FilterIdMiddleware

bot = Bot(
    token=os.getenv("TG_BOT_TOKEN"),
    default=DefaultBotProperties(parse_mode='HTML')
)

dp = Dispatcher()


async def main() -> None:
    dp.include_routers(
        default.router,
        registration.router,
        main_menu.router,
        trips.router,
        locations.router,
        profile.router,
    )

    if bool(os.getenv("DEBUG")) and (filter_id := os.getenv("DEV_TG_ID")):
        dp.message.middleware(FilterIdMiddleware(int(filter_id)))

    print("Bot was successfully initiated, starting polling...")

    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
