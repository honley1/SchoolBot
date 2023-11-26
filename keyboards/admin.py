from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from database import getUserLang


async def mainKeyboardAdmin(userID) -> ReplyKeyboardMarkup:
    userLang = await getUserLang(userID)

    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📧 Обращение")],
            [KeyboardButton(text="💬 Консультация")],
            [KeyboardButton(text="⚙️ Настройки" if userLang == "Русский" else "⚙️ Параметрлер")],
            [KeyboardButton(text="💻 Посмотреть все консультаций")],
            [KeyboardButton(text="📱 Посмотреть все обращения")],
            [KeyboardButton(text="👤 Посмотреть всех администраторов")],
            [KeyboardButton(text="🚽 Очистить данные")],
            [KeyboardButton(text="🖋 Добавить админа")]
        ], resize_keyboard=True
    )

    return kb


canckb = ReplyKeyboardMarkup(resize_keyboard=True)
canckb1 = KeyboardButton(text="❌ Отмена")
canckb.add(canckb1)
