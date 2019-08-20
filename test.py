# !/usr/bin/env python
# coding=utf-8
import telebot
from telebot.types import LabeledPrice
from telebot.types import ShippingOption

# https://github.com/eternnoir/pyTelegramBotAPI/blob/master/examples/payments_example.py
# https://github.com/python-telegram-bot/python-telegram-bot/blob/master/examples/paymentbot.py

# bot = TeleBot('638688358:AAEVbQXx7VYTaHGEOZS-f_mgQTkCgbCSD8M')
# bot = TeleBot('454102540:AAF7Bsw96abzv80FK2-NQf8PVRPFfini_vU')

token = '454102540:AAF7Bsw96abzv80FK2-NQf8PVRPFfini_vU'
# provider_token = '410694247:TEST:798de6fb-c387-4adc-8934-87851820b7a3'  # @BotFather -> Bot Settings -> Payments
provider_token = '390540012:LIVE:4167'  # @BotFather -> Bot Settings -> Payments 390540012:LIVE:4167
bot = telebot.TeleBot(token)

# More about Payments: https://core.telegram.org/bots/payments


# LabeledPrice = [{'label': 'ru', 'amount': 150}]
# prices = [LabeledPrice(label='Working Time Machine', amount=1000), LabeledPrice('Gift wrapping', 500)]
prices = [LabeledPrice(label='Working Time Machine', amount=6000)]

# shipping_options = [
#     ShippingOption(id='instant', title='WorldWide Teleporter').add_price(LabeledPrice('Teleporter', 1000)),
#     ShippingOption(id='pickup', title='Local pickup').add_price(LabeledPrice('Pickup', 300))]


a = ShippingOption(id='instant', title='WorldWide Teleporter')
a.add_price(LabeledPrice('Teleporter', 1000))
b = ShippingOption(id='pickup', title='Local pickup')
b.add_price(LabeledPrice('Pickup', 300))
shipping_options = [a, b]
print(shipping_options)
# b =
# print(a.to_json())

@bot.message_handler(commands=['start'])
def command_start(message):
    bot.send_message(message.chat.id,
                     "Hello, I'm the demo merchant bot."
                     " I can sell you a Time Machine."
                     " Use /buy to order one, /terms for Terms and Conditions")


@bot.message_handler(commands=['terms'])
def command_terms(message):
    bot.send_message(message.chat.id,
                     'Thank you for shopping with our demo bot. We hope you like your new time machine!\n'
                     '1. If your time machine was not delivered on time, please rethink your concept of time and try again.\n'
                     '2. If you find that your time machine is not working, kindly contact our future service workshops on Trappist-1e.'
                     ' They will be accessible anywhere between May 2075 and November 4000 C.E.\n'
                     '3. If you would like a refund, kindly apply for one yesterday and we will have sent it to you immediately.')


@bot.message_handler(commands=['buy'])
def command_pay(message):
    bot.send_message(message.chat.id,
                     "Real cards won't work with me, no money will be debited from your account."
                     " Use this test card number to pay for your Time Machine: `4242 4242 4242 4242`"
                     "\n\nThis is your demo invoice:", parse_mode='Markdown')
    bot.send_invoice(message.chat.id, title='Working Time Machine',
                     description='Want to visit your great-great-great-grandparents?'
                                 ' Make a fortune at the races?'
                                 ' Shake hands with Hammurabi and take a stroll in the Hanging Gardens?'
                                 ' Order our Working Time Machine today!',
                     provider_token=provider_token,
                     currency='RUB',
                     photo_url='http://erkelzaar.tsudao.com/models/perrotta/TIME_MACHINE.jpg',
                     photo_height=512,  # !=0/None or picture won't be shown
                     photo_width=512,
                     photo_size=512,
                     is_flexible=False,  # True If you need to set up Shipping Fee
                     prices=prices,
                     start_parameter='time-machine-example',
                     invoice_payload='HAPPY FRIDAYS COUPON')


@bot.shipping_query_handler(func=lambda query: True)
def shipping(shipping_query):
    print(shipping_query)
    bot.answer_shipping_query(shipping_query.id, ok=True, shipping_options=shipping_options,
                              error_message='Oh, seems like our Dog couriers are having a lunch right now. Try again later!')


@bot.pre_checkout_query_handler(func=lambda query: True)
def checkout(pre_checkout_query):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True,
                                  error_message="Aliens tried to steal your card's CVV, but we successfully protected your credentials,"
                                                " try to pay again in a few minutes, we need a small rest.")


@bot.message_handler(content_types=['successful_payment'])
def got_payment(message):
    bot.send_message(message.chat.id,
                     'Hoooooray! Thanks for payment! We will proceed your order for `{} {}` as fast as possible! '
                     'Stay in touch.\n\nUse /buy again to get a Time Machine for your friend!'.format(
                         message.successful_payment.total_amount / 100, message.successful_payment.currency),
                     parse_mode='Markdown')



@bot.message_handler(content_types=["text"])
def textc(message):
    print(message)



@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
            if call.message:
                # main menu
                if call.data[:3] == "a: ":
                    print('ok')
    except Exception as e:
        print(e)
#
# a = {5:{'index': 1}}
#
# a[5].update(c='Ул. Влажная, 9')
# print(a)
#
# a[5].update(c='Маячная 5 кв 1')
# print(a)
#
bot.skip_pending = True
bot.polling(none_stop=True, interval=0)

#
# @bot.message_handler(commands=["start"])
# def start_main_menu(message):
#     am = 5
#     print('message', message)
#     bot.send_invoice(
#         chat_id=message.chat.id,
#         title='Оплатить заказ',
#         description='Описание',
#         invoice_payload="Custom-Payload",
#         provider_token='381764678:TEST:6558',
#         start_parameter="test-payment",
#         currency='RUB',
#         prices=[types.LabeledPrice(label='Working Time Machine', amount=13000*am)],
#         need_name=False, need_phone_number=False,
#         need_email=False, need_shipping_address=False,
#         is_flexible=False)
#     # print(types.Update.pre_checkout_query)
#
#
#
#
# # types.ShippingOption(id='pickup', title='Local pickup').add_price(types.LabeledPrice('Pickup', 300))
#
#
# @bot.shipping_query_handler(func=lambda query: True)
# def shipping(shipping_query):
#     shipping_options = [types.ShippingOption(id='instant', title='WorldWide Teleporter').
#                             add_price(types.LabeledPrice('Teleporter', 1000)),
#                         types.ShippingOption(id='pickup', title='Local pickup').add_price(
#                             types.LabeledPrice('Pickup', 300))]
#     print('shipping_query', shipping_query)
#     options = list()
#     # a single LabeledPrice
#     # a = [types.LabeledPrice('A', 100)]
#     types.ShippingOption(id='1', title='Shipping Option A').\
#         add_price(types.LabeledPrice(label='Teleporter', amount=1000))
#     # # an array of LabeledPrice objects
#     price_list = [types.LabeledPrice(label='B1', amount=150),
#                   types.LabeledPrice(label='B2', amount=200)]
#     print('price_listr', price_list)
#     options.append(types.ShippingOption(id='2', title='Shipping Option B').
#                    add_price(price_list))
#     options.append(types.ShippingOption.to_json())
#     # u = types.ShippingOption()
#     print('shipping_options', shipping_options)
#     print('options', options)
#     bot.answer_shipping_query(shipping_query_id=shipping_query.id, ok=True,
#                               shipping_options=options)
#     # bot.answer_shipping_query(shipping_query.id, ok=True, shipping_options=shipping_query.shipping_address,
#     #                           error_message='Oh, seems like our Dog couriers are having a lunch right now. Try again later!')
#
#
# # @bot.pre_checkout_query_handler()
# # @bot.add_pre_checkout_query_handler()
#
#
#
#
# @bot.pre_checkout_query_handler(func=lambda query: True)
# def checkout(pre_checkout_query):
#     bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True,
#                                   error_message="Aliens tried to steal your card's CVV, but we successfully protected your credentials,"
#                                                 " try to pay again in a few minutes, we need a small rest.")
#
#
# @bot.message_handler(content_types=['successful_payment'])
# def got_payment(message):
#     bot.send_message(message.chat.id,
#                      'Hoooooray! Thanks for payment! We will proceed your order for `{} {}` as fast as possible! '
#                      'Stay in touch.\n\nUse /buy again to get a Time Machine for your friend!'.format(
#                          message.successful_payment.total_amount / 100, message.successful_payment.currency),
#                      parse_mode='Markdown')
#
#
#
# @bot.pre_checkout_query_handler(func=lambda query: True)
# def PreCheckoutQueryHandler(pre_checkout_query):
#         print(';;;;;')
#         print()
#         # query = message.pre_checkout_query
#         print(pre_checkout_query)
#         # check the payload, is this from your bot?
#         # if query.invoice_payload != 'Custom-Payload':
#         #     # answer False pre_checkout_query
#         #     bot.answer_pre_checkout_query(pre_checkout_query_id=query.id, ok=False,
#         #                                   error_message="Something went wrong...")
#         # else:
#         #     bot.answer_pre_checkout_query(pre_checkout_query_id=query.id, ok=True)
#
#
# # finally, after contacting to the payment provider...
# # @bot.pre_checkout_query_handler(func=lambda query: True)
# # def successful_payment_callback(bot, update):
# #     # do something after successful receive of payment?
# #     update.message.reply_text("Thank you for your payment!")
# #
#
# @bot.message_handler(content_types=["text"])
# def build_menu(update):
#     print(update)
#
#
# if __name__ == '__main__':
#     bot.polling(none_stop=True)


# import requests, json

# users = [226665834, 507185981, 167315364, 70025022, 34436430, 108794197, 282580371, 259855747, 352074606, 400738456, 61140744, 27390261, 65472004]
# users = [226665834]
# {'id': 507185981, 'is_bot': False, 'first_name': 'Свежая Вода. Доставка.', 'username': 'proektSV19'}
# def report(msg):
#     for user in users:
#         send_message(user, msg)
#
# butt = {}
# def send_message(chat_id, text):
#     try:
#         but = requests.get("https://api.telegram.org/bot638688358:AAEVbQXx7VYTaHGEOZS-f_mgQTkCgbCSD8M/sendMessage",
#                      params={"chat_id": chat_id, "text": text})
#         butt.update({chat_id: {'message_id': json.loads(but.content.decode('utf8')).get('result').get('message_id')}})
#         print(butt)
#     except requests.HTTPError as e:
#         print('ERROR')
#
#
# def editMessageText(chat_id, message_id, text):
#     try:
#         requests.get("https://api.telegram.org/bot638688358:AAEVbQXx7VYTaHGEOZS-f_mgQTkCgbCSD8M/editMessageText",
#                      params={"chat_id": chat_id, "message_id": message_id, "text": text})
#     except requests.HTTPError as e:
#         print('ERROR')
#
#
#
# send_message(users[0], 'ID пользователя: 226665834\n '
#                        'Имя: Gadjimurad\n'
#                        'Номер: +79673910682\n'
#                        'Место доставки: test\n'
#                        'Коментарий: None\n\n'
#                        'Товар: вода\n'
#                        'Количество бутылок: 2\n'
#                        'Сумма: 300 руб.')

#
# import time
# time.sleep(31)
# editMessageText(users[0], butt[users[0]].get('message_id'),
#                 'ID пользователя: 226665834\n '
#                 'Имя: Gadjimurad\n'
#                 'Номер: +79673910682\n'
#                 'Место доставки: test\n'
#                 'Коментарий: ok\n\n'
#                 'Товар: вода\n'
#                 'Количество бутылок: 2\n'
#                 'Сумма: 300 руб.')
# # editMessageText(users[0], message_id, text)
# chat_id, message_id, text

#
# a = 'ID пользователя: 226665834\n' \
#     'Имя: Gadjimurad\n' \
#     'Номер: +79673910682\n' \
#     'Место доставки: test\n\n' \
#     'Товар: вода\n' \
#     'Количество бутылок: 2\n' \
#     'Сумма: 300 руб.\n'
#
# import json
# b = 'Коментарий: ok'
# c =  a + b
# # print(c)
#
# print(c)
#
# # print(b)
# #
# # a.join(b)
# # print(a)


# Модернизация для
# if phone_number[0] != '+':
#     phone_number = '+' + phone_number
# try:
#     bot.delete_message(telegram, users[telegram].get('mess_id'))
# except Exception as e:
#     print('error', e)