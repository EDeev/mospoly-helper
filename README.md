# МосПолиХелпер

**Русский** · [English](README.en.md)

[![CI](https://github.com/EDeev/mospoly-helper/actions/workflows/ci.yml/badge.svg)](https://github.com/EDeev/mospoly-helper/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/EDeev/mospoly-helper)](https://github.com/EDeev/mospoly-helper/releases)

Telegram-бот, который присылает видео-маршрут до нужной аудитории в корпусах Московского Политеха:
выбираешь кампус, пишешь номер кабинета — получаешь кружок с дорогой от входа на территорию или от входа
в корпус.

**Статус:** учебный командный проект (проектная практика, Московский Политех, группа 241-327, 2025),
завершён · бот [@MosPoly_Helperbot](https://t.me/MosPoly_Helperbot)

**Стек:** Python 3.10 · aiogram 3 · MoviePy 2 · FFmpeg · Docker

## Возможности

- Пять кампусов: Большая Семёновская, Павла Корчагина, Прянишникова, Михалковская, Автозаводская
- Маршрут от входа на территорию или от входа в корпус: ролик собирается из фрагментов «корпус → этаж →
  кабинет», ускоряется вдвое и кодируется под Telegram (H.264, 1500k)
- Готовые ролики кешируются, повторный запрос отдаётся сразу; `combine.py` собирает кеш заранее
- Проверка номера кабинета и подсказки, если формат не тот или кампус не совпадает

Видео сняты для корпусов на Прянишникова (76 кабинетов) и частично на Автозаводской; для остальных
кампусов бот отвечает, что маршрута пока нет, и предлагает написать на почту.

| Кампус | Формат кабинета | Пример |
|---|---|---|
| Прянишникова | пр[корпус][этаж][номер] | `пр2202а` |
| Автозаводская | ав[корпус][этаж][номер] | `ав2301` |
| Павла Корчагина | пк[корпус][этаж][номер] | `пк1201` |
| Михалковская | м[корпус][этаж][номер] | `м1205` |
| Большая Семёновская | [корпус][этаж]-[номер] | `а1-01` |

## Запуск

```bash
git clone https://github.com/EDeev/mospoly-helper.git && cd mospoly-helper
cp .env.example .env      # BOT_TOKEN от @BotFather
docker compose up -d
```

**Готовый образ** (видео внутри, кеш маршрутов строится сам):

```bash
docker run -d -e BOT_TOKEN=токен -v mospoly-cache:/app/src/data/cache -v mospoly-users:/app/src/data/users ghcr.io/edeev/mospoly-helper
```

(то же — `git.deev.su/edeev/mospoly-helper`).

Без Docker: Python 3.10+, FFmpeg, `pip install -r requirements.txt`, затем
`cd src/code && BOT_TOKEN=… python bot.py`. Подробнее — [QUICKSTART.md](QUICKSTART.md) и [DOCKER.md](DOCKER.md).

> [!NOTE]
> В репозитории около 220 роликов (исходники и кеш), поэтому он весит больше 500 МБ.

## Структура

```
src/code/       бот: handlers.py (команды и кнопки), scripts.py (маршруты и монтаж), combine.py (кеш)
src/videos/     исходные фрагменты: <кампус>/buildings, floors, offices
src/data/cache  собранные маршруты
site/           сайт проекта практики
reports/        отчёты участников и презентация
task/           задание практики
```

## Лицензия

Учебный проект (проектная практика, Московский Политех, 2025). Код открыт для изучения, отдельной
лицензии нет.

## Авторы

- **Деев Егор** — [GitHub](https://github.com/EDeev)
- **Сапрыкин Пётр** — [GitHub](https://github.com/PetrSaprykin)
- **Старков Руслан** — [GitHub](https://github.com/RayStar-k)

---

<div align="center">
  <sub>⭐ Если проект оказался полезным, поставьте звёздочку на GitHub!</sub>
  <p><sub>Сделано с ❤️ студентами Московского Политеха, группа 241-327</sub></p>
</div>
