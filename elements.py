from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

from state import BouquetOrder


# Функция для выбора цветовой палитры
async def ask_color(message: types.Message, state: FSMContext):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Красный", callback_data="color_red")],
        [InlineKeyboardButton(text="Голубой", callback_data="color_blue")],
        [InlineKeyboardButton(text="Желтый", callback_data="color_yellow")],
        [InlineKeyboardButton(text="Оранжевый", callback_data="color_orange")],
        [InlineKeyboardButton(text="Розовый", callback_data="color_pink")],
        [InlineKeyboardButton(text="Белый", callback_data="color_white")]
    ])
    await message.answer("Выберите цветовую палитру:", reply_markup=keyboard)
    await state.set_state(BouquetOrder.color)


# Функция для выбора получателя
async def ask_recipient(message: types.Message, state: FSMContext):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Женщина", callback_data="recipient_woman")],
        [InlineKeyboardButton(text="Мужчина", callback_data="recipient_man")],
        [InlineKeyboardButton(text="Ребенок", callback_data="recipient_child")],
    ])
    await message.answer("Для кого предназначен букет?", reply_markup=keyboard)
    await state.set_state(BouquetOrder.recipient)


# Функция для выбора бюджета
async def ask_budget(message: types.Message, state: FSMContext):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="До 3000 ₽", callback_data="budget_3000")],
        [InlineKeyboardButton(text="3000-5000 ₽", callback_data="budget_5000")],
        [InlineKeyboardButton(text="Более 5000 ₽", callback_data="budget_5000+")],
    ])
    await message.answer("Выберите ваш бюджет:", reply_markup=keyboard)
    await state.set_state(BouquetOrder.budget)


# Функция для выбора повода
async def ask_occasion(message: types.Message, state: FSMContext):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="День рождения", callback_data="occasion_birthday")],
        [InlineKeyboardButton(text="8 марта", callback_data="occasion_womenday")],
        [InlineKeyboardButton(text="День знаний", callback_data="occasion_teacherday")],
        [InlineKeyboardButton(text="Просто так", callback_data="occasion_justbecause")],
    ])
    await message.answer("Выберите повод:", reply_markup=keyboard)
    await state.set_state(BouquetOrder.occasion)


def get_restart_button():
    button = KeyboardButton(text='Запустить подборку заново')

    keyboard = ReplyKeyboardMarkup(keyboard=[[button]], resize_keyboard=True)

    return keyboard
