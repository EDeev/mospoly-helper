import asyncio, logging

from init import *
from handlers import router


async def main() -> None:
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)

    await setup_bot_commands()
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    try: asyncio.run(main())
    except KeyboardInterrupt: pass
