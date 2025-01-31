import asyncio
import os

from aiogram.exceptions import TelegramBadRequest
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage

import elements

# Объект бота
bot = Bot(token="7667989932:AAHl42T6fGeTt4h0Ut9QFHpOYQ4aMH0_VLo")

# Диспетчер с хранилищем состояний
dp = Dispatcher(storage=MemoryStorage())


# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await message.answer("Привет! Я помогу подобрать букет. Начнем с выбора цветовой палитры.")
    await elements.ask_color(message, state)


@dp.message()
async def restart(message: types.Message, state: FSMContext):
    await message.answer("Какого цвета вы хотите цветочную композицию?")
    await elements.ask_color(message, state)


# Хэндлер для обработки выбора цветовой палитры
@dp.callback_query(lambda c: c.data and c.data.startswith("color_"))
async def handle_color(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    color = callback.data.split("_")[1]
    
    try:
        await bot.delete_message(user_id, callback.message.message_id)
    except TelegramBadRequest as e:
        if "message to delete not found" in str(e).lower():
            print(f"Пользователь с id {user_id} нажал два раза на одну и ту же inline кнопку")
        else:
            print(f"Произошла другая ошибка: {e}")

    await state.update_data(color=color)
    await elements.ask_budget(callback.message, state)
    await callback.answer()


# Хэндлер для обработки выбора бюджета
@dp.callback_query(lambda c: c.data and c.data.startswith("budget_"))
async def handle_budget(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    budget = callback.data.split("_")[1]
    try:
        await bot.delete_message(user_id, callback.message.message_id)
    except TelegramBadRequest as e:
        if "message to delete not found" in str(e).lower():
            print(f"Пользователь с id {user_id} нажал два раза на одну и ту же inline кнопку")
        else:
            print(f"Произошла другая ошибка: {e}")

    await state.update_data(budget=budget)
    await elements.ask_occasion(callback.message, state)
    await callback.answer()


# Функция для поиска фотографии
def find_photo(base_dir, color, occasion, budget):
    folder_path = os.path.join(base_dir, color, occasion, budget)
    if not os.path.exists(folder_path):
        return None

    photos = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith(('.jpg', '.png', '.jpeg'))]
    if not photos:
        return None

    return photos


# Хэндлер для обработки выбора повода
@dp.callback_query(lambda c: c.data and c.data.startswith("occasion_"))
async def handle_occasion(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    occasion = callback.data.split("_")[1]

    try:
        await bot.delete_message(user_id, callback.message.message_id)
    except TelegramBadRequest as e:
        if "message to delete not found" in str(e).lower():
            print(f"Пользователь с id {user_id} нажал два раза на одну и ту же inline кнопку")
        else:
            print(f"Произошла другая ошибка: {e}")

    await state.update_data(occasion=occasion)

    data = await state.get_data()
    color = data.get("color")
    budget = data.get("budget")

    base_dir = "каталог букетов"
    photo_path = find_photo(base_dir, color, occasion, budget)

    print(photo_path)

    if photo_path:
        for photo in photo_path:
            await bot.send_photo(user_id, photo=types.FSInputFile(photo),
                                 reply_markup=elements.get_restart_button())
        await bot.send_message(user_id,
                               "Если вы хотите заново подобрать подходящий Вам букет, воспользуйтесь "
                               "командой /start или готовой панелью",
                               reply_markup=elements.get_restart_button()
                               )
    else:
        await bot.send_message(
            chat_id=user_id,
            text="К сожалению, не удалось найти подходящую фотографию. Попробуйте выбрать другой вариант.",
        )


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    print("Бот запущен")
    asyncio.run(main())


