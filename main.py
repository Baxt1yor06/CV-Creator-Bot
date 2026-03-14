import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from os import getenv
from dotenv import load_dotenv
from messages import common, quiz
import utilits



load_dotenv()
TOKEN = getenv("BOT_TOKEN")
print("TOKEN:", TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)







# ===============================
# O'ZGARUVCHILAR
# ===============================




async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )


# ===============================
# MAIN
# ===============================


if __name__ == '__main__':
    asyncio.run(main())

async def main() -> None:
    dp.include_router(common.router)
    dp.include_router(quiz.router)
    dp.include_router(utilits.router)
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())