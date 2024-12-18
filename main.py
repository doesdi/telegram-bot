import logging
from telegram import *
from telegram.ext import *
import os
from dotenv import load_dotenv


load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

questions = [
    ("Какой язык программирования используется для создания Telegram-ботов?", "Python",
     ["Python", "Java", "C#", "JavaScript"]),
    ("Какой метод используется для отправки сообщений в Telegram?", "sendMessage",
     ["sendMessage", "postMessage", "sendText", "sendMsg"]),
    ("Какой оператор используется для сравнения в Python?", "==", ["==", "=", "===", "!="]),
    ("Какой метод добавляет элемент в список?", "append", ["add", "append", "insert", "push"]),
    ("Какой символ используется для комментариев в Python?", "#", ["#", "//", "/*", "--"])
]

score = 0
current_question = 0

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global score, current_question
    score = 0
    current_question = 0
    await update.message.reply_text(f"{update.message.from_user.first_name}, Добро пожаловать в викторину! Начнем с первого вопроса.")
    await ask_question(update, context)

async def ask_question(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global current_question
    question, correct_answer, options = questions[current_question]
    keyboard = [[InlineKeyboardButton(option, callback_data=option) for option in options]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    try:
        message = update.callback_query.message if update.callback_query else update.message
        await message.reply_text(question, reply_markup=reply_markup)
    except Exception as e:
        logger.error(f"Ошибка при отправке вопроса: {e}")

async def answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global score, current_question
    await update.callback_query.answer()
    user_answer = update.callback_query.data
    correct_answer = questions[current_question][1]
    try:
        if user_answer.lower() == correct_answer.lower():
            score += 1
            await update.callback_query.edit_message_text(text="Правильно!")
        else:
            await update.callback_query.edit_message_text(text=f"Неправильно! Правильный ответ: {correct_answer}")

        current_question += 1

        if current_question < len(questions):
            await ask_question(update, context)
        else:
            await update.callback_query.edit_message_text(text=f"Викторина окончена! Ваш счет: {score}/{len(questions)}")
            current_question = 0
    except Exception as e:
        logger.error(f"Ошибка в обработке ответа: {e}")
        await update.callback_query.edit_message_text(text="Произошла ошибка. Попробуйте еще раз.")

def main() -> None:
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(answer))
    application.run_polling()

if __name__ == '__main__':
    main()