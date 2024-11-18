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

from src.Services import Service_yd
import numpy as np
from pandas import Series,DataFrame
import pandas as pd

from datetime import datetime, timedelta


# Инициализируем роутер уровня модуля
router = Router()



@router.callback_query(F.data == "all_stats1111")
async def start_chinese_train_1(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(Status.Mode_reports)

    clients = [
        "avrorakuhni-spb",
        "dinamikadvizhenia",
        "g-geoservis",
        "happykitchen-ru",
        "happykitchen-spb",
        "kuhni-mf-kitchen-msk",
        "kuhni-mf-kitchen-spb",
        "kuhni-mf-msk",
        "kuhni-mf-spb",
        "kuhnirubika-ru",
        "kuhnirubika-ru-spb",
        "kuhni-sinterio",
        "kuhzavod-ru",
        "kuhzavod-ru-shkafi",
        "kuhzavod-spb-kuhni",
        "logistikz2020",
        "milismebel",
        "milismebel-spb",
        "pmfb2b",
        "profprioritetadwin",
        "prostyeformy",
        "prostyeformy-msk",
        "renckuhni",
        "sdfabrika-spb",
        "sinteriospb2",
        "skatetownmoscow",
        "skatetownspb",
        "tehnospbservis",
        "vmeste-uytno-msk",
        "vmeste-uytno-ru",
        "wowkitchenmsk",
        "wowkitchen-ru2016",
        "zabota-travel-adwin"
    ]

    # data_list = list()
    
    for name in clients:
        Service_yd.get_report(name)
    
    await callback.message.answer(f"Статистика за месяц загружена в базу.")



@router.callback_query(F.data == "yesterday")
async def start_chinese_train_1(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(Status.Mode_reports)
     
    def get_keyboard():
            buttons = [
                [types.InlineKeyboardButton(text="Аврора СПБ", callback_data="0")],
                [types.InlineKeyboardButton(text="ДинамикаДвижения", callback_data="1")],
                [types.InlineKeyboardButton(text="Геосервис", callback_data="2")],
            ]
            keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
            return keyboard
    
    await callback.message.answer(f"Выберите клиента по которому требуется показать данные.\n Вам доступны следующие клиенты:", reply_markup=get_keyboard())


@router.callback_query(F.data == "0")
async def start_chinese_train_1(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(Status.Mode_reports)
     
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    df = Service_yd.get_report('avrorakuhni-spb', 1)
    x = df.loc[[yesterday],['Impressions', 'Clicks', 'Cost']]

    view = int(x.iloc[0,0])
    click = int(x.iloc[0,1])
    cost =x.iloc[0,2]
    cpc = cost/click

    await callback.message.answer(f"Данные по клиенту 'Аврора СПБ' на {yesterday}:\nПросмотры: {view} \nКлики: {click} \nРасход: {cost} \nСРС: {cpc}")


@router.callback_query(F.data == "1")
async def start_chinese_train_1(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(Status.Mode_reports)
    
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    df = Service_yd.get_report('dinamikadvizhenia', 1)
    x = df.loc[[yesterday],['Impressions', 'Clicks', 'Cost']]

    view = int(x.iloc[0,0])
    click = int(x.iloc[0,1])
    cost =x.iloc[0,2]
    cpc = cost/click

    await callback.message.answer(f"Данные по клиенту 'ДинамикаДвижения' на {yesterday}:\nПросмотры: {view} \nКлики: {click} \nРасход: {cost} \nСРС: {cpc}")


@router.callback_query(F.data == "2")
async def start_chinese_train_1(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(Status.Mode_reports)
    
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    df = Service_yd.get_report('g-geoservis', 1)
    x = df.loc[[yesterday],['Impressions', 'Clicks', 'Cost']]

    view = int(x.iloc[0,0])
    click = int(x.iloc[0,1])
    cost =x.iloc[0,2]
    cpc = cost/click
     
    await callback.message.answer(f"Данные по клиенту 'Геосервис' на {yesterday}:\nПросмотры: {view} \nКлики: {click} \nРасход: {cost} \nСРС: {cpc}")


    # clients = [
    #     "avrorakuhni-spb",
    #     "dinamikadvizhenia",
    #     "g-geoservis"
    # ]

    # df_list = list()
    
    # for name in clients:
    #     df_list.append(Service_yd.get_report(name, 1))
    
    # df = df_list[0]


    # yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

    # x = df.loc[[yesterday],['Impressions', 'Clicks', 'Cost']]

    # view = int(x.iloc[0,0])
    # click = int(x.iloc[0,1])
    # cost =x.iloc[0,2]
    # cpc = cost/click


    # print(f"Просмотры: {view} \nКлики: {click} \nРасход: {cost} \nСРС: {cpc}")


    # x = df.loc[df['Date'] == '24-10-11']['Clicks'].values[0]

    # print(x)
    
    # await callback.message.answer(f"Статистика за месяц загружена в базу.")
