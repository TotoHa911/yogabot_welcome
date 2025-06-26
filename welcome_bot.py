from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler, MessageHandler, Filters

# ✅ Твой токен приветственного бота
TOKEN = "8128088643:AAFX6vFLh8HAlcm_IxBS4DJzGdbyirQAiWc"

# ✅ Твой канал и чат (без @)
CHANNEL_USERNAME = "Doroga_k_Yoga"
GROUP_USERNAME = "chatdorogakyoga"

def start(update: Update, context: CallbackContext):
    user = update.effective_user

    buttons = [
        [InlineKeyboardButton("📢 Подписаться на канал", url=f"https://t.me/{CHANNEL_USERNAME}")],
        [InlineKeyboardButton("💬 Вступить в чат", url=f"https://t.me/{GROUP_USERNAME}")],
        [InlineKeyboardButton("✅ Я подписался", callback_data="check_subs")]
    ]
    update.message.reply_text(
        f"Привет, {user.first_name or 'друг'}! 🧘‍♀️\n\n"
        "Перед тем как открыть меню, пожалуйста подпишись:\n\n"
        "📢 На наш канал — там много полезного\n"
        "💬 И на уютный чат — чтобы общаться с единомышленниками\n\n"
        "Когда подпишешься — жми кнопку ниже ⬇️",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

def check_subs(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = query.from_user.id
    bot = context.bot

    # Проверка подписки
    try:
        channel_status = bot.get_chat_member(f"@{CHANNEL_USERNAME}", user_id).status
        group_status = bot.get_chat_member(f"@{GROUP_USERNAME}", user_id).status

        is_subscribed = channel_status not in ['left', 'kicked'] and group_status not in ['left', 'kicked']

        if is_subscribed:
            query.answer()
            query.edit_message_text(
                "Спасибо за подписку! 🌿\n\n"
                "Теперь можно открыть главное меню:",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("📂 Открыть меню", url="https://t.me/YogaWelcomebot")]
                ])
            )
        else:
            raise Exception("Not subscribed")

    except Exception:
        query.answer()
        query.edit_message_text(
            "Похоже, ты ещё не подписался на канал и чат 🙈\n\n"
            "Подпишись и нажми кнопку ещё раз ⬇️",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📢 Подписаться на канал", url=f"https://t.me/{CHANNEL_USERNAME}")],
                [InlineKeyboardButton("💬 Вступить в чат", url=f"https://t.me/{GROUP_USERNAME}")],
                [InlineKeyboardButton("✅ Я подписался", callback_data="check_subs")]
            ])
        )

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(check_subs))

    print("Приветственный бот запущен!")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
