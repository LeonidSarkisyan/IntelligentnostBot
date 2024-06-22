import logging
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from src.middlewares.limit import RateLimitMiddleware

from src.config import BOT_TOKEN

from src.handlers import basic, about, find, balance
from src.handlers.legit import client as legit_client, moderator as legit_moderator
from src.handlers.order import client as order_client, moderator as order_moderator

from src.utils.commands import set_commands
from src.database import get_connect_with_database
from src.repositories.users import user_repository
from src.repositories.finds import find_repository
from src.repositories.legit import legit_repository
from src.repositories.order import order_repository


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
    )

    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    await set_commands(bot)

    dp = Dispatcher()

    dp.message.middleware.register(RateLimitMiddleware(60, 60))
    dp.callback_query.middleware.register(RateLimitMiddleware(60, 60))

    routers = [
        basic.router, balance.router, about.router, find.router, legit_client.router, legit_moderator.router,
        order_client.router, order_moderator.router
    ]

    for r in routers:
        dp.include_router(r)

    db = await get_connect_with_database()

    repositories = [user_repository, find_repository, legit_repository, order_repository]

    for r in repositories:
        await r.connect(db)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
