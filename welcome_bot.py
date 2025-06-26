from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext
import os

TOKEN = "8128088643:AAFX6vFLh8HAlcm_IxBS4DJzGdbyirQAiWc"
CHANNEL_ID = "-1002026202622"  # @Doroga_k_Yoga
GROUP_ID = "-1001942632620"    # @chatdorogakyoga

def start(update: Update, context: CallbackContext):
    user = update.effective_user
    chat_id = update.effective_chat.id

    try:
        is_channel_member = context.bot.get_chat_member(CHANNEL_ID, user.id).status in ["member", "administrator", "creator"]
        is_group_member = context.bot.get_chat_member(GROUP_ID, user.id).status in ["member", "administrator", "creator"]
    except:
        is_channel_member = False
        is_group_member = False

    if is_channel_member and is_group_member:
        keyboard = [[InlineKeyboardButton("👇 открыть меню", url="https://t.me/YogaWelcomeBot?start=go")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(
            "🌿 ты уже с нами!\n\nтеперь можно перейти в бот-меню 👇",
            reply_markup=reply_markup
        )
    else:
        keyboard = [
            [InlineKeyboardButton("📌 подписаться на канал", url="https://t.me/Doroga_k_Yoga")],
            [InlineKeyboardButton("💬 вступить в чат", url="https://t.me/chatdorogakyoga")],
            [InlineKeyboardButton("🔄 Я подписался", callback_data="check_subs")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(
            "👋 привет! прежде чем продолжить, пожалуйста, подпишись на наш канал и вступи в чат 🌿",
            reply_markup=reply_markup
        )

def button(update, context):
    query = update.callback_query
    user = query.from_user
    context.bot.answer_callback_query(query.id)

    is_channel_member = context.bot.get_chat_member(CHANNEL_ID, user.id).status in ["member", "administrator", "creator"]
    is_group_member = context.bot.get_chat_member(GROUP_ID, user.id).status in ["member", "administrator", "creator"]

    if is_channel_member and is_group_member:
        keyboard = [[InlineKeyboardButton("👇 открыть меню", url="https://t.me/YogaWelcomeBot?start=go")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text("🌿 отлично! теперь можно открыть меню:", reply_markup=reply_markup)
    else:
        query.edit_message_text("❗️ ты ещё не подписался на всё необходимое. Попробуй ещё раз.")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(telegram.ext.CallbackQueryHandler(button))

    print("Welcome Bot запущен!")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
