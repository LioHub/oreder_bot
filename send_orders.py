import requests
import json
users = []

user_mes = {}

def report(msg):
    for user in users:
        send_message(user, msg)


def report_about_paid(msg):
    for user in users:
        notic_about_payment(user, msg)


def edit_report(msg):
    for user in users:
        editMessageText(user, msg)


def send_message(chat_id, text):
    try:
        mes_id = requests.get("https://api.telegram.org/bot638688358:AAEVbQXx7VYTaHGEOZS-f_mgQTkCgbCSD8M/sendMessage",
                     params={"chat_id": chat_id, "text": text})
        try:
            user_mes.update({chat_id: {'message_id': json.loads(mes_id.content.decode('utf8')).get('result').get('message_id')}})
        except Exception as e:
            print('ERROR')
        print(mes_id)
    except requests.HTTPError as e:
        print('ERROR')


def editMessageText(chat_id, text):
    try:
        message_id = user_mes[chat_id].get('message_id')
        try:
            user_mes.pop(chat_id)
        except Exception as e:
            print(e)
        requests.get("https://api.telegram.org/bot638688358:AAEVbQXx7VYTaHGEOZS-f_mgQTkCgbCSD8M/editMessageText",
                     params={"chat_id": chat_id, "message_id": message_id, "text": text})
    except requests.HTTPError as e:
        print('ERROR')


def notic_about_payment(chat_id, text):
    try:
        requests.get("https://api.telegram.org/bot638688358:AAEVbQXx7VYTaHGEOZS-f_mgQTkCgbCSD8M/sendMessage",
                     params={"chat_id": chat_id, "text": text})
    except requests.HTTPError as e:
        print('ERROR')
# chat_id, message_id, text