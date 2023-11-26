from aiogram import types, Dispatcher
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from aiogram.dispatcher import FSMContext
from keyboards import choice_lang, mainKeyboard, changeKeyboardFunc, causeKeyboard, setAppealKeyboard, skipKeyboard, \
    dayOfTheWeekKeyboard, timeConsultationKeyboard, mainKeyboardAdmin
from database import createUserColumn, userExist, getUserLang, getName, getUserPerson, getUserClass, setNewLang, \
    createUserColumnAppeal, createUserColumnConsultation, sql_read_admins
from states.client import *


async def start_cmd(message: types.Message, state: FSMContext):
    user = await userExist(message.from_user.id)
    if user:
        admin_id = sql_read_admins()
        if message.from_user.id in admin_id:
            userLang = await getUserLang(message.from_user.id)
            name = await getName(message.from_user.id)
            if userLang == "Русский":
                await message.answer(f"🙇🏻‍♂️ Здравствуйте, <b>{name}</b>!\n🔹 Выберите <b>действие</b>",
                                     parse_mode='html',
                                     reply_markup=await mainKeyboardAdmin(message.from_user.id))
                await state.finish()
            elif userLang == "Қазақша":
                await message.answer(f"🙇🏻‍♂️ Сәлеметсіз бе, <b>{name}</b>!\n🔹 Әрекетті <b>таңдаңыз</b>",
                                     parse_mode='html',
                                     reply_markup=await mainKeyboardAdmin(message.from_user.id))
                await state.finish()
        else:
            userLang = await getUserLang(message.from_user.id)
            name = await getName(message.from_user.id)
            if userLang == "Русский":
                await message.answer(f"👋 Здравствуйте, <b>{name}</b>!\n🔹 Выберите <b>действие</b>",
                                     parse_mode='html',
                                     reply_markup=await mainKeyboard(message.from_user.id))
                await state.finish()
            elif userLang == "Қазақша":
                await message.answer(f"👋 Сәлем, <b>{name}</b>!\n🔹 Әрекетті <b>таңдаңыз</b>",
                                     parse_mode='html',
                                     reply_markup=await mainKeyboard(message.from_user.id))
                await state.finish()

    else:
        await message.answer("<b>Выберите язык\n\nТілді таңдаңыз</b>",
                             parse_mode='html', reply_markup=choice_lang)
        await StartFSM.lang.set()


async def set_lang(callback: types.CallbackQuery, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['lang'] = callback.data

            ParentButton = KeyboardButton(callback_data="Parent",
                                          text="👤 Родитель" if data['lang'] == "Русский" else "👤 Ата-ана")

            kidButton = KeyboardButton(callback_data="Kid",
                                       text="💼 Школьник" if data['lang'] == "Русский" else "💼 Мектеп оқушысы")

            choice_person = ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)

            choice_person.add(ParentButton)
            choice_person.add(kidButton)

            if data['lang'] == "Русский":
                await callback.message.reply("Кто вы ?", reply_markup=choice_person)
            elif data['lang'] == "Қазақша":
                await callback.message.reply("Сіз кімсіз ?", reply_markup=choice_person)
        await callback.answer()

        await StartFSM.next()
    except Exception as e:
        await callback.message.reply("Ошибка регистраций , попробуйте снова")
        print(f"Ошибка: {e}")


async def set_person(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['person'] = message.text

            if data['lang'] == "Русский":
                await message.reply("🖋 Введите Ваше <b>имя</b> и <b>фамилию</b>:", parse_mode='html',
                                    reply_markup=types.ReplyKeyboardRemove())
            elif data['lang'] == "Қазақша":
                await message.reply("🖋<b>Атыңызды</b> және <b>фамилияңызды</b> енгізіңіз:", parse_mode='html',
                                    reply_markup=types.ReplyKeyboardRemove())

        await StartFSM.next()
    except Exception as e:
        await message.reply("Ошибка регистраций , попробуйте снова")
        print(f"Ошибка: {e}")


async def set_name(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['name'] = message.text

            if data['lang'] == "Русский":
                await message.reply("🖋 Введите Ваш <b>класс</b> и <b>литер</b>:\n(Например: 1А, 2Б)", parse_mode='html')
            elif data['lang'] == "Қазақша":
                await message.reply("🖋 <b>Сыныбы</b> мен <b>әріпті</b> енгізіңіз:\n(Мысалы: 1A, 2Б)", parse_mode='html')

        await StartFSM.next()

    except Exception as e:
        await message.reply("Ошибка регистраций , попробуйте снова")
        print(f"Ошибка: {e}")


async def set_Class(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['Class'] = message.text

            await createUserColumn(message.from_user.id, message.from_user.username, data['name'], data['lang'],
                                   data['person'], data['Class'])

            if data['lang'] == "Русский":
                admin_id = sql_read_admins()
                if message.from_user.id in admin_id:
                    await message.reply(f"👋 Здравствуйте, <b>{data['name']}</b>!\n🔹 Выберите <b>действие</b>",
                                        parse_mode='html',
                                        reply_markup=await mainKeyboardAdmin(message.from_user.id))
                else:
                    await message.reply(f"👋 Здравствуйте, <b>{data['name']}</b>!\n🔹 Выберите <b>действие</b>",
                                        parse_mode='html',
                                        reply_markup=await mainKeyboard(message.from_user.id))
            elif data['lang'] == "Қазақша":
                admin_id = sql_read_admins()
                if message.from_user.id in admin_id:
                    await message.reply(f"👋 Сәлем, <b>{data['name']}</b>!\n🔹 Әрекетті <b>таңдаңыз</b>",
                                        parse_mode='html',
                                        reply_markup=await mainKeyboardAdmin(message.from_user.id))

                else:
                    await message.reply(f"👋 Сәлем, <b>{data['name']}</b>!\n🔹 Әрекетті <b>таңдаңыз</b>",
                                        parse_mode='html',
                                        reply_markup=await mainKeyboard(message.from_user.id))

        await state.finish()

    except Exception as e:
        await message.reply("Ошибка регистраций , попробуйте снова")
        print(f"Ошибка: {e}")


async def settings_cmdRu(message: types.Message):
    user = await userExist(message.from_user.id)
    if user:
        person = await getUserPerson(message.from_user.id)
        userLang = await getUserLang(message.from_user.id)
        name = await getName(message.from_user.id)
        userClass = await getUserClass(message.from_user.id)
        await message.answer(f"<b>⚙️ Настройки</b>\n\n"
                             f"<b>{person}</b>\n"
                             f"Имя: <b>{name}</b>\n"
                             f"Класс: <b>{userClass}\n</b>"
                             f"Язык: <b>{userLang}</b>",
                             reply_markup=await changeKeyboardFunc(message.from_user.id),
                             parse_mode='html')
    else:
        await message.answer("<b>🚫 Вы не зарегистрированы\n\n🚫 Сіз тіркелмегенсіз\n\nЗарегистрироваться: "
                             "/start\nТіркелу: /start</b>", parse_mode='html')


async def settings_cmdKz(message: types.Message):
    user = await userExist(message.from_user.id)
    if user:
        person = await getUserPerson(message.from_user.id)
        userLang = await getUserLang(message.from_user.id)
        name = await getName(message.from_user.id)
        userClass = await getUserClass(message.from_user.id)
        await message.answer(f"<b>⚙️ Параметрлер</b>\n\n"
                             f"<b>{person}</b>\n"
                             f"Аты: <b>{name}</b>\n"
                             f"Сынып: <b>{userClass}</b>\n"
                             f"Тіл: <b>{userLang}</b>",
                             reply_markup=await changeKeyboardFunc(message.from_user.id), parse_mode='html')
    else:
        await message.answer("<b>🚫 Вы не зарегистрированы\n\n🚫 Сіз тіркелмегенсіз\n\nЗарегистрироваться: "
                             "/start\nТіркелу: /start</b>", parse_mode='html')


async def changeLang(callback: types.CallbackQuery):
    await callback.message.answer("<b>Выберите язык\n\nТілді таңдаңыз</b>",
                                  reply_markup=choice_lang, parse_mode='html')
    await callback.answer()
    await ChangeLangFSM.newLang.set()


async def newLangCmd(callback: types.CallbackQuery, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['newLang'] = callback.data

            userLang = data['newLang']
            name = await getName(callback.from_user.id)

            if userLang == "Русский":
                admin_id = sql_read_admins()
                if callback.message.from_user.id in admin_id:
                    await setNewLang(callback.from_user.id, userLang)
                    await callback.message.answer(f"👋 Здравствуйте, <b>{name}</b>!\n🔹 Выберите <b>действие</b>",
                                                  parse_mode='html',
                                                  reply_markup=await mainKeyboardAdmin(callback.from_user.id))
                else:
                    await setNewLang(callback.from_user.id, userLang)
                    await callback.message.answer(f"👋 Здравствуйте, <b>{name}</b>!\n🔹 Выберите <b>действие</b>",
                                                  parse_mode='html',
                                                  reply_markup=await mainKeyboard(callback.from_user.id))

            elif userLang == "Қазақша":
                await setNewLang(callback.from_user.id, userLang)
                admin_id = sql_read_admins()
                if callback.message.from_user.id in admin_id:
                    await callback.message.answer(f"👋 Сәлем, <b>{name}</b>!\n🔹 Әрекетті <b>таңдаңыз</b>",
                                                  parse_mode='html',
                                                  reply_markup=await mainKeyboardAdmin(callback.from_user.id))
                else:
                    await callback.message.answer(f"👋 Сәлем, <b>{name}</b>!\n🔹 Әрекетті <b>таңдаңыз</b>",
                                                  parse_mode='html',
                                                  reply_markup=await mainKeyboard(callback.from_user.id))

            await callback.answer()

            await state.finish()
    except Exception as e:
        await callback.message.reply("Ошибка регистраций , попробуйте снова")
        print(f"Ошибка: {e}")


async def appeal_cmd(message: types.Message):
    user = await userExist(message.from_user.id)
    if user:
        userLang = await getUserLang(message.from_user.id)
        await message.answer("👤 К кому вы хотели бы <b>обратиться</b> ?" if userLang == "Русский"
                             else "👤Кімге <b>хабарласқыңыз</b> келеді?", parse_mode='html',
                             reply_markup=await setAppealKeyboard(message.from_user.id))

        await AppealFSM.pscZdvr.set()

    else:
        await message.answer("<b>🚫 Вы не зарегистрированы\n\n🚫 Сіз тіркелмегенсіз\n\nЗарегистрироваться: "
                             "/start\nТіркелу: /start</b>", parse_mode='html')


async def pscZdvr_cmd(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['pscZdvr'] = message.text

        if data['pscZdvr'] == "👩‍⚕ Психолог" or data['pscZdvr'] == "👨‍💼 ЗДВР" or data['pscZdvr'] == "👨‍💼 ДТЖЖО":

            userLang = await getUserLang(message.from_user.id)

            await message.answer("Выберите <b>причину</b> обращения" if userLang == "Русский"
                                 else "📄 Сұрауыңыздың <b>себебін</b> таңдаңыз",
                                 reply_markup=await causeKeyboard(message.from_user.id),
                                 parse_mode='html')
            await AppealFSM.next()

        elif data['pscZdvr'] == "◀️ Назад" or data['pscZdvr'] == "◀️ Артқа":
            userLang = await getUserLang(message.from_user.id)
            name = await getName(message.from_user.id)

            await message.answer(f"👋 Здравствуйте, <b>{name}</b>!\n🔹 Выберите <b>действие</b>" if userLang == "Русский"
                                 else f"👋 Сәлем, <b>{name}</b>!\n🔹 Әрекетті <b>таңдаңыз</b>",
                                 parse_mode='html',
                                 reply_markup=await mainKeyboard(message.from_user.id))

            await state.finish()
        else:
            userLang = await getUserLang(message.from_user.id)

            await state.finish()
            await message.answer("Вы ввели не соответствующую команду" if userLang == "Русский"
                                 else "Сіз қате пәрменді енгіздіңіз")


async def causeAppeal_cmd(message: types.Message, state: FSMContext):
    causeRuArray = ["Поведенческое расстройство", "Буллинг", "Нет желания учиться", "Нет друзей",
                    "Конфликт с одноклассниками", "Снижение мотивации"]

    causeKzArray = ["Мінез-құлықтың бұзылуы", "Қорқыту", "Оқуға деген құштарлықтың болмауы", "Достары жоқ",
                    "Сыныптастармен жанжал", "Мотивацияның төмендеуі"]

    async with state.proxy() as data:
        data['cause'] = message.text

        causeAppeal = data['cause']

        userLang = await getUserLang(message.from_user.id)

        if causeAppeal in causeKzArray or causeAppeal in causeRuArray:

            await message.answer("📝 Опишите <b>Вашу проблему</b>:" if userLang == "Русский"
                                 else "📝 <b>Мәселеңізді</b> сипаттаңыз:", parse_mode='html',
                                 reply_markup=await skipKeyboard(message.from_user.id))

            await AppealFSM.next()
        elif causeAppeal == "◀️ Haзaд" or causeAppeal == "◀️ Apтқa":

            await message.answer("👤 К кому вы хотели бы <b>обратиться</b> ?" if userLang == "Русский"
                                 else "👤Кімге <b>хабарласқыңыз</b> келеді?", parse_mode='html',
                                 reply_markup=await setAppealKeyboard(message.from_user.id))

            await AppealFSM.previous()


async def descriptionOfProblem(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['descriptionOfProblem'] = message.text

        userLang = await getUserLang(message.from_user.id)

        await message.answer("📞 Оставьте <b>свои контакты</b>, чтобы мы с Вами связались: \n"
                             "<i>(Например: Номер телефона, Электронная почта)</i>"
                             if userLang == "Русский"
                             else "📞 Біз сізбен байланыса алуымыз үшін <b>контактілеріңізді</b> қалдырыңыз: \n"
                                  "<i>(Мысалы: Телефон нөмірі, Электрондық пошта)</i>", parse_mode='html')

        await AppealFSM.next()


async def contactAppeal_cmd(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Contact'] = message.text

        userPerson = await getUserPerson(message.from_user.id)
        name = await getName(message.from_user.id)
        Class = await getUserClass(message.from_user.id)
        userLang = await getUserLang(message.from_user.id)

        await createUserColumnAppeal(message.from_user.id, userPerson, message.from_user.username, name, Class,
                                     data['pscZdvr'], data['cause'], data['descriptionOfProblem'], data['Contact'])

        admin_id = sql_read_admins()
        if message.from_user.id in admin_id:
            await message.answer("✅ Спасибо, Ваше <b>обращение принято</b>!" if userLang == "Русский"
                                 else "✅ Рахмет, сіздің <b>апелляцияңыз қабылданды</b>!", parse_mode='html',
                                 reply_markup=await mainKeyboardAdmin(message.from_user.id))
        else:
            await message.answer("✅ Спасибо, Ваше <b>обращение принято</b>!" if userLang == "Русский"
                                 else "✅ Рахмет, сіздің <b>апелляцияңыз қабылданды</b>!", parse_mode='html',
                                 reply_markup=await mainKeyboard(message.from_user.id))

        await state.finish()


async def consultation_cmd(message: types.Message):
    user = await userExist(message.from_user.id)
    if user:
        userLang = await getUserLang(message.from_user.id)
        await message.answer("👤 К кому вы хотели бы <b>обратиться</b> ?" if userLang == "Русский"
                             else "👤Кімге <b>хабарласқыңыз</b> келеді?", parse_mode='html',
                             reply_markup=await setAppealKeyboard(message.from_user.id))

        await ConsultationFSM.pscZdvr.set()

    else:
        await message.answer("<b>🚫 Вы не зарегистрированы\n\n🚫 Сіз тіркелмегенсіз\n\nЗарегистрироваться: "
                             "/start\nТіркелу: /start</b>", parse_mode='html')


async def pscZdvrConsultation_cmd(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['pscZdvr'] = message.text

        if data['pscZdvr'] == "👩‍⚕ Психолог" or data['pscZdvr'] == "👨‍💼 ЗДВР" or data['pscZdvr'] == "👨‍💼 ДТЖЖО":

            userLang = await getUserLang(message.from_user.id)

            await message.answer("🕐 Выберите <b>день недели</b>" if userLang == "Русский"
                                 else "🕐 <b>Апта күнін</b> таңдаңыз",
                                 reply_markup=await dayOfTheWeekKeyboard(message.from_user.id),
                                 parse_mode='html')
            await ConsultationFSM.next()

        elif data['pscZdvr'] == "◀️ Назад" or data['pscZdvr'] == "◀️ Артқа":
            userLang = await getUserLang(message.from_user.id)
            name = await getName(message.from_user.id)

            await message.answer(f"👋 Здравствуйте, <b>{name}</b>!\n🔹 Выберите <b>действие</b>" if userLang == "Русский"
                                 else f"👋 Сәлем, <b>{name}</b>!\n🔹 Әрекетті <b>таңдаңыз</b>",
                                 parse_mode='html',
                                 reply_markup=await mainKeyboard(message.from_user.id))

            await state.finish()
        else:
            userLang = await getUserLang(message.from_user.id)

            await state.finish()
            await message.answer("Вы ввели не соответствующую команду" if userLang == "Русский"
                                 else "Сіз қате пәрменді енгіздіңіз")


async def dayOfTheWeek_cmd(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['dayOfTheWeek'] = message.text

        dayOfTheWeek = data['dayOfTheWeek']

        time = ["9:00",
                "9:30",
                "10:00",
                "10:30",
                "11:00",
                "11:30",
                "12:00",
                "12:30",
                "14:30",
                "15:00",
                "15:30",
                "16:00",
                "16:30",
                "17:00",
                "17:30"]

        dayOfTheWeekArray = ["Понедельник",
                             "Вторник",
                             "Среда",
                             "Четверг",
                             "Пятница",
                             "Дүйсенбі",
                             "Сейсенбі",
                             "Сәрсенбі",
                             "Бейсенбі",
                             "Жұма"]

        if dayOfTheWeek in dayOfTheWeekArray:

            userLang = await getUserLang(message.from_user.id)

            await message.answer("🕐 Выберите или введите удобное для вас <b>время</b>" if userLang == "Русский" else
                                 "🕐 Ыңғайлы уақытты таңдаңыз немесе енгізіңіз", parse_mode='html',
                                 reply_markup=await timeConsultationKeyboard(message.from_user.id))
            await ConsultationFSM.next()
        elif dayOfTheWeek == "◀️ Назад" or dayOfTheWeek == "◀️ Артқа":
            userLang = await getUserLang(message.from_user.id)

            await message.answer("👤 К кому вы хотели бы <b>обратиться</b> ?" if userLang == "Русский"
                                 else "👤Кімге <b>хабарласқыңыз</b> келеді?", parse_mode='html',
                                 reply_markup=await setAppealKeyboard(message.from_user.id))

            await ConsultationFSM.previous()


async def timeForConsultation(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['timeUser'] = message.text

        timeUser = data['timeUser']

        userLang = await getUserLang(message.from_user.id)

        if timeUser == "◀️ Назад" or timeUser == "◀️ Артқа":
            userLang = await getUserLang(message.from_user.id)

            await message.answer("🕐 Выберите <b>день недели</b>" if userLang == "Русский"
                                 else "🕐 <b>Апта күнін</b> таңдаңыз",
                                 reply_markup=await dayOfTheWeekKeyboard(message.from_user.id),
                                 parse_mode='html')

            await ConsultationFSM.previous()
        else:
            await message.answer("📞 Оставьте <b>свои контакты</b>, чтобы мы с Вами связались: \n"
                                 "<i>(Например: Номер телефона, Электронная почта)</i>"
                                 if userLang == "Русский"
                                 else "📞 Біз сізбен байланыса алуымыз үшін <b>контактілеріңізді</b> қалдырыңыз: \n"
                                      "<i>(Мысалы: Телефон нөмірі, Электрондық пошта)</i>", parse_mode='html',
                                 reply_markup=await skipKeyboard(message.from_user.id))

            await ConsultationFSM.next()


async def contactConsultation(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Contact'] = message.text

        userLang = await getUserLang(message.from_user.id)

        person = await getUserPerson(message.from_user.id)
        name = await getName(message.from_user.id)
        Class = await getUserClass(message.from_user.id)

        await createUserColumnConsultation(message.from_user.id, person, message.from_user.username, name, Class,
                                           data['pscZdvr'], data['dayOfTheWeek'], data['Contact'])

        admin_id = sql_read_admins()
        if message.from_user.id in admin_id:
            await message.answer(f"✅ Консультация успешно назначена на <b>{data['dayOfTheWeek']}</b>, <b>{data['timeUser']}</b>!"
                                 if userLang == "Русский" else f"✅ Консультация <b>{data['dayOfTheWeek']}, "
                                 f"{data['timeUser']}</b> күндеріне сәтті жоспарланған!",
                                 parse_mode='html', reply_markup=await mainKeyboardAdmin(message.from_user.id))
        else:
            await message.answer(f"✅ Консультация успешно назначена на <b>{data['dayOfTheWeek']}</b>, <b>{data['timeUser']}</b>!"
                                 if userLang == "Русский" else f"✅ Консультация <b>{data['dayOfTheWeek']}, "
                                 f"{data['timeUser']}</b> күндеріне сәтті жоспарланған!",
                                 parse_mode='html', reply_markup=await mainKeyboard(message.from_user.id))

        await state.finish()


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(start_cmd, commands=['start'], state='*')
    dp.register_callback_query_handler(set_lang, state=StartFSM.lang)
    dp.register_message_handler(set_person, state=StartFSM.person)
    dp.register_message_handler(set_name, state=StartFSM.name)
    dp.register_message_handler(set_Class, state=StartFSM.Class)
    dp.register_message_handler(settings_cmdRu, text="⚙️ Настройки")
    dp.register_message_handler(settings_cmdKz, text="⚙️ Параметрлер")
    dp.register_callback_query_handler(changeLang, text=['changeLang'])
    dp.register_callback_query_handler(newLangCmd, state=ChangeLangFSM.newLang)
    dp.register_message_handler(appeal_cmd, text="📧 Обращение")
    dp.register_message_handler(pscZdvr_cmd, state=AppealFSM.pscZdvr)
    dp.register_message_handler(causeAppeal_cmd, state=AppealFSM.cause)
    dp.register_message_handler(descriptionOfProblem, state=AppealFSM.descriptionOfProblem)
    dp.register_message_handler(contactAppeal_cmd, state=AppealFSM.Contact)
    dp.register_message_handler(consultation_cmd, text="💬 Консультация")
    dp.register_message_handler(pscZdvrConsultation_cmd, state=ConsultationFSM.pscZdvr)
    dp.register_message_handler(dayOfTheWeek_cmd, state=ConsultationFSM.dayOfTheWeek)
    dp.register_message_handler(timeForConsultation, state=ConsultationFSM.timeUser)
    dp.register_message_handler(contactConsultation, state=ConsultationFSM.Contact)

