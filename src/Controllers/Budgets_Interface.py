from aiogram import Bot, types
from aiogram import F # магические функции - позволяют вытаскивать всю нужную инфу с минимумом кода

from aiogram.filters.command import Command, CommandObject, CommandStart # Позволяет ловить команды в обработчик по схеме Command('команда')
from aiogram.types import Message,MessageEntity,FSInputFile, URLInputFile, BufferedInputFile, InputTextMessageContent, InlineQueryResultArticle # Работа с файлами
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from aiogram.utils.keyboard import ReplyKeyboardBuilder # Подстрочные кнопки
from aiogram.utils.keyboard import InlineKeyboardBuilder # Инлайновые кнопки

from aiogram import Router
from src.Models.Status import Status


# Инициализируем роутер уровня модуля
router = Router()




# ВЫБОР МОДА ПРИЛОЖЕНИЯ

# @router.callback_query(F.data == "set_budgets")
# async def start_chinese_train_1(callback: types.CallbackQuery, state: FSMContext):
#     await state.set_state(Status.Mode_budgets)

#     def get_keyboard():
#             buttons = [
#                 [types.InlineKeyboardButton(text="Показать план на текущую неделю", callback_data="gg")],
#                 [types.InlineKeyboardButton(text="Показать планы за последние несколько недель", callback_data="gg")],
#                 [types.InlineKeyboardButton(text="Установить новый план на неделю", callback_data="gg")],
#             ]
#             keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
#             return keyboard

#     await callback.message.answer(f"Выберите что хотите сделать с планом", reply_markup=get_keyboard())

# @router.callback_query(F.data == "set_clients")
# async def start_chinese_train_1(callback: types.CallbackQuery, state: FSMContext):
#     await state.set_state(Status.Mode_clients)
    
#     def get_keyboard():
#             buttons = [
#                 [types.InlineKeyboardButton(text="пупс", callback_data="gg")],
#                 [types.InlineKeyboardButton(text="пупс", callback_data="gg")],
#                 [types.InlineKeyboardButton(text="пупс", callback_data="gg")],
#             ]
#             keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
#             return keyboard
#     await callback.message.answer(f"Выберите, что хотите сделать с клиентами", reply_markup=get_keyboard())
