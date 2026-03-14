from aiogram.fsm.state import State, StatesGroup
import re



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


