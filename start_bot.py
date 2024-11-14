import asyncio
import logging

from aiogram import Bot, Dispatcher
from config import Config, load_config

from src import *

# Запуск процесса поллинга новых апдейтов
async def main():

    # turn_on_logging()
    config: Config = load_config()
    BOT_TOKEN: str = config.bot.token

    # Объект бота
    bot = Bot(BOT_TOKEN, parse_mode="HTML")
    # Диспетчер
    dp = Dispatcher()

    async def start_bot(bot: Bot):
        print("\n\n🟢 Бот запущен\n\n\n")
    async def stop_bot(bot: Bot):
        print("\n\n🔴 Бот остановлен\n\n\n")

    dp.startup.register(start_bot)  # регистрируем в диспетчере функцию по запуску
    dp.shutdown.register(stop_bot)  # регистрируем в диспетчере функцию по остановке

    Database().create_tables()

    dp.include_router(MainInterface.router)
    dp.include_router(BudgetsInterface.router)
    dp.include_router(ClientsInterface.router)
    dp.include_router(StatisticsInterface.router)
    dp.include_router(UsersInterface.router)


    await dp.start_polling(bot)

    
    def turn_on_logging():    
        # Включаем логирование, чтобы не пропустить важные сообщения
        logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    asyncio.run(main())

