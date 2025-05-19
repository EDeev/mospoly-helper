from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.bot import DefaultBotProperties
from aiogram.types import BotCommand, BotCommandScopeDefault
from aiogram.methods import SetMyCommands

import config

# Структурированное определение команд для меню
async def setup_bot_commands():
    commands = [
        BotCommand(command="help", description="Получить помощь"),
        BotCommand(command="route", description="Построить маршрут")
    ]

    await bot(SetMyCommands(
        commands=commands,
        scope=BotCommandScopeDefault()
    ))

bot = Bot(token=config.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())
