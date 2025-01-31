# Определение состояний
from aiogram.fsm.state import StatesGroup, State


class BouquetOrder(StatesGroup):
    color = State()
    budget = State()
    occasion = State()
    review = State()
