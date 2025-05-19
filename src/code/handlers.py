from aiogram import F, Router
from aiogram.types import (Message, ContentType, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, FSInputFile)
from aiogram.filters import Command, CommandStart

from scripts import *
from database import *

router = Router()


@router.message(CommandStart())
async def start_handler(msg: Message) -> None:
    await msg.answer("Здравствуйте! Этот бот поможет вам добраться до кабинета в структуре корпусов Московского "
                     "Политехнического Университета. Для начала работы просто пропишите команду <b>/route</b>")


@router.message(Command("help"))
async def help_handler(msg: Message) -> None:
    text = "<b>Напомню, что за команды у нас тут есть)</b>\n\n"

    text += "<b>/help</b> - Команда помощи, выведет все доступные команды\n\n"
    text += "<b>/route</b> - Команда выводит маршрут до введённого кабинета"

    await msg.answer(text)


@router.message(Command("route"))
async def route_handler(msg: Message) -> None:
    buttons = [[InlineKeyboardButton(text=f"На Большой Семёновской", callback_data="edu:bs")],
               [InlineKeyboardButton(text=f"На Павла Корчагина", callback_data="edu:pk")],
               [InlineKeyboardButton(text=f"На Прянишкова", callback_data="edu:pr"),
                InlineKeyboardButton(text=f"На Михалковской", callback_data="edu:mi")],
               [InlineKeyboardButton(text=f"На Автозаводской", callback_data="edu:av")]]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    await msg.answer(text="Выберите корпус на котором вы хотите проложить маршрут:", reply_markup=keyboard)


@router.callback_query(F.data.startswith("edu:"))
async def route_button(call: CallbackQuery) -> None:
    action = call.data.split(":")[1]

    user_dict = dict()
    user_dict[action] = []

    JsonTools(call.from_user.id).save_json(user_dict)

    await call.message.edit_text("Укажите до какого кабинет вам необходимо добраться "
                                 "(обязательно напишите кабинет в точности как указано в личном кабинет):")

@router.message(F.content_type == ContentType.TEXT)
async def add_cabinet(msg: Message) -> None:
    cab = msg.text.lower()

    jsn = JsonTools(msg.from_user.id)
    user_dict = jsn.read_json()
    edu_keys = list(user_dict.keys())

    if ((cab[0] == "м" and len(cab) == 5 and "mi" == edu_keys[0]) or
            (cab[:2] == "ав" and len(cab) == 6 and "av" == edu_keys[0]) or
            (cab[:2] == "пк" and len(cab) == 6 and "pk" == edu_keys[0]) or
            (cab[:2] == "пр" and len(cab) == 6 and "pr" == edu_keys[0]) or
            (cab[0] in ["а", "б", "в", "н", "нд"] and "bs" == edu_keys[0])):
        lst_routes = get_routes(edu_keys[0], cab)

        if lst_routes:
            user_dict[edu_keys[0]] = lst_routes
            jsn.save_json(user_dict)

            buttons = [[InlineKeyboardButton(text=f"От входа на территорию", callback_data="route:build")],
                       [InlineKeyboardButton(text=f"От входа в корпус", callback_data="route:floor")]]
            keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

            await msg.answer("Кабинет успешно получен, обрабатываем путь! Откуда вам проложить маршрут:", reply_markup=keyboard)
        else:
            await msg.answer("Обрыв программы по неизвестной причине!")
    else:
        await msg.answer("Вы скинули не кабинет! Я же вижу)")


@router.callback_query(F.data.startswith("route:"))
async def var_button(call: CallbackQuery) -> None:
    action = call.data.split(":")[1]

    jsn = JsonTools(call.from_user.id)
    user_dict = jsn.read_json()
    edu_keys = list(user_dict.keys())
    lst_routes = user_dict[edu_keys[0]]

    msg = await call.message.answer("1. Получение видео...")
    path = ""

    if action == "build":
        if os.path.exists(f"../data/cache/{lst_routes[-1][21:].replace('.mp4', '-all.mp4')}"):
            path = f"../data/cache/{lst_routes[-1][21:].replace('.mp4', '-all.mp4')}"
        else:
            path = make_full_clip(lst_routes)
            if not path:
                await msg.edit_text("Данного маршрута в нашей базе пока нет, извините за неудобство, можете написать "
                                    "желаемые маршруты на почту <a href='mailto:support@new-devs.ru' >support@new-devs.ru</a>")
                return 0
    elif action == "floor":
        if os.path.exists(f"../data/cache/{lst_routes[-1][21:].replace('.mp4', '-small.mp4')}"):
            path = f"../data/cache/{lst_routes[-1][21:].replace('.mp4', '-small.mp4')}"
        else:
            path = make_full_clip(lst_routes[1:])
            if not path:
                await msg.edit_text("Данного маршрута в нашей базе пока нет, извините за неудобство, можете написать "
                                    "желаемые маршруты на почту <a href='mailto:support@new-devs.ru' >support@new-devs.ru</a>")
                return 0

    msg_finally = await msg.edit_text("2. Видео готово!")

    await msg.answer_video_note(video_note=FSInputFile(path))
    await msg_finally.delete()
