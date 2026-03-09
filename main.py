import asyncio
import logging
import sys
import re
from aiogram import Bot, Dispatcher, F, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, BufferedInputFile, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.fsm.context import FSMContext
from free_template import render_cv
from weasyprint import HTML
from os import getenv
from dotenv import load_dotenv
from aiogram.utils.i18n import I18n, FSMI18nMiddleware, gettext as _


load_dotenv()
TOKEN = getenv("BOT_TOKEN")  # Railway dagi variable nomi
print("TOKEN:", TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

i18n = I18n(path="locales", default_locale="uz", domain="messages")
i18n_middleware = FSMI18nMiddleware(i18n)
dp.update.middleware(i18n_middleware)

#  Tugmalar
start = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[[
            KeyboardButton(text=_("Yangi CV/Rezyume yaratish")),
]])

skip_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text=_("⏭ O‘tkazib yuborish"), callback_data="skip_links")]
    ]
)



#   O'zgaruvchilar
class UserStates(StatesGroup):
    # Hammasi
    user_start = State()
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
    pattern = r"^\+998\d{9}$"
    return re.match(pattern, phone)

def check_email(email: str):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email)

def check_year(text: str):
    pattern = r"^\d{4}\s-\s\d{4}$"
    return re.match(pattern, text)

# Start funksiya
@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer("Salom! Men CV(Rezyume) yasab beradigan botman.\nHello! I am a CV (Resume) creation bot.\nЗдравствуйте! Я — бот для создания резюме.", reply_markup=start)

# Команда /language для смены языка
@dp.message(Command("language"))
async def cmd_language(message: types.Message):
    keyboard = ReplyKeyboardBuilder()
    keyboard.add(KeyboardButton(text="English"), KeyboardButton(text="O'zbekcha"), KeyboardButton(text="Русский"),)
    await message.answer(_("Iltimos tilni tanlang: "), reply_markup=keyboard.as_markup(resize_keyboard=True))

# Обработка выбора языка
@dp.message(F.text.in_(["English", "Русский", "O'zbekcha"]))
async def set_language(message: types.Message, state: FSMContext):

    if message.text == "English":
        locale = "en"
    elif message.text == "Русский":
        locale = "ru"
    else:
        locale = "uz"

    await i18n_middleware.set_locale(state, locale)
    await message.answer(_("Til o'zgartirildi."), reply_markup=ReplyKeyboardRemove())



@dp.message(F.text.in_(["Yangi CV/Rezyume yaratish", "Create a new CV/Resume", "Создать новое резюме"]))
async def get_name(message: Message, state: FSMContext) -> None:
    await message.answer(_("Ism va Familiyangizni kiritng:"), reply_markup=ReplyKeyboardRemove())
    await state.set_state(UserStates.user_full_name)

@dp.message(UserStates.user_full_name)
async def get_full_name(message: Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    await message.answer(_("Endi manzilingizni kiriting (shahar, tuman):"))
    await state.set_state(UserStates.user_location)


@dp.message(UserStates.user_location)
async def get_location(message: Message, state: FSMContext):
    await state.update_data(location=message.text)
    await message.answer(_("Telefon raqamingizni yuboring:"))
    await state.set_state(UserStates.user_phone_number)



# @dp.message(UserStates.user_phone_number)
# async def get_phone(message: Message, state: FSMContext):
#     await state.update_data(phone=message.text)
#     await message.answer("Email yuboring:")
#     await state.set_state(UserStates.user_email)
@dp.message(UserStates.user_phone_number)
async def get_phone(message: Message, state: FSMContext):

    if not check_phone(message.text):
        await message.answer(_("❌ Telefon raqam noto‘g‘ri.\nMasalan: +998901234567"))
        return

    await state.update_data(phone=message.text)
    await message.answer(_("Email yuboring:"))
    await state.set_state(UserStates.user_email)

# @dp.message(UserStates.user_email)
# async def get_email(message: Message, state: FSMContext):
#     await state.update_data(email=message.text)
#     await message.answer("Sohangizni kiriting:")
#     await state.set_state(UserStates.user_proffesion)

@dp.message(UserStates.user_email)
async def get_email(message: Message, state: FSMContext):

    if not check_email(message.text):
        await message.answer(_("❌ Email noto‘g‘ri.\nMasalan: example@gmail.com"))
        return

    await state.update_data(email=message.text)
    await message.answer(_("Sohangizni kiriting:"))
    await state.set_state(UserStates.user_proffesion)



@dp.message(UserStates.user_proffesion)
async def get_proffesion(message: Message, state: FSMContext):
    await state.update_data(proffesion=message.text)
    await message.answer(_("🎓 Ta’lim tarixini kiriting. Qayerda o‘qigansiz?"))
    await state.set_state(UserStates.edu_name)

# ===============================
# TA'LIM LOOP
# ===============================

@dp.message(UserStates.edu_name)
async def get_edu(message: Message, state: FSMContext):
    await state.update_data(current_edu={"place": message.text})
    await message.answer(_("Qaysi yillarda o‘qigansiz(2020-2022)?"))
    await state.set_state(UserStates.edu_years)

# @dp.message(UserStates.edu_years)
# async def edu_year(message: Message, state: FSMContext):
#     data = await state.get_data()
#     data["current_edu"]["years"] = message.text
#     await state.update_data(data)
#     await message.answer("Qaysi yo‘nalishda o‘qigansiz?")
#     await state.set_state(UserStates.edu_field)
@dp.message(UserStates.edu_years)
async def edu_year(message: Message, state: FSMContext):

    if not check_year(message.text):
        await message.answer(_("❌ Format noto‘g‘ri.\nMasalan: 2021 - 2024"))
        return

    data = await state.get_data()
    data["current_edu"]["years"] = message.text
    await state.update_data(data)

    await message.answer(_("Qaysi yo‘nalishda o‘qigansiz?"))
    await state.set_state(UserStates.edu_field)

@dp.message(UserStates.edu_field)
async def edu_field(message: Message, state: FSMContext):
    data = await state.get_data()
    data["current_edu"]["field"] = message.text

    studies = data.get("education", [])
    studies.append(data["current_edu"])
    await state.update_data(education=studies)
    await state.update_data(current_edu=None)

    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=_("Ha")), KeyboardButton(text=_("Yo‘q"))]
        ],
        resize_keyboard=True
    )
    await state.set_state(UserStates.edu_again)
    await message.answer(_("Yana ta’lim qo‘shasizmi?"), reply_markup=kb)


@dp.message(UserStates.edu_again)
async def edu_again(message: Message, state: FSMContext):
    if message.text.lower() in ["ha", "yes", "да"]:
        await message.answer(_("Qayerda o‘qigansiz?"), reply_markup=ReplyKeyboardRemove())
        await state.set_state(UserStates.edu_name)
    else:
        await message.answer(_("Nimalarni bilasiz:"), reply_markup=ReplyKeyboardRemove())
        await state.set_state(UserStates.user_skills)

@dp.message(UserStates.user_skills)
async def get_skills(message: Message, state: FSMContext):
    await state.update_data(
        skills=[s.strip() for s in message.text.split(",")]
    )
    await message.answer(_("Portfolio/GitHub uchun link kiritng (ixtiyoriy):"), reply_markup=skip_kb)
    await state.set_state(UserStates.user_links)

@dp.callback_query(F.data == "skip_links")
async def skip_links(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(links="")
    await callback.message.answer(_("Qaysi tillarni bilasiz:"))
    await state.set_state(UserStates.user_language)
    await callback.answer()

@dp.message(UserStates.user_links)
async def get_links(message: Message, state: FSMContext):
    await state.update_data(links=message.text)
    await message.answer(_("Qaysi tillarni bilasiz:"))
    await state.set_state(UserStates.user_language)

@dp.message(UserStates.user_language)
async def get_language(message: Message, state: FSMContext):
    await state.update_data(
        languages=[l.strip() for l in message.text.split(",")]
    )
    await message.answer(_("O'zingiz haqingizda ma'lumotlarni kiriting:"))
    await state.set_state(UserStates.user_about)

@dp.message(UserStates.user_about)
async def get_about(message: Message, state: FSMContext):
    await state.update_data(about=message.text)
    await message.answer(_("Qayerda ishlaganingizni kiriting:"))
    await state.set_state(UserStates.work_name)

# ===============================
# ISH LOOP
# ===============================

@dp.message(UserStates.work_name)
async def work_company(message: Message, state: FSMContext):
    await state.update_data(current_work={"company": message.text})
    await message.answer(_("Qaysi yillarda ishladingiz?"))
    await state.set_state(UserStates.work_years)

# @dp.message(UserStates.work_years)
# async def work_years(message: Message, state: FSMContext):
#     data = await state.get_data()
#     data["current_work"]["years"] = message.text
#     await state.update_data(data)
#     await message.answer("Lavozimingiz?")
#     await state.set_state(UserStates.work_field)
@dp.message(UserStates.work_years)
async def work_years(message: Message, state: FSMContext):

    if not check_year(message.text):
        await message.answer(_("❌ Format noto‘g‘ri.\nMasalan: 2021 - 2024"))
        return

    data = await state.get_data()
    data["current_work"]["years"] = message.text
    await state.update_data(data)

    await message.answer(_("Lavozimingiz?"))
    await state.set_state(UserStates.work_field)

@dp.message(UserStates.work_field)
async def work_field(message: Message, state: FSMContext):
    data = await state.get_data()
    data["current_work"]["field"] = message.text
    await state.update_data(data)
    await message.answer(_("Batafsil nima ish qildingiz?"))
    await state.set_state(UserStates.work_more)

@dp.message(UserStates.work_more)
async def work_more(message: Message, state: FSMContext):
    data = await state.get_data()
    data["current_work"]["description"] = message.text
    works = data.get("work", [])
    works.append(data["current_work"])
    await state.update_data(work=works)
    await state.update_data(current_work=None)

    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=_("Ha")), KeyboardButton(text=_("Yo‘q"))]
        ],
        resize_keyboard=True
    )
    await state.set_state(UserStates.work_again)
    await message.answer(_("Yana ish joyi qo‘shasizmi?"), reply_markup=kb)


@dp.message(UserStates.work_again)
async def work_again(message: types.Message, state: FSMContext):
    if message.text.lower() in ["ha", "yes", "да"]:
        await message.answer(_("Qayerda ishladingiz?"), reply_markup=ReplyKeyboardRemove())
        await state.set_state(UserStates.work_name)
    else:
        # Ma'lumotlarni olish
        data = await state.get_data()

        # 1. Jinja2 bilan HTML render qilish (bu funksiyangiz tayyor deb hisoblaymiz)
        html_content = render_cv(data)

        # 2. HTML ni PDF (byte) ko'rinishida generatsiya qilish
        # WeasyPrint ishlatayotgan bo'lsangiz:
        pdf_bytes = HTML(string=html_content).write_pdf()

        # 3. BufferedInputFile orqali serverga saqlamasdan yuborish
        # aiogram 3.x da BytesIO ishlatish shart emas, to'g'ridan-to'g'ri bytelarni bersa bo'ladi
        document = BufferedInputFile(
            file=pdf_bytes,
            filename=f"{data.get('full_name', 'CV')}.pdf"
        )

        await message.answer(_("Tayyorlanmoqda, iltimos kuting..."))

        # 4. Hujjatni yuborish
        await message.answer_document(
            document=document,
            caption=_("Sizning professional CV-ingiz tayyor! ✨"),
            reply_markup=start
        )

        # Holatni tozalash
        await state.clear()







async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())