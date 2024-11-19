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
from src.Models.Client import Client

# Инициализируем роутер уровня модуля
router = Router()


@router.callback_query(F.data == "users_mode")
async def start_chinese_train_1(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(Status.Mode_users)
    
    def get_keyboard():
            buttons = [
                [types.InlineKeyboardButton(text="Показать всех пользователей", callback_data="show_users")],
                [types.InlineKeyboardButton(text="Показать клиентов пользователей", callback_data="showclients_users")],
                [
                    types.InlineKeyboardButton(text="Добавить клиента пользователю", callback_data="addclients_users")
                    # types.InlineKeyboardButton(text="Удалить клиента у пользователя", callback_data="remclients_users")
                ],
                [types.InlineKeyboardButton(text="Создать нового пользователя", callback_data="create_users")]
                # [types.InlineKeyboardButton(text="Обновить текущего пользователя", callback_data="update_users")],
                # [types.InlineKeyboardButton(text="Удалить пользователя", callback_data="delete_users")]
            ]
            keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
            return keyboard
    
    await callback.message.answer(f"Выберите необходимую функцию из предложенных ниже.", reply_markup=get_keyboard())



@router.callback_query(F.data == "show_users")
async def start_chinese_train_1(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(Status.Mode_users_show)

    users = User(callback.from_user.id).get_users()
    answer = ""
    for user in users:
        answer += f"<b>ID: {user[0]}</b> | Доступ: {user[3]}\nЛогин: {user[1]}\nИмя: {user[2]}\nСоздан: {user[5]}\n\n" 
    await callback.message.answer(f"<b>Список текущих пользователей системы:</b>\n{answer}")



@router.callback_query(F.data == "showclients_users")
async def start_chinese_train_1(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(Status.Mode_users_showclients)

    text = User().get_users_clients()

    await callback.message.answer(f"Вот список пользователей и их клиентов:\n{text}")





# @router.message(Status.Mode_users_create, F.text)
# async def get_message_base(message: types.Message, bot: Bot, state: FSMContext):
    # (message.from_user.username, message.chat.id)

    # hanzi = await irg_generate(message.from_user.username, message.chat.id)
    # await message.answer(f"{hanzi[0]} - <tg-spoiler>{hanzi[1]}</tg-spoiler> - {hanzi[2]}\n")
    # pass    
    

    
@router.callback_query(F.data == "addclients_users")
async def start_chinese_train_1(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(Status.Mode_users_addclient)
    await callback.message.answer(f"Введите ниже идентификатор пользователя и логин клиента, чтобы добавить клиента пользователю.\nПример:\n1192983 bestwindows_spb")

@router.message(Status.Mode_users_addclient, F.text)
async def get_message_base(message: types.Message, bot: Bot, state: FSMContext):
    # (message.from_user.username, message.chat.id)
    split_message = message.text.split(' ', maxsplit=1)

    try:
        if split_message[0] is None:
            await message.answer("Ошибка: переданы не все аргументы")
            return
        
        user = User(split_message[0]).get_current_user_info()
        client = Client(split_message[1]).get_current_client_info()

        request = User(user._id, client._login).add_client()
        user = User(message.chat.id).get_current_user_info()
        await message.answer(f"{request} {user}")

    except:
        await message.answer(
            "Ошибка: неправильный формат ввода. Попробуйте ещё раз:\n"
            "user_chat_id @tg_login name role"
        )
        return





    
@router.callback_query(F.data == "remclients_users")
async def start_chinese_train_1(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(Status.Mode_users_remclient)
    await callback.message.answer(f"Выберите необходимую функцию из предложенных ниже.")





    
@router.callback_query(F.data == "create_users")
async def start_chinese_train_1(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(Status.Mode_users_create)
    await callback.message.answer(f"Введите ниже данные пользователя, которого необходимо добавить. Данные следует вводить следующим образом:\nuser_chat_id @tg_login name role")

@router.message(Status.Mode_users_create, F.text)
async def get_message_base(message: types.Message, bot: Bot, state: FSMContext):
    # (message.from_user.username, message.chat.id)
    split_message = message.text.split(' ', maxsplit=3)

    try:
        if split_message[0] is None:
            await message.answer("Ошибка: переданы не все аргументы")
            return
        request = User(split_message[0],split_message[1],split_message[2],split_message[3]).create_user()
        await message.answer(request)

    except:
        await message.answer(
            "Ошибка: неправильный формат ввода. Попробуйте ещё раз:\n"
            "user_chat_id @tg_login name role"
        )
        return
    


    
@router.callback_query(F.data == "update_users")
async def start_chinese_train_1(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(Status.Mode_users_update)
    await callback.message.answer(f"Выберите необходимую функцию из предложенных ниже.")

    
@router.callback_query(F.data == "delete_users")
async def start_chinese_train_1(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(Status.Mode_users_delete)
    await callback.message.answer(f"Выберите необходимую функцию из предложенных ниже.")