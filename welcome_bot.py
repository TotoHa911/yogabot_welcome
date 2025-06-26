from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext
import logging
import os
import telegram.error

# ✅ Настройки
TOKEN = "8128088643:AAFX6vFLh8HAlcm_IxBS4DJzGdbyirQAiWc"
CHANNEL_ID = "@Doroga_k_Yoga"
GROUP_ID = "@chatdorogakyoga"
MENU_BOT_LINK = "https://t.me/YogaWelcomeBot"  # основной бот-меню

# ✅ Включаем логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def start(update: Update, context: CallbackContext):
    user_id = update.effective_user.id

    try:
        # Проверяем подписку на канал и чат
        chat_status = context.bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id).status
        group_status = context.bot.get_chat_member(chat_id=GROUP_ID, user_id=user_id).status

        if chat_status in ['member', 'administrator', 'creator'] and group_status in ['member', 'administrator', 'creator']:
            # ✅ Подписан — даём кнопку перехода в меню
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("🌿 Перейти в главное меню", url=MENU_BOT_LINK)]
            ])
            update.message.reply_text(
                "ура! ты с нами 🧘‍♀️\n\nвсё готово — можешь открыть главное меню и выбрать подходящую практику ✨",
                reply_markup=keyboard
            )
        else:
            # ⛔️ Не подписан — просим подписаться
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("📌 Подписаться на канал", url=f"https://t.me/{CHANNEL_ID.lstrip('@')}")],
                [InlineKeyboardButton("💬 Войти в чат", url=f"https://t.me/{GROUP_ID.lstrip('@')}")],
                [InlineKeyboardButton("🔄 Я подписался", callback_data="check")]
            ])
            update.message.reply_text(
                "прежде чем продолжим 🌿\n\nпожалуйста, подпишись на наш канал и чат — так мы будем на связи и ты не пропустишь полезности 🧘‍♀️",
                reply_markup=keyboard
            )

    except telegram.error.Unauthorized:
        update.message.reply_text("❌ Упс! Бот не может проверить твою подписку. Напиши нам вручную.")
    except Exception as e:
        logging.error(f"Ошибка: {e}")
        update.message.reply_text("⚠️ Что-то пошло не так. Попробуй ещё раз.")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))

    print("✨ Приветственный бот запущен!")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
