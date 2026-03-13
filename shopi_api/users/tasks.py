from celery import shared_task
from time import sleep
from datetime import datetime
import smtplib

@shared_task
def add(x, y):
    sleep(10)
    print(x + y)
    return "OK"

@shared_task
def show_time():
    print("Текущее время:", datetime.now())   

@shared_task
def send_test_email():
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login("example@gmail.com", "password")

    message = "Subject: Test\n\nHello from Celery"
    server.sendmail("example@gmail.com", "user@gmail.com", message)

    server.quit()
    return "Email sent"