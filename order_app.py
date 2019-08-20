#!/usr/bin/env python
# coding=utf-8

from telebot import TeleBot, types
from telebot.types import LabeledPrice
from telebot.types import ShippingOption

import views
from core import order_water
from core import basket
from core import admin_panel
from core import instruction
from core import back_to_main_menu
from core import builder_menu
from core import main_menu
from core import take_contact
from core import check_answer
from core import cancel_the_order
from core import show_orders
from core import confirm_delivery
from core import pack_three_months
from core import pack_six_months
from core import pack_1_year
from core import order_pompa
from core import no_need_pompa
from core import plus_of_pompa
from core import minus_of_pompa
from core import to_order_pompa
import core
import time
from dictionary import prices
from flask import Flask, request

# Testbot
# token = ''
# bot = TeleBot(token)


# bot = TeleBot('')

# SV19bot
token = ''
bot = TeleBot(token)
#
# WEBHOOK_HOST = ''
# WEBHOOK_PORT = 8443  # 443, 80, 88 или 8443 (порт должен быть открыт!)
# LOCAL_PORT = 9001  #
# LOCAL_LISTEN = '127.0.0.1'
# WEBHOOK_LISTEN = ''
#
# # WEBHOOK_SSL_CERT = '/root/ssl/webhook_cert.pem'  # Путь к сертификату
# WEBHOOK_SSL_CERT = '/home/iman/ssl/webhook_pkey.pem'  # Путь к сертификату

#
# WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
# LOCAL_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, LOCAL_PORT)
# WEBHOOK_URL_PATH = "/%s/" % token

#
# bot = TeleBot(token)
#
# app = Flask(__name__)
#
#
# @app.route(WEBHOOK_URL_PATH, methods=['POST'])
# def webhook():
#     update = types.Update.de_json(request.get_json(force=True))
#     bot.process_new_updates([update])
#     return ''



@bot.message_handler(commands=["start"])
def start_main_menu(message):
    main_menu(bot, message.chat.id, message.from_user.first_name)


# Ввод контактов
@bot.message_handler(content_types=["contact"])
def contact(message):
    # 'first_name': 'Gadjimurad', 'username': 'strongmuslim', 'last_name': 'Bagatyrov',
    take_contact(bot, message.chat.id, message.from_user.first_name, message.from_user.username,
                 message.from_user.last_name, message.contact.phone_number)


user_time = {}


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        telegram = call.message.chat.id
        message_id = call.message.message_id
        try:
            user_time[telegram].get('last_time')
        except Exception as e:
            user_time.update({telegram: {'last_time': time.time(), 'first_time': True}})
            print(e)
        if user_time[telegram].get('last_time') < (time.time() - 1) or user_time[telegram].get('first_time'):
            if call.message:
                user_time.update({telegram: {'last_time': time.time(), 'first_time': False}})
                # main menu
                if call.data[:7] == "start: ":
                    if call.data[7:] == 'order_water':
                        order_water(bot, telegram)
                    elif call.data[7:] == 'basket':
                        basket(bot, telegram, message_id)
                    elif call.data[7:] == 'admin_panel':
                        admin_panel(bot, telegram)
                    elif call.data[7:] == 'instruction':
                        instruction(bot, telegram)

                if call.data[:6] == 'back: ':
                    if call.data[6:] == 'to_packages':
                        core.want_to_economize(bot, telegram)
                    elif call.data[6:] == 'to_show_pack_bottle':
                        core.show_pack_bottle(bot, telegram)
                    elif call.data[6:] == "back_to_main_menu":
                        # back_to_main_menu(bot, telegram, message_id, call.id)
                        print(1)
                        core.back_to_main_menu_del(bot, telegram)
                    # back_to_main_menu_with_del button
                    elif call.data[6:] == "back_to_main_menu_del":
                        core.back_to_main_menu_del(bot, telegram)
                    elif call.data[6:] == "pompa_ques":
                        core.to_order_bottles(bot, telegram)
                    elif call.data[6:] == "back_to_show_bottles":
                        core.show_selected_bottles(bot, telegram)
                # order menu
                elif call.data[:7] == "order: ":
                    if call.data[7:] == 'minus':
                        core.minus_of_bottle(bot, telegram, call.id)
                    elif call.data[7:] == 'select':
                        core.to_order_bottles(bot, telegram)
                    elif call.data[7:] == 'plus':
                        core.plus_of_bottle(bot, telegram)
                    elif call.data[7:] == 'input':
                        core.cin_other_water(bot, telegram, message_id, call.id)
                # confirm menu
                elif call.data[:9] == "confirm: ":
                    if call.data[9:] == 'confirm':
                        core.confirm(bot, telegram, call.id)
                    if call.data[9:] == 'change_adress':
                        core.change_adress(bot, telegram, "show_confirm", 0)
                    if call.data[9:] == 'want_to_economize':
                        core.want_to_economize(bot, telegram)
                # basket menu cancel_the_order
                elif call.data[:8] == "basket: ":
                    if call.data[8:] == 'replay_order':
                        core.replay_order(bot, telegram)
                    elif call.data[8:] == 'cancel_the_order':
                        cancel_the_order(bot, telegram, call.id)

                elif call.data[:8] == "replay: ":
                    if call.data[8:] == 'confirm':
                        core.confirm(bot, telegram, call.id)
                    elif call.data[8:] == 'skip':
                        # core.skip_comment(bot, telegram, call.id)
                        core.back_to_main_menu_del(bot, telegram)
                # basket menu
                elif call.data[:10] == "location: ":
                    if call.data[10:16] == 'street':
                        print('before error', call.data)
                        core.set_street(bot, telegram)
                        # core.set_street(bot, telegram, str(call.data[17:]))

                    elif call.data[10:] == 'back_to_order':
                        core.show_selected_bottles(bot, telegram)
                        # core.to_order_bottles(bot, telegram, call.id)
                    elif call.data[10:] == 'back_to_confirm_package' or call.data[10:] == 'confirm_pack':
                        print('here')
                        core.show_confirm_pack_bottle(bot, telegram, False)
                    elif call.data[10:] == "show_confirm":
                        core.confirm_menu(bot, telegram)
                    elif call.data[10:] == "show_pompa":
                        core.show_pompa_confirm(bot, telegram)
                    elif call.data[10:] == "order_package":
                        core.show_pack_bottle(bot, telegram)
                # instruction menu
                elif call.data[:13] == "instruction: ":
                    if call.data[13:] == 'about_water':
                        core.about_water(bot, telegram)

                    elif call.data[13:] == 'about_company':
                        core.about_company(bot, telegram)


               # instruction menu

                elif call.data[:7] == "admin: ":
                    if call.data[7:] == 'orders':
                        show_orders(bot, telegram, message_id, call.id)

                    elif call.data[7:] == 'confirm_delivery':
                        confirm_delivery(bot, telegram, message_id, call.id)
                # pompa menu
                elif call.data[:7] == "pompa: ":
                    if call.data[7:] == 'order_pompa':
                        order_pompa(bot, telegram)

                    if call.data[7:] == 'no_need':
                        no_need_pompa(bot, telegram, message_id, call.id)

                    if call.data[7:] == 'back_to_water':
                        core.show_selected_bottles(bot, telegram)

                    if call.data[7:] == 'minus':
                        minus_of_pompa(bot, telegram, call.id)

                    elif call.data[7:] == 'select':
                        to_order_pompa(bot, telegram)

                    elif call.data[7:] == 'plus':
                        plus_of_pompa(bot, telegram)

                    elif call.data[7:] == 'input':
                        order_pompa(bot, telegram)

                elif call.data[:9] == "package: ":
                    if call.data[9:] == '3_months':
                        pack_three_months(bot, telegram)
                    if call.data[9:] == '6_months':
                        pack_six_months(bot, telegram)
                    if call.data[9:] == '1_year':
                        pack_1_year(bot, telegram)
                    if call.data[9:] == 'back_to_confirm_order':
                        core.confirm_menu(bot, telegram, False)
                    if call.data[9:] == 'to_order_package':
                        core.to_order_package(bot, telegram)
                    if call.data[9:] == 'minus_of_pack_bottle':
                        core.minus_of_pack_bottle(bot, telegram, call.id)
                    if call.data[9:] == 'plus_of_pack_bottle':
                        core.plus_of_pack_bottle(bot, telegram)
                    if call.data[9:] == 'change_the_quantity':
                        core.change_the_quantity(bot, telegram)

                elif call.data[:17] == "confirm_package: ":
                    if call.data[17:] == "change_adress_pack":
                        # core.change_adress_pack(bot, telegram)
                        core.change_adress(bot, telegram, "confirm_pack", 26)

                    elif call.data[17:] == "confirm_pack_add_to_db":
                        core.confirm_pack_add_to_db(bot, telegram, call.id)

                elif call.data[:9] == "bottles: ":
                    if call.data[9:] == "1":
                        core.set_bottles(bot, telegram, 1)
                    elif call.data[9:] == "2":
                        core.set_bottles(bot, telegram, 2)
                    elif call.data[9:] == "3":
                        core.set_bottles(bot, telegram, 3)
                    elif call.data[9:] == "4":
                        core.set_bottles(bot, telegram, 4)
                    elif call.data[9:] == "5":
                        core.set_bottles(bot, telegram, 5)
                    elif call.data[9:] == "economize":
                        core.economize(bot, telegram)
                    elif call.data[9:] == "back_to_confirm_order":
                        core.order_water(bot, telegram)

                elif call.data[:7] == "pomps: ":
                    if call.data[7:] == "1":
                        core.set_pomps(bot, telegram, 1)
                    elif call.data[7:] == "2":
                        core.set_pomps(bot, telegram, 2)
                    elif call.data[7:] == "3":
                        core.set_pomps(bot, telegram, 3)

                elif call.data[:9] == "payment: ":
                    if call.data[9:] == "pay_menu":
                        core.pay_menu(bot, telegram)
                    elif call.data[9:] == "yandex":
                        core.yandex_payment(bot, telegram)
                    elif call.data[9:] == "cash":
                        core.cash_payment(bot, telegram)
                    elif call.data[9:] == 'wish':
                        core.leave_wishes(bot, telegram)
                    elif call.data[9:] == 'skip':
                        core.skip(bot, telegram)

    except Exception as e:
        print(e)
        # menu = views.select_menu(call.message.chat.id)
        # try:
        #     views.del_menu(bot, menu.get('telegram'),
        #          menu.get('message_id'))
        # except KeyError as e:
        #     print(e)
        # views.send_menu(bot, call.message.chat.id, 'Главное меню', 1)


@bot.message_handler(content_types=["photo"])
def photos(message):
    try:
        print(message.photo[0].file_id)
    except Exception as e:
        print(e)
    builder_menu(bot, message.chat.id)


@bot.message_handler(content_types=['document', 'audio'])
def audio(message):
    print('audio')
    builder_menu(bot, message.chat.id)


# @bot.message_handler(commands=['buy'])



@bot.pre_checkout_query_handler(func=lambda query: True)
def checkout(pre_checkout_query):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True,
                                  error_message="Aliens tried to steal your card's CVV, but we successfully protected your credentials,"
                                                " try to pay again in a few minutes, we need a small rest.")


@bot.message_handler(content_types=['successful_payment'])
def got_payment(message):
    # bot.send_message(message.chat.id,
    #                  'Hoooooray! Thanks for payment! We will proceed your order for `{} {}` as fast as possible! '
    #                  'Stay in touch.'.format(
    #                      message.successful_payment.total_amount / 100, message.successful_payment.currency),
    #                  parse_mode='Markdown')
    summa = message.successful_payment.total_amount / 100
    core.payment_success(bot, message.chat.id, summa)


@bot.message_handler(content_types=["text"])
def build_menu(message):
    try:
        check_answer(bot, message.chat.id, message.text)
    except Exception as e:
        print(e)

# bot.remove_webhook()

if __name__ == '__main__':
    bot.polling(none_stop=True)

#
#
#
# bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH,
#                 certificate=open(WEBHOOK_SSL_CERT, 'rb'))
#
# app.run(host=LOCAL_LISTEN, port=LOCAL_PORT, debug=True)