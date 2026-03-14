from typing import Callable, Dict, Any, Awaitable
from aiogram import Bot, Dispatcher, BaseMiddleware
from aiogram.types import TelegramObject
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from os import getenv
from dotenv import load_dotenv
from aiogram.utils.i18n import I18n, FSMI18nMiddleware


load_dotenv()
TOKEN = getenv("BOT_TOKEN")
print("TOKEN:", TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)


i18n = I18n(path="locales", default_locale="uz", domain="messages")
i18n_middleware = FSMI18nMiddleware(i18n)
dp.update.middleware(i18n_middleware)
class LocaleRestoreMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        state: FSMContext = data.get("state")
        if state:
            state_data = await state.get_data()
            locale = state_data.get("locale", "uz")
            await i18n_middleware.set_locale(state, locale)
        return await handler(event, data)

dp.update.middleware(LocaleRestoreMiddleware())





