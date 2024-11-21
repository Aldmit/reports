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
from src.Models.User import User


# Инициализируем роутер уровня модуля
router = Router()



@router.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await state.set_state(Status.Mode_ON)

    await message.answer(f"Добро пожаловать в Adwin Reports Bot. Ваш пользовательский идентификатор: {message.chat.id}")

    try:
        user = User(message.chat.id).get_current_user_info()
        if int(user._id) != message.chat.id:
            await message.answer("Для использования сервиса необходимо запросить регистрацию у администратора.")
            return
    except:
        await message.answer("Для использования сервиса необходимо запросить регистрацию у администратора.")
        return
    
    def get_keyboard():
            buttons = [
                # [types.InlineKeyboardButton(text="Работа с планами", callback_data="budgets_mode")],
                [types.InlineKeyboardButton(text="Работа с клиентами", callback_data="clients_mode")],
                [types.InlineKeyboardButton(text="Работа с пользователями", callback_data="users_mode")],
                [types.InlineKeyboardButton(text="Получить статистику", callback_data="reports_mode")],
            ]
            keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
            return keyboard
    await message.answer(f"Выберите что нужно сделать", reply_markup=get_keyboard())


    



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
