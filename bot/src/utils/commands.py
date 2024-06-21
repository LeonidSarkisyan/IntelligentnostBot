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
            description="Узнать свой баланс"
        ),
        BotCommand(
            command="find",
            description="Найти вещь"
        ),
        BotCommand(
            command="cancel",
            description="Отменить действие"
        ),
    ]

    await bot.set_my_commands(commands)
