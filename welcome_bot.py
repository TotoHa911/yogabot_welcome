from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CallbackContext, CommandHandler, CallbackQueryHandler
import os
import logging
import requests

# Токен от BotFather
TOKEN = "8128088643:AAFX6vFLh8HAlcm_IxBS4DJzGdbyirQAiWc"

# Ссылки на канал и группу
CHANNEL_USERNAME = "Doroga_k_Yoga"
GROUP_USERNAME = "chatdorogakyoga"

# ID чата, куда бот будет направлять (вторая часть)
BOT_MENU_LINK = "https://t.me/YogaWelcomebot?start=go"

# Включаем логгирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def start(update: Update, context: CallbackContext):
    user = update.effective_user
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔔 Подписаться на канал", url=f"https://t.me/{CHANNEL_USERNAME}")],
        [InlineKeyboardButton("💬 Вступить в чат", url=f"https://t.me/{GROUP_USERNAME}")],
        [InlineKeyboardButton("✅ Я подписался", callback_data="check")]
    ])

    text = (
        f"привет, {user.first_name or 'друг'} 🤍\n\n"
        "добро пожаловать в пространство йоги и тёплого общения 🌿\n\n"
        "чтобы открыть меню, пожалуйста:\n"
        "1. подпишись на наш канал и группу\n"
        "2. нажми кнопку ниже «я подписался»"
    )
    update.message.reply_text(text, reply_markup=keyboard)

def check_subscription(user_id):
    def is_member(username):
        url = f"https://api.telegram.org/bot{TOKEN}/getChatMember"
        response = requests.get(url, params={"chat_id": f"@{username}", "user_id": user_id})
        if response.ok:
            status = response.json()["result"]["status"]
            return status in ["member", "administrator", "creator"]
        return False

    return is_member(CHANNEL_USERNAME) and is_member(GROUP_USERNAME)

def button_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = query.from_user.id

    if query.data == "check":
        if check_subscription(user_id):
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("🌿 Открыть меню", url=BOT_MENU_LINK)]
            ])
            query.edit_message_text(
                "спасибо за подписку 🤍\nтеперь ты можешь открыть главное меню бота:",
                reply_markup=keyboard
            )
        else:
            query.answer("Подписка не найдена 🙈", show_alert=True)

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button_callback))

    print("Приветственный бот запущен!")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
