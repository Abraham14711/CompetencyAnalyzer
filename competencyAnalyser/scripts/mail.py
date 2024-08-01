import smtplib
import os
from email.mime.text import MIMEText

from dotenv import load_dotenv


def send_email(userMail, user_data, message):
    load_dotenv()

    sender = "titikaka0097@gmail.com"
    password = os.getenv("EMAIL_PASSWORD")

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    server.login(sender, password)
    msg = MIMEText(f"{user_data['name']}, большое спасибо за прохождение теста."
                   f"\n Ваш результат:\n {message}")
    msg["Subject"] = "Результаты тестирования на Jobster"
    server.sendmail(sender, userMail, msg.as_string())
    server.quit()
