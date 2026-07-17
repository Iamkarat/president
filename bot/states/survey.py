from aiogram.fsm.state import State, StatesGroup


class SurveyForm(StatesGroup):
    name = State()
    age = State()
    city = State()
    height = State()
    experience = State()
    has_photos = State()
    photos = State()
    social = State()
    motivation = State()
