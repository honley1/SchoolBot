from aiogram import executor
from createBot import dp
from database.database import sql_start
from handlers import client, admin


async def on_startup(_):
    print("Бот запущен")
    sql_start()


client.register_handlers_client(dp)
admin.register_handlers_admin(dp)


if __name__ == "__main__":
    executor.start_polling(dispatcher=dp, on_startup=on_startup)
