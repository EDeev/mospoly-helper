from aiogram import types, F, Router
from aiogram.types import (Message, InlineQuery, InlineQueryResultArticle, InputTextMessageContent, ChosenInlineResult,
                           ContentType, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, FSInputFile,
                           InputMediaPhoto, InlineQueryResultPhoto)
from aiogram.filters import Command, CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder

from init import *
from scripts import *

router = Router()


@router.message(CommandStart())
async def start_handler(msg: Message) -> None:
    await msg.answer("Привет мир!")


@router.message(Command("help"))
async def help_handler(msg: Message) -> None:
    text = "<b>Текст</b>\n\n"

    text += "<b>/dates</b> - Текст\n\n"
    text += "<b>/picture</b> - Текст\n\n"
    text += "<b>/gallery</b> - Текст"

    await msg.answer(text)
