from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove


YOUR_TELEGRAM_ID = '1080325838'

# Этапы
NAME, TYPE, DESC = range(3)

# Старт
def start(update: Update, context: CallbackContext):
    update.message.reply_text("👋 Привет! Я помогу оформить заказ на разработку.\n\nКак тебя зовут?")
    return NAME

def get_name(update: Update, context: CallbackContext):
    context.user_data['name'] = update.message.text

    reply_keyboard = [['🤖 Бот', '🌐 Сайт'], ['⚙️ Скрипт', '📄 Лендинг'], ['📦 Другое']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True)

    update.message.reply_text(
        "Отлично, приятно познакомиться! 😊\n\nТеперь выбери, что тебе нужно:",
        reply_markup=markup
    )
    return TYPE



def get_type(update: Update, context: CallbackContext):
    context.user_data['type'] = update.message.text

    update.message.reply_text(
        "Супер! ✨ Теперь опиши, пожалуйста, что именно ты хочешь. Чем подробнее — тем лучше! 📝",
        reply_markup=ReplyKeyboardRemove()
    )
    return DESC



def get_desc(update: Update, context: CallbackContext):
    context.user_data['desc'] = update.message.text
    user = update.message.from_user

    order_text = (
        f"🆕 Новый заказ:\n\n"
        f"👤 Имя: {context.user_data['name']}\n"
        f"📦 Тип: {context.user_data['type']}\n"
        f"📝 Описание: {context.user_data['desc']}\n"
        f"💬 Telegram: @{user.username if user.username else 'нет username'}"
    )

    context.bot.send_message(chat_id=YOUR_TELEGRAM_ID, text=order_text)

    update.message.reply_text("🎉 Спасибо! Я получил заказ и скоро с тобой свяжусь. Хорошего дня! ☀️")
    return ConversationHandler.END


def cancel(update: Update, context: CallbackContext):
    update.message.reply_text("🚫 Заказ отменён. Если что — просто напиши /start 😉")
    return ConversationHandler.END


def main():
    updater = Updater("8034962442:AAEh7mNCHP4o_IEeKf4LLilYbUMLlfkxX14", use_context=True)
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            NAME: [MessageHandler(Filters.text & ~Filters.command, get_name)],
            TYPE: [MessageHandler(Filters.text & ~Filters.command, get_type)],
            DESC: [MessageHandler(Filters.text & ~Filters.command, get_desc)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dp.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
