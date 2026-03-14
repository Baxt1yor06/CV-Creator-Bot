from aiogram.fsm.state import State, StatesGroup
import re
from aiogram import Router
from aiogram.utils.i18n import I18n, FSMI18nMiddleware
from aiogram.fsm.context import FSMContext
from aiogram.types import TelegramObject
from aiogram import BaseMiddleware
from typing import Callable, Dict, Any, Awaitable

router = Router()

class UserStates(StatesGroup):
    user_full_name = State()
    user_location = State()
    user_phone_number = State()
    user_email = State()
    user_proffesion = State()
    user_skills = State()
    user_links = State()
    user_language = State()
    user_about = State()
    # Ish loop uchun
    work_name = State()
    work_years = State()
    work_field = State()
    work_more = State()
    work_again = State()
    # Ta'lim loop uchun
    edu_name = State()
    edu_years = State()
    edu_field = State()
    edu_again = State()


def check_phone(phone: str):
    return re.match(r"^\+998\d{9}$", phone)

def check_email(email: str):
    return re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email)

def check_year(text: str):
    return re.match(r"^\d{4}\s-\s\d{4}$", text)


i18n = I18n(path="locales", default_locale="uz", domain="messages")
i18n_middleware = FSMI18nMiddleware(i18n)
router.update.middleware(i18n_middleware)


# ===============================
# LOCALE RESTORE MIDDLEWARE
# ===============================

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

router.update.middleware(LocaleRestoreMiddleware())