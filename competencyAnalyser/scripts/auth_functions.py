import telebot
from competencyAnalyser.config import BOT_TOKEN

from competencyAnalyser.scripts.verifyTheHash import \
    verify_telegram_authentication


def get_user_id(request: dict):
    return request["id"]


def check_authorized(request: dict):
    if "hash" in request.keys():
        return verify_telegram_authentication(request)
    return False


def get_params(data) -> dict:
    params = {"id": data["id"], "first_name": data["first_name"],
              "username": data["username"], "photo_url": data["photo_url"],
              "auth_date": data["auth_date"], "hash": data["hash"]}

    return params


bot = telebot.TeleBot(BOT_TOKEN)


def send_telegram_message(user_id: str, message: str):
    bot.send_message(user_id, message)
