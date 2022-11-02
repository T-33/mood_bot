import time
import random
from datetime import datetime
from threading import Thread

import schedule
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler, CallbackContext

from settings import TOKEN

users = [] # Список пользователей
histoy = {} # История ответов пользователя

# Создание клавиатуры
keyboard = [
        [
            InlineKeyboardButton("😃", callback_data='5'),
            InlineKeyboardButton("😐", callback_data='4'),
            InlineKeyboardButton("😞", callback_data='3'),
            InlineKeyboardButton("☹️", callback_data='2'),
            InlineKeyboardButton("😢", callback_data='1'),
        ]
    ]


def start_user(update: Updater, context: CallbackContext):
    """Обработка команды /start"""
    user = update.effective_user
    print(user)
    users.append(user.id)
    histoy[user.id] = []
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Привет, {}! Я бот!".format(user.first_name), reply_markup=reply_markup)
    

def mood(update: Updater, context: CallbackContext):
    """Обработка ответа пользователя на вопрос о настроении"""
    user = update.effective_user
    query = update.callback_query
    
    histoy[user.id].append({'answer': query.data, 'date': datetime.now()})
    
    query.edit_message_text(
        text="Спасибо, {}! Ваше настроение на: {}".format(user.first_name, query.data)
    )
    

def schedule_checker():
    """Обработка задач из модуля schedule.
    
        Проверяем, есть ли задачи, которые нужно выполнить
    """
    while True:
        schedule.run_pending()
        time.sleep(1)
    

def main():
    mybot = Updater(TOKEN, use_context=True)
    
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", start_user))
    dp.add_handler(CallbackQueryHandler(mood))
    
    def send_mood():
        """Рассылка всем пользователям, вопроса о настроении."""
        for user in users:
            dp.bot.sendMessage(chat_id=user, text="Как твое настроение?", reply_markup=InlineKeyboardMarkup(keyboard))
    
    def send_you_best():
        """Рассылка всем пользователм, подбадривающего сообщения."""
        phrases = [
            'Марковка полна каротином, шпинат полон кальцеем, а твое настроение полно позитивом!',
            'Ты сегодня великолепен!',
            'Ты сегодня прекрасен!',
            'Ты сегодня замечательен!',
            'Тебе просили передать: Ты должен быть обнять!',
            'Это палочка ➖, а это галочка ✅ , в графе что ты лапочка!',
        ]
        for user in users:
            dp.bot.sendMessage(chat_id=user, text=random.choice(phrases))
    
    # schedule.every().day.at("17:56").do(send_mood)
    schedule.every(10).seconds.do(send_you_best)
    Thread(target=schedule_checker).start()

    print("Бот стартовал")
    mybot.start_polling()
    mybot.idle()


if __name__ == "__main__":
    main()
