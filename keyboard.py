from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.i18n import gettext as _


def get_start_kb():
    return ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[[
        KeyboardButton(text=_("Yangi CV/Rezyume yaratish")),
    ]])

def get_skip_kb():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=_("⏭ O'tkazib yuborish"), callback_data="skip_links")]
        ]
    )

def get_language_kb():
    keyboard = ReplyKeyboardBuilder()
    keyboard.add(KeyboardButton(text="English"), KeyboardButton(text="O'zbekcha"), KeyboardButton(text="Русский"))
    return keyboard.as_markup(resize_keyboard=True)

def get_yes_no_kb():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=_("Ha")), KeyboardButton(text=_("Yo'q"))]],
        resize_keyboard=True
    )