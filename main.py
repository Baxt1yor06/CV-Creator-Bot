import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher, F, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, BufferedInputFile, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from free_template import render_cv
from weasyprint import HTML
from os import getenv
from dotenv import load_dotenv


load_dotenv()
TOKEN = getenv("BOT_TOKEN")  # Railway dagi variable nomi
print("TOKEN:", TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

#  Tugmalar
start = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[[
            KeyboardButton(text="Yangi CV/Rezyume yaratish"),
]])

skip_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="⏭ O‘tkazib yuborish", callback_data="skip_links")]
    ]
)



#   O'zgaruvchilar
class UserStates(StatesGroup):
    # Hammasi
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


# Start funksiya
@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Salom! Men CV(Rezyume) yasab beradigan botman.", reply_markup=start)



@dp.message(F.text.lower() == "yangi cv/rezyume yaratish")
async def get_name(message: Message, state: FSMContext) -> None:
    await message.answer("Ism va Familiyangizni kiritng:", reply_markup=ReplyKeyboardRemove())
    await state.set_state(UserStates.user_full_name)

@dp.message(UserStates.user_full_name)
async def get_full_name(message: Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    await message.answer("Endi manzilingizni kiriting (shahar, tuman):")
    await state.set_state(UserStates.user_location)

@dp.message(UserStates.user_location)
async def get_location(message: Message, state: FSMContext):
    await state.update_data(location=message.text)
    await message.answer("Telefon raqamingizni yuboring:")
    await state.set_state(UserStates.user_phone_number)

@dp.message(UserStates.user_phone_number)
async def get_phone(message: Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await message.answer("Email yuboring:")
    await state.set_state(UserStates.user_email)

@dp.message(UserStates.user_email)
async def get_email(message: Message, state: FSMContext):
    await state.update_data(email=message.text)
    await message.answer("Sohangizni kiriting:")
    await state.set_state(UserStates.user_proffesion)



@dp.message(UserStates.user_proffesion)
async def get_proffesion(message: Message, state: FSMContext):
    await state.update_data(proffesion=message.text)
    await message.answer("🎓 Ta’lim tarixini kiriting. Qayerda o‘qigansiz?")
    await state.set_state(UserStates.edu_name)

# ===============================
# TA'LIM LOOP
# ===============================

@dp.message(UserStates.edu_name)
async def get_edu(message: Message, state: FSMContext):
    await state.update_data(current_edu={"place": message.text})
    await message.answer("Qaysi yillarda o‘qigansiz?")
    await state.set_state(UserStates.edu_years)

@dp.message(UserStates.edu_years)
async def edu_year(message: Message, state: FSMContext):
    data = await state.get_data()
    data["current_edu"]["years"] = message.text
    await state.update_data(data)
    await message.answer("Qaysi yo‘nalishda o‘qigansiz?")
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
            [KeyboardButton(text="Ha"), KeyboardButton(text="Yo‘q")]
        ],
        resize_keyboard=True
    )
    await state.set_state(UserStates.edu_again)
    await message.answer("Yana ta’lim qo‘shasizmi?", reply_markup=kb)


@dp.message(UserStates.edu_again)
async def edu_again(message: Message, state: FSMContext):
    if message.text.lower() == "ha":
        await message.answer("Qayerda o‘qigansiz?", reply_markup=ReplyKeyboardRemove())
        await state.set_state(UserStates.edu_name)
    else:
        await message.answer("Nimalarni bilasiz:", reply_markup=ReplyKeyboardRemove())
        await state.set_state(UserStates.user_skills)

@dp.message(UserStates.user_skills)
async def get_skills(message: Message, state: FSMContext):
    await state.update_data(
        skills=[s.strip() for s in message.text.split(",")]
    )
    await message.answer("Portfolio/GitHub uchun link kiritng (ixtiyoriy):", reply_markup=skip_kb)
    await state.set_state(UserStates.user_links)

@dp.message(F.data == "skip_links")
async def skip_links(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(links="")
    await callback.message.answer("Qaysi tillarni bilasiz:")
    await state.set_state(UserStates.user_language)
    await callback.answer()

@dp.message(UserStates.user_links)
async def get_links(message: Message, state: FSMContext):
    await state.update_data(links=message.text)
    await message.answer("Qaysi tillarni bilasiz:")
    await state.set_state(UserStates.user_language)

@dp.message(UserStates.user_language)
async def get_language(message: Message, state: FSMContext):
    await state.update_data(
        languages=[l.strip() for l in message.text.split(",")]
    )
    await message.answer("O'zingiz haqingizda ma'lumotlarni kiriting:")
    await state.set_state(UserStates.user_about)

@dp.message(UserStates.user_about)
async def get_about(message: Message, state: FSMContext):
    await state.update_data(about=message.text)
    await message.answer("Qayerda ishlaganingizni kiriting:")
    await state.set_state(UserStates.work_name)

# ===============================
# ISH LOOP
# ===============================

@dp.message(UserStates.work_name)
async def work_company(message: Message, state: FSMContext):
    await state.update_data(current_work={"company": message.text})
    await message.answer("Qaysi yillarda ishladingiz?")
    await state.set_state(UserStates.work_years)

@dp.message(UserStates.work_years)
async def work_years(message: Message, state: FSMContext):
    data = await state.get_data()
    data["current_work"]["years"] = message.text
    await state.update_data(data)
    await message.answer("Lavozimingiz?")
    await state.set_state(UserStates.work_field)

@dp.message(UserStates.work_field)
async def work_field(message: Message, state: FSMContext):
    data = await state.get_data()
    data["current_work"]["field"] = message.text
    await state.update_data(data)
    await message.answer("Batafsil nima ish qildingiz?")
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
            [KeyboardButton(text="Ha"), KeyboardButton(text="Yo‘q")]
        ],
        resize_keyboard=True
    )
    await state.set_state(UserStates.work_again)
    await message.answer("Yana ish joyi qo‘shasizmi?", reply_markup=kb)


@dp.message(UserStates.work_again)
async def work_again(message: types.Message, state: FSMContext):
    if message.text.lower() == "ha":
        await message.answer("Qayerda ishladingiz?", reply_markup=ReplyKeyboardRemove())
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

        await message.answer("Tayyorlanmoqda, iltimos kuting...")

        # 4. Hujjatni yuborish
        await message.answer_document(
            document=document,
            caption="Sizning professional CV-ingiz tayyor! ✨",
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