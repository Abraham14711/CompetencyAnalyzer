#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import telebot
import os
import dotenv

dotenv.load_dotenv()

token = os.getenv("TELEGRAM_API_TOKEN")

bot = telebot.TeleBot(token)
webApp = telebot.types.WebAppInfo('https://competency.jobster.uz')


@bot.message_handler(commands=['start'])
def start_message(message):
    markup = telebot.types.InlineKeyboardMarkup()
    button = telebot.types.InlineKeyboardButton(
        text="Нажмите для открытия приложения",
        web_app=webApp
    )
    markup.add(button)
    bot.send_message(message.chat.id,
                     "Здравствуйте. Данный бот предназначен для "
                     "оценки ваших компетенций.\n"
                     "Правила использования бота:\n"
                     "1) Откройте webApp\n"
                     "2) Выберите вакансию, на которую вы хотите податься\n"
                     "3) Пройдите тест, чтобы узнать ваши компетенции.\n"
                     "Искусственный интеллект так же поможет подобрать "
                     "подходящие вакансии основываясь на ответах\n"
                     "4) Получите результат и персональные советы по развитию. "
                     "Письмо будет отправлено не только внутри приложения но и "
                     "на вашу почту.",
                     reply_markup=markup)


def main():
    bot.infinity_polling()
