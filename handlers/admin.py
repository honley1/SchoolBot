from aiogram import types, Dispatcher

from aiogram.dispatcher import FSMContext

from keyboards import mainKeyboardAdmin, mainKeyboard, canckb
from database import userExist, sql_read_admins, sql_read_consultation, sql_read_appeal, sql_read_admins_for_admin, \
    sql_delete_column_query, sql_add_admins
from states.admin import *


async def get_all_consultation(message: types.Message):
    user = await userExist(message.from_user.id)
    if user:
        admin_id = sql_read_admins()
        if message.from_user.id in admin_id:
            string = await sql_read_consultation()
            await message.answer(string, parse_mode='html', reply_markup=await mainKeyboardAdmin(message.from_user.id))
        else:
            await message.answer("Вы не <b>админ</b> !",
                                 reply_markup=await mainKeyboard(message.from_user.id),
                                 parse_mode='html')
    else:
        await message.answer("<b>🚫 Вы не зарегистрированы\n\n🚫 Сіз тіркелмегенсіз\n\nЗарегистрироваться: "
                             "/start\nТіркелу: /start</b>", parse_mode='html')


async def get_all_appeal(message: types.Message):
    user = await userExist(message.from_user.id)
    if user:
        admin_id = sql_read_admins()
        if message.from_user.id in admin_id:
            string = await sql_read_appeal()
            await message.answer(string, parse_mode='html', reply_markup=await mainKeyboardAdmin(message.from_user.id))
        else:
            await message.answer("Вы не <b>админ</b> !",
                                 reply_markup=await mainKeyboard(message.from_user.id),
                                 parse_mode='html')
    else:
        await message.answer("<b>🚫 Вы не зарегистрированы\n\n🚫 Сіз тіркелмегенсіз\n\nЗарегистрироваться: "
                             "/start\nТіркелу: /start</b>", parse_mode='html')


async def get_user_count_cmd(message: types.Message):
    user = await userExist(message.from_user.id)
    if user:
        admin_id = sql_read_admins()
        if message.from_user.id in admin_id:
            string = await sql_read_admins_for_admin()
            await message.answer(string, parse_mode='html', reply_markup=await mainKeyboardAdmin(message.from_user.id))
        else:
            await message.answer("Вы не <b>админ</b> !",
                                 reply_markup=await mainKeyboard(message.from_user.id),
                                 parse_mode='html')
    else:
        await message.answer("<b>🚫 Вы не зарегистрированы\n\n🚫 Сіз тіркелмегенсіз\n\nЗарегистрироваться: "
                             "/start\nТіркелу: /start</b>", parse_mode='html')


async def delete_all_column_query(message: types.Message):
    user = await userExist(message.from_user.id)
    if user:
        if message.from_user.id == 803817300:
            await sql_delete_column_query()
            await message.answer("✅ Данные <b>успешно</b> очищены !", parse_mode='html',
                                 reply_markup=await mainKeyboardAdmin(message.from_user.id))
        else:
            await message.answer("Вы не <b>админ</b> !",
                                 reply_markup=await mainKeyboard(message.from_user.id),
                                 parse_mode='html')
    else:
        await message.answer("<b>🚫 Вы не зарегистрированы\n\n🚫 Сіз тіркелмегенсіз\n\nЗарегистрироваться: "
                             "/start\nТіркелу: /start</b>", parse_mode='html')


async def cmd_cancel(message: types.Message, state: FSMContext):
    if state is None:
        return

    await state.finish()
    await message.reply('Добавление <b>отменено</b>',
                        parse_mode='html',
                        reply_markup=await mainKeyboardAdmin(message.from_user.id))


async def add_admin_id(message: types.Message):
    try:
        if message.from_user.id == 803817300:
            await message.reply("Отправьте <b>ID</b> нового админа",
                                parse_mode='html',
                                reply_markup=canckb)
            await AddAdminState.admin_id.set()
        else:
            await message.answer("Вы не <b>админ</b> !",
                                 reply_markup=await mainKeyboard(message.from_user.id),
                                 parse_mode='html')
    except Exception as e:
        print(f"Ошибка: {e}")


async def load_admin_id(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['admin_id'] = int(message.text)

        await sql_add_admins(data['admin_id'])
        await message.reply(text="✅ Новый админ успешно добавлен")
        await state.finish()
    except ValueError as e:
        await message.answer("Вы ввели не <b>ID</b>")
        await state.finish()


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(get_all_consultation, text="💻 Посмотреть все консультаций")
    dp.register_message_handler(get_all_appeal, text="📱 Посмотреть все обращения")
    dp.register_message_handler(get_user_count_cmd, text="👤 Посмотреть всех администраторов")
    dp.register_message_handler(delete_all_column_query, text="🚽 Очистить данные")
    dp.register_message_handler(cmd_cancel, text='❌ Отмена', state='*')
    dp.register_message_handler(add_admin_id, text='🖋 Добавить админа')
    dp.register_message_handler(load_admin_id, state=AddAdminState.admin_id)

