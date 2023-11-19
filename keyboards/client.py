from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from database import getUserLang

# ************************************* 1 *************************************

russianButton = InlineKeyboardButton(callback_data="Русский", text="🇷🇺 Русский")
kazakhButton = InlineKeyboardButton(callback_data="Қазақша", text="🇰🇿 Қазақша")

choice_lang = InlineKeyboardMarkup(row_width=2, resize_keyboard=True)

choice_lang.add(kazakhButton)
choice_lang.add(russianButton)


# ************************************* 2 *************************************

async def mainKeyboard(userID) -> ReplyKeyboardMarkup:
    userLang = await getUserLang(userID)

    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📧 Обращение")],
            [KeyboardButton(text="💬 Консультация")],
            [KeyboardButton(text="⚙️ Настройки" if userLang == "Русский" else "⚙️ Параметрлер")]
        ], resize_keyboard=True
    )

    return kb

# ************************************* 3 *************************************


async def changeKeyboardFunc(userID) -> InlineKeyboardMarkup:
    userLang = await getUserLang(userID)

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton("⌨️ Изменить язык" if userLang == "Русский" else "⌨️ Тілді өзгерту",
                                  callback_data="changeLang")]
        ]
    )

    return kb

# ************************************* 4 *************************************


async def setAppealKeyboard(userID) -> ReplyKeyboardMarkup:
    userLang = await getUserLang(userID)

    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="👩‍⚕ Психолог")],
            [KeyboardButton(text="👨‍💼 ЗДВР" if userLang == "Русский" else "👨‍💼 ДТЖЖО")],
            [KeyboardButton(text="◀️ Назад" if userLang == "Русский" else "◀️ Артқа")]
        ], resize_keyboard=True
    )

    return kb


# ************************************* 5 *************************************
async def causeKeyboard(userID) -> ReplyKeyboardMarkup:
    userLang = await getUserLang(userID)

    causeRuArray = ["Поведенческое расстройство", "Буллинг", "Нет желания учиться", "Нет друзей",
                    "Конфликт с одноклассниками", "Снижение мотивации"]

    causeKzArray = ["Мінез-құлықтың бұзылуы", "Қорқыту", "Оқуға деген құштарлықтың болмауы", "Достары жоқ",
                    "Сыныптастармен жанжал", "Мотивацияның төмендеуі"]

    kb = ReplyKeyboardMarkup(resize_keyboard=True)

    causeArray = causeRuArray if userLang == "Русский" else causeKzArray

    # Добавление кнопок в клавиатуру
    for i in causeArray:
        kb.add(KeyboardButton(text=i))

    kb.add("◀️ Haзaд" if userLang == "Русский" else "◀️ Apтқa")

    return kb

# ************************************* 6 *************************************


async def skipKeyboard(userID):
    userLang = await getUserLang(userID)
    kb = ReplyKeyboardMarkup(resize_keyboard=True)

    kb.add("▶️ Пропустить" if userLang == "Русский" else "▶️ Өткізіп жіберу")

    return kb


# ************************************* 7 *************************************

async def dayOfTheWeekKeyboard(userID) -> ReplyKeyboardMarkup:
    userLang = await getUserLang(userID)

    dayOfTheWeekArrayRu = ["Понедельник",
                           "Вторник",
                           "Среда",
                           "Четверг",
                           "Пятница",
                           ]

    dayOfTheWeekArrayKz = [
                            "Дүйсенбі",
                            "Сейсенбі",
                            "Сәрсенбі",
                            "Бейсенбі",
                            "Жұма"
                        ]

    kb = ReplyKeyboardMarkup(resize_keyboard=True)

    causeArray = dayOfTheWeekArrayRu if userLang == "Русский" else dayOfTheWeekArrayKz

    for i in causeArray:
        kb.add(KeyboardButton(text=i))

    kb.add(KeyboardButton(text="◀️ Назад" if userLang == "Русский" else "◀️ Артқа"))

    return kb


async def timeConsultationKeyboard(userID):

    userLang = await getUserLang(userID)

    time = [
        "9:00",
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
        "17:30"
    ]

    kb = ReplyKeyboardMarkup(resize_keyboard=True)

    for i in time:
        kb.add(KeyboardButton(text=i))

    kb.add(KeyboardButton(text="◀️ Назад" if userLang == "Русский" else "◀️ Артқа"))

    return kb

