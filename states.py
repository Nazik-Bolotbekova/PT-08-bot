from aiogram.fsm.state import StatesGroup,State



class Questionnairre(StatesGroup):
    gender = State()
    age = State()
    job = State()

class Order(StatesGroup):
    product = State()
    color = State()
    amount = State()
    address = State()
    payment = State()