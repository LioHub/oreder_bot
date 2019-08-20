#!/usr/bin/env python
# coding=utf-8

from db import connect_mysql
from dictionary import menu, provider_token, prices
from words import *
import button
import bitrix24
import time

all_rows = 0

# Обновление кнопок
def reply_message(bot, telegram, message_id, text, index):
    bot.edit_message_text(chat_id=telegram, message_id=message_id, text=text,
                          reply_markup=menu[index].get('button'), parse_mode='HTML')
    check_connect()
    where = 'telegram = %s' % telegram
    connect_mysql.update('menu', where, **{'message_id': message_id,
                                           'text': text, 'index': index})


# Уведомить о разных случаях
def notification(bot, call_id, text):
    bot.answer_callback_query(call_id, text=text)


# Удалить меню
def del_menu(bot, chat_id, message_id):
    return bot.delete_message(chat_id=chat_id, message_id=message_id)


# Показ результата в виде окошки
def alert(bot, call_id, text):
    bot.answer_callback_query(call_id, show_alert=True, text=text)


# Отправить меню
def send_menu(bot, chat_id, text, index):
    check_connect()
    message_id = bot.send_message(chat_id, text, reply_markup=menu[index].get('button'), parse_mode='HTML')
    where = 'telegram = %s' % chat_id
    connect_mysql.update('menu', where, **{'message_id': message_id.message_id, 'text': text, 'index': index})


# Отправить меню
def send_photo(bot, chat_id, photo, text, index):
    check_connect()
    message_id = bot.send_photo(chat_id, photo, text, reply_markup=menu[index].get('button'))
    where = 'telegram = %s' % chat_id
    connect_mysql.update('menu', where, **{'message_id': message_id.message_id, 'text': text, 'index': index})


def edit_caption_of_photo(bot, caption, telegram, message_id, index):
    bot.edit_message_caption(caption, telegram, message_id, reply_markup=menu[index].get('button'))


# Проверка подключения к бд
def check_connect():
    try:
        where = 'telegram = %s' % 12345
        menu = connect_mysql.select('users', where, *['telegram'])
    except Exception as e:
        print('e %s' % e)
        connect_mysql.open()
    return True


def check_user(telegram):
    check_connect()
    where = 'telegram = %s' % telegram
    return connect_mysql.select('users', where, *['telegram'])


def select_menu(telegram):
    check_connect()
    where = 'telegram = %s' % telegram
    return connect_mysql.select('menu', where, *['telegram', 'message_id', 'text', 'index'])


def insert_menu(telegram):
    check_connect()
    connect_mysql.insert('menu', **{'telegram': telegram})


def update_menu(telegram, message_id, greetings, index):
    check_connect()
    where = 'telegram = %s' % telegram
    connect_mysql.update('menu', where, **{'message_id': message_id,
                                           'text': greetings, 'index': index})


def select_user(telegram):
    check_connect()
    where = 'telegram = %s' % telegram
    return connect_mysql.select('users', where, *['telegram', 'name', 'phone'])


def select_list_of_users():
    check_connect()
    return connect_mysql.select_all_for_count_row('users', *['id', 'telegram'])


def insert_order(**kwargs):
    check_connect()
    connect_mysql.insert('basket', **kwargs)


def select_orders(telegram):
    check_connect()
    where = 'telegram = %s ORDER BY order_number DESC LIMIT 10;' % (telegram)
    return connect_mysql.select_all('basket', where, *['order_number', 'telegram', 'name', 'phone', 'goods',
                                                       'amount', 'sum', 'deal_id', 'status', 'street', 'added'])


def select_active_orders(telegram):
    check_connect()
    # where = """telegram = %s and status = "PREPARATION" or status = 'NEW' or status = 'PREPAYMENT_INVOICE' or
    # status = 'EXECUTING' or status = 'FINAL_INVOICE'
    # ORDER BY order_number DESC LIMIT 10;""" % (telegram)
    # 1 NEW
    # 2 PREPARATION
    # 3 PREPAYMENT_INVOICE
    # 4 EXECUTING
    # 5 FINAL_INVOICE
    where = """telegram = %s and status = '1' or status = 'NEW';""" % (telegram)
    return connect_mysql.select_all('basket', where, *['order_number', 'telegram', 'name', 'phone', 'goods',
                                                       'amount', 'sum', 'deal_id', 'status', 'street', 'added'])


def delete_the_order(order_number):
    check_connect()
    where = 'order_number = %s' % order_number
    return connect_mysql.delete('basket', where)


def select_all_orders():
    return connect_mysql.select_all('basket', *['', 'order_number', 'telegram', 'name', 'phone', 'goods',
                                                'amount', 'sum', 'street'])


def check_order(telegram, order_number):
    check_connect()
    where = 'telegram = %s and order_number = %s' % (telegram, order_number)
    return connect_mysql.select_all('basket', where, *['order_number'])


def add_package(**kwargs):
    check_connect()
    return connect_mysql.insert('packages', **kwargs)


def select_last_street(telegram):
    check_connect()
    water = "'water'"
    where = 'telegram = %s and goods = %s ORDER BY order_number DESC LIMIT 1;' % (telegram, water)
    return connect_mysql.select('basket', where, *['order_number', 'telegram', 'name', 'phone', 'goods',
                                                   'amount', 'sum', 'street'])


def for_street_menu(bot, telegram, street, where, index):
    check_connect()
    print('street %s ' % street)
    if street == []:
        message_id = bot.send_message(telegram, LOCATION, reply_markup=button.inline_location_menu(where),
                                      parse_mode='HTML')
    else:
        message_id = bot.send_message(telegram, LOCATION, reply_markup=
        button.inline_location_menu2(street.get('street'), where), parse_mode='HTML')

    where = 'telegram = %s' % telegram
    connect_mysql.update('menu', where, **{'message_id': message_id.message_id, 'text': LOCATION, 'index': index})


def just_send_mes(bot, telegram, text):
    bot.send_message(telegram, text, parse_mode='HTML')


# Добавление делки
def pre_add_deal(name, contact_id, price):
    # Для добавления новой сделки
    data = {'fields': {
        "TITLE": name,
        "TYPE_ID": "GOODS",
        "STAGE_ID": "NEW",
        "COMPANY_ID": 1,
        # "CONTACT_ID": +79635896583,
        "CONTACT_ID": contact_id,
        "OPENED": "YES",
        "ASSIGNED_BY_ID": 1,
        "PROBABILITY": 100,
        "CURRENCY_ID": "RUB",
        "OPPORTUNITY": price,
        "BEGINDATE": time.time()
    },
        'params': {"REGISTER_SONET_EVENT": "Y"}}
    result = bitrix24.add_deal(data)
    # save deal_id


# Добавление контактов
def pre_add_contact(first_name, second_name, last_name, phone):
    data = {'fields': {
        "NAME": first_name,
        "SECOND_NAME": second_name,
        "LAST_NAME": last_name,
        "OPENED": "YES",
        "ASSIGNED_BY_ID": 1,
        "TYPE_ID": "CLIENT",
        # "SOURCE_ID": "SELF",
        "COMMENTS": "FROM TELEGRAM",
        "DATE_CREATE": time.time(),
        "COMPANY_ID"
        "PHONE": [{"VALUE": phone, "VALUE_TYPE": "WORK"}]
    },
        'params': {"REGISTER_SONET_EVENT": "Y"}}
    result = bitrix24.add_contact(data)
    # save deal_id


# # Для проверки контакта на exist
# def checkout_contact(contact):
#     results = bitrix24.get_contact_list(contact)
#     print(results)
#     if results == []:
#         print(False)
#     else:
#         print(True)

def add_contactID_to_db(telegram, contact_id):
    check_connect()
    where = 'telegram = %s' % telegram
    connect_mysql.update('users', where, **{'contact_id': contact_id})


def select_contactID(telegram):
    check_connect()
    where = 'telegram = %s' % telegram
    return connect_mysql.select('users', where, *['contact_id']).get('contact_id')


def check_contact_and_get(telegram):
    print('into check_contact_and_get')
    contact_id = select_contactID(telegram)
    print('contact_id', contact_id)
    if contact_id == None:
        user = select_user(telegram)
        print('user', user)
        contact_list = bitrix24.get_contact_list(user.get('phone'))
        print('contact_list', contact_list)
        if contact_list == []:
            contact_id = bitrix24.add_contact(user.get('name'), None, None, user.get('phone'))
            print('contact_id', contact_id)
            print(contact_id.get('result'))
            add_contactID_to_db(telegram, contact_id.get('result'))
            return contact_id.get('result')
        else:
            # result = bitrix24.get_contact_list(user.get('phone'))
            print(contact_list[0].get('ID'))
            add_contactID_to_db(telegram, contact_list[0].get('ID'))
            return contact_list[0].get('ID')
    else:
        return contact_id


def check_state_of_deal(active_orders):
    # 'order_number', 'telegram', 'name', 'phone', 'goods',
    # 'amount', 'sum', 'deal_id', 'status', 'street', 'added'
    print('active_orders', active_orders)
    print('______________________________')
    for active_order in active_orders:
        print('active_order', active_order)
        result = bitrix24.get_deal_state({'id': active_order.get('deal_id')})
        print('______________________________')
        print('result', result)
        try:
            print('status', active_order.get('status'))
            print('STAGE_ID', result.get('result').get('STAGE_ID'))
            print(result.get('result').get('STAGE_ID') != active_order.get('status'))
            if result.get('result').get('STAGE_ID') != active_order.get('status'):
                where = 'order_number = %s' % active_order.get('order_number')
                print('where', where)
                connect_mysql.update('basket', where, **{'status': result.get('result').get('STAGE_ID')})
        except Exception as e:
            where = 'telegram = %s' % active_order.get('telegram')
            connect_mysql.update('basket', where, **{'status': 'WON'})
    return


def invoice(bot, telegram):
    price = prices[telegram]
    print('__________________________')
    print('price', price)
    print('type(price)', type(price))
    print('__________________________')
    bot.send_invoice(telegram, title='SV',
                     description=PAYMENT_WARRING,
                     provider_token=provider_token,
                     currency='RUB',
                     # photo_url='http://erkelzaar.tsudao.com/models/perrotta/TIME_MACHINE.jpg',
                     # photo_height=512,  # !=0/None or picture won't be shown
                     # photo_width=512,
                     # photo_size=512,
                     is_flexible=False,  # True If you need to set up Shipping Fee
                     prices=price,
                     start_parameter='time-machine-example',
                     invoice_payload='HAPPY FRIDAYS COUPON')