from aiogram import Bot
from aiogram.types import BotCommand


async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command="start",
            description="Начать"
        ),
        BotCommand(
            command="about",
            description="О нас"
        ),
        BotCommand(
            command="balance",
            description="Мой баланс"
        ),
        BotCommand(
            command="order",
            description="Заказать вещь"
        ),
        BotCommand(
            command="legit",
            description="Legit Check"
        ),
        BotCommand(
            command="find",
            description="Поиск айтема"
        ),
        BotCommand(
            command="cancel",
            description="Отменить действие"
        ),
    ]

    await bot.set_my_commands(commands)
