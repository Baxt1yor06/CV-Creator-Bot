from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from utilits import i18n_middleware
from keyboard import *
from aiogram.utils.i18n import gettext as _


router = Router()



@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    data = await state.get_data()
    locale = data.get("locale", "uz")
    await state.clear()
    await state.update_data(locale=locale)
    await i18n_middleware.set_locale(state, locale)
    await message.answer(
        "Salom! Men CV(Rezyume) yasab beradigan botman.\n"
        "Hello! I am a CV (Resume) creation bot.\n"
        "Здравствуйте! Я — бот для создания резюме.",
        reply_markup=get_language_kb()
    )


@router.message(Command("language"))
async def cmd_language(message: Message):
    await message.answer(_("Iltimos tilni tanlang: "), reply_markup=get_language_kb())


# ===============================
# TIL TANLASH
# ===============================

@router.message(F.text.in_(["English", "Русский", "O'zbekcha"]))
async def set_language(message:  Message, state: FSMContext):
    if message.text == "English":
        locale = "en"
    elif message.text == "Русский":
        locale = "ru"
    else:
        locale = "uz"

    await i18n_middleware.set_locale(state, locale)
    await state.update_data(locale=locale)
    await message.answer(_("Til o'zgartirildi."), reply_markup=get_start_kb())