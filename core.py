#!/usr/bin/env python
# coding=utf-8

from views import notification
from views import reply_message
from views import del_menu
from views import send_menu
from views import check_connect
from views import check_user
from views import select_menu
from views import insert_menu
from views import update_menu
from views import send_photo
from views import alert
from views import select_user
from views import insert_order
from views import select_orders
from views import delete_the_order
from views import select_all_orders
from views import check_order
from views import edit_caption_of_photo
from views import add_package
from views import select_last_street
from views import for_street_menu
from telebot.types import LabeledPrice
from send_orders import report, edit_report, report_about_paid
from dictionary import menu, users, provider_token
from words import *
from db import connect_mysql
from button import contact_menu
import views
import time
import bitrix24
from dictionary import prices

def order_water(bot, telegram, index=7):
    user = select_user(telegram)
    try:
        users.update({telegram: {'index': index, 'name': user.get('name'), 'phone': user.get('phone')}})
    except Exception as e:
        return back_to_main_menu_del(bot, telegram)
    # reply_message(bot, telegram, select_menu(telegram).get('message_id'), HOW_MUCH, index)
    message_id = select_menu(telegram).get('message_id')
    send_menu(bot, telegram, HOW_MUCH, index)
    try:
        del_menu(bot, telegram, message_id)
    except Exception as e:
        print('error', e)
    return


def cin_other_water(bot, telegram, message_id, call_id):
    users.update({telegram: {'index': 25, 'message_id': message_id, 'call_id': call_id}})
    message_id = select_menu(telegram).get('message_id')
    send_menu(bot, telegram, HOW_MUCH, 25)
    try:
        del_menu(bot, telegram, message_id)
    except Exception as e:
        print('error', e)
    return


def basket(bot, telegram, message_id):
    active_orders = views.select_active_orders(telegram)
    views.check_state_of_deal(active_orders)
    # active_orders = views.select_active_orders(telegram)
    # print('active_orders', active_orders)
    orders = select_orders(telegram)
    message_id = select_menu(telegram).get('message_id')
    if orders == []:
        send_menu(bot, telegram, BAKEST_EMPTY, 11)
        try:
            del_menu(bot, telegram, message_id)
        except Exception as e:
            print('error', e)
        # reply_message(bot, telegram, message_id, BAKEST_EMPTY, 11)
    else:
        text = build_orders(orders[::-1])
        print('text -> %s' % text)
        # views.just_send_mes(bot, telegram, text)
        # 'Корзина'
        send_menu(bot, telegram, text, 1)
        try:
            del_menu(bot, telegram, message_id)
        except Exception as e:
            print('error', e)
    return


def build_orders(orders):
    text = ''
    # summa = 0
    max_orders = 10
    for order in orders:
        text += ORDER_NUMBER % order.get('order_number')
        if order.get('goods') == 'water':
            text += TYPE_OF_ORDER.format('Вода') + \
                    DATES_FOR_CONFIRM.format(order.get('name'), order.get('phone'), order.get('street')) + \
                    STATUS.format(status[order.get('status')]) + \
                    BOTTLES_FOR_BASKET.format(str(order.get('amount')), str(150), str(order.get('sum')), order.get('added'))
            # summa += order.get('amount') * 150
        if order.get('goods') == 'pompa':
            text += TYPE_OF_ORDER.format('Помпа') + \
                    DATES_FOR_CONFIRM.format(order.get('name'), order.get('phone'), order.get('street')) + \
                    STATUS.format(status[order.get('status')]) + \
                    POMPA_FOR_BASKET.format(order.get('amount'), 450, order.get('sum'), order.get('added'))
            # summa += order.get('amount') * 450
        if max_orders == 0:
            break
        max_orders -= 1
    # text += ITOG_CONFIRM.format(summa)
    return text


def admin_panel(bot, telegram):
    message_id = select_menu(telegram).get('message_id'),
    send_menu(bot, telegram, ADMIN_PANEL, 4)
    try:
        del_menu(bot, telegram, message_id)
    except Exception as e:
        print('error', e)
    return
    # reply_message(bot, telegram, select_menu(telegram).get('message_id'), ADMIN_PANEL, 4)


def instruction(bot, telegram):
    message_id = select_menu(telegram).get('message_id'),
    send_menu(bot, telegram, NEED_HELP, 5)
    try:
        del_menu(bot, telegram, message_id)
    except Exception as e:
        print('error', e)
    return
    # reply_message(bot, telegram, select_menu(telegram).get('message_id'), NEED_HELP, 5)


# start main menu
def main_menu(bot, telegram, first_name):
    if check_user(telegram) == []:
        message_id = bot.send_message(telegram, NEED_PHONE_NUMBER, reply_markup=contact_menu())
        users.update({telegram: {'mess_id': message_id.message_id}})
        return True
    else:
        user_menu = select_menu(telegram)
        if user_menu == []:
            insert_menu(telegram)
        else:
            try:
                del_menu(bot, user_menu.get('telegram'),
                         user_menu.get('message_id'))
            except Exception as e:
                print('error', e)
        try:
            # message_id = bot.send_message(telegram, GREETINS.format(first_name),
            #                               reply_markup=inline_main_menu())
            send_photo(bot, telegram, WATER_PHOTO, GREETINS.format(first_name), 1)
            # update_menu(telegram, message_id.message_id, GREETINS.format(first_name), 1)
        except Exception as e:
            print('error', e)


# the way to main menu
def back_to_main_menu_del(bot, telegram):
    message_id = select_menu(telegram).get('message_id')
    # send_menu(bot, telegram, MAIN_MENU, 1)
    try:
        users.pop(telegram)
    except Exception as e:
        print('error', e)
    send_photo(bot, telegram, WATER_PHOTO, MAIN_MENU, 1)
    try:
        del_menu(bot, telegram, message_id)
    except Exception as e:
        print('error', e)


# the way to main menu
def back_to_main_menu(bot, telegram, message_id, call_id):
    try:
        users.pop(telegram)
    except Exception as e:
        print('error', e)
    notification(bot, call_id, text=MAIN_MENU)
    reply_message(bot, telegram, message_id, MAIN_MENU, 1)


# save phone_number
def take_contact(bot, telegram, first_name, second_name, last_name, phone_number):
    text = GREETINS.format(first_name)
    # message_id = bot.send_message(telegram, text, reply_markup=menu[1].get('button'))
    message_id = bot.send_photo(telegram, WATER_PHOTO, text, reply_markup=menu[1].get('button'))
    try:
        del_menu(bot, telegram, users[telegram].get('mess_id'))
    except Exception as e:
        print('error', e)
        message_id = bot.send_message(telegram, NEED_PHONE_NUMBER, reply_markup=contact_menu())
        del_menu(bot, telegram, message_id.message_id)

    check_connect()
    user = select_user(telegram)
    if user == []:
        print(phone_number)
        if phone_number[0] == '+':
            phone_number = phone_number[1::]
            print('without+', phone_number)
        connect_mysql.insert('users', **{'telegram': telegram, 'name': first_name,
                                         'phone': phone_number})
        # views.checkout_contact(phone_number)
        contact_list = bitrix24.get_contact_list(phone_number)
        if contact_list == []:
            contact_id = bitrix24.add_contact(first_name, second_name, last_name, phone_number)
            print(contact_id.get('result'))
            views.add_contactID_to_db(telegram, contact_id.get('result'))
        else:
            views.add_contactID_to_db(telegram, contact_list[0].get('ID'))
        all_rows = views.select_list_of_users()
        print('^^^^^^^^^^^all_rows^^^^^^^^^^^', all_rows)
        report(NEW_USER.format(first_name, phone_number, all_rows))
    user_menu = select_menu(telegram)
    if user_menu == []:
        connect_mysql.insert('menu', **{'telegram': telegram, 'message_id': message_id.message_id,
                                        'text': text, 'index': 1})
    else:
        update_menu(telegram, message_id.message_id, text, 1)


# check text and build a new menu
def builder_menu(bot, telegram):
    users_menu = select_menu(telegram)
    send_menu(bot, telegram, users_menu.get('text'),
              users_menu.get('index'))
    try:
        del_menu(bot, users_menu.get('telegram'),
                 users_menu.get('message_id'))
    except Exception as e:
        print('error', e)


def check_answer(bot, telegram, text):
    if check_user(telegram) == []:
        message_id = bot.send_message(telegram, NEED_PHONE_NUMBER, reply_markup=contact_menu())
        users.update({telegram: {'mess_id': message_id.message_id}})
        return True
    users_menu = select_menu(telegram)
    if text == 'В начало':
        message_id = users_menu.get('message_id')
        send_menu(bot, telegram, MAIN_MENU, 1)
        try:
            del_menu(bot, telegram, message_id)
        except Exception as e:
            print('error', e)
        return
    if users_menu.get('index') == 0:
        try:
            try:
                users[telegram].update(street=text)
            except Exception as e:
                return back_to_main_menu_del(bot, telegram)
            confirm_menu(bot, telegram, False)
        except Exception as e:
            print('error', e)
    elif users_menu.get('index') == 1:
        back_to_main_menu_del(bot, telegram)
    elif users_menu.get('index') == 2:
        show_selected_bottles(bot, telegram)
    elif users_menu.get('index') == 15:
        to_order_bottles(bot, telegram)
    elif users_menu.get('index') == 7:
        try:
            text = int(text)
            try:
                users[telegram].update(bottles=text)
            except Exception as e:
                return back_to_main_menu_del(bot, telegram)
            show_selected_bottles(bot, telegram)
        except Exception as e:
            message_id = select_menu(telegram).get('message_id')
            send_menu(bot, telegram, HOW_MUCH, 7)
            try:
                del_menu(bot, telegram, message_id)
            except Exception as e:
                print('error', e)
    elif users_menu.get('index') == 8:
        try:
            users[telegram].update(street=text)
        except Exception as e:
            return back_to_main_menu_del(bot, telegram)
        confirm_menu(bot, telegram)
    elif users_menu.get('index') == 10:
        confirm_menu(bot, telegram, False)
    elif users_menu.get('index') == 12:
        try:
            canceled_the_order(bot, telegram, int(text))
        except Exception as e:
            print('error', e)
    elif users_menu.get('index') == 13:
        try:
            confirm_the_deliver(bot, telegram, int(text))
        except Exception as e:
            print('error', e)
    elif users_menu.get('index') == 14:
        show_pompa_confirm(bot, telegram)
    elif users_menu.get('index') == 17:
        try:
            text = int(text)
            try:
                users[telegram].update(pompa=text)
            except Exception as e:
                return back_to_main_menu_del(bot, telegram)
                # users.get({telegram: {'pompa': text}})
            show_pompa_confirm(bot, telegram)
        except Exception as e:
            order_pompa(bot, telegram)
    elif users_menu.get('index') == 19 or users_menu.get('index') == 21:
        try:
            text = int(text)
            try:
                if users[telegram].get('min_pack') <= text:
                    users[telegram].update(how_much_pack=text)
                    show_pack_bottle(bot, telegram)
                else:
                    text_send = 'Мало бутылок, <b>в пакете %s</b> минимальное количество бутылей равно <b>%s</b>' % \
                                (users[telegram].get('term'), users[telegram].get('min_pack'))
                    print('text_send', text_send)
                    views.just_send_mes(bot, telegram, text_send)
                    print('Мало бутылок')
            except Exception as e:
                return back_to_main_menu_del(bot, telegram)
        except Exception as e:
            print('error', e)
            message_id = select_menu(telegram).get('message_id')
            try:
                send_menu(bot, telegram, CIN_PACK_BOTTLES.format(users[telegram].get('price'),
                                                             users[telegram].get('min_pack'),
                                                             users[telegram].get('term')), 19)
            except Exception as e:
                return back_to_main_menu_del(bot, telegram)
            try:
                del_menu(bot, telegram, message_id)
            except Exception as e:
                print('error', e)
    elif users_menu.get('index') == 20:
        message_id = select_menu(telegram).get('message_id')
        try:
            send_photo(bot, telegram, WATER_PHOTO, SHOW_PACKAGE.
                       format(users[telegram]['price'], users[telegram]['term'],
                              users[telegram]['how_much_pack'],
                              (users[telegram]['how_much_pack'] * int(users[telegram]['price'])),
                              (users[telegram]['how_much_pack'] * (150 - int(users[telegram]['price'])))), 20)
        except Exception as e:
            return back_to_main_menu_del(bot, telegram)
        try:
            del_menu(bot, telegram, message_id)
        except Exception as e:
            print('error', e)
    elif users_menu.get('index') == 22:
        try:
            users[telegram].update(pack_street=text)
        except Exception as e:
            return back_to_main_menu_del(bot, telegram)
        show_confirm_pack_bottle(bot, telegram, False)
    elif users_menu.get('index') == 25:
        try:
            users[telegram].update(pack_comment=text)
        except Exception as e:
            return back_to_main_menu_del(bot, telegram)
        show_confirm_pack_bottle(bot, telegram, True)
        try:
            del_menu(bot, telegram, users_menu.get('message_id'))
        except Exception as e:
            print('error', e)
        return
    elif users_menu.get('index') == 26:
        try:
            # message_id = select_menu(telegram).get('message_id')
            try:
                users[telegram].update(pack_street=text)
            except Exception as e:
                return back_to_main_menu_del(bot, telegram)
            show_confirm_pack_bottle(bot, telegram)
            # try:
            #     del_menu(bot, telegram, message_id)
            # except Exception as e:
            #     print('error', e)
        except Exception as e:
            print('error', e)
    # elif users_menu.get('index') == 27:
    #     try:
    #         users[telegram].update(comment=text)
    #         report(users[telegram].get('report'))
    #     except Exception as e:
    #         return back_to_main_menu_del(bot, telegram)
    elif users_menu.get('index') == 28:
        try:
            users[telegram].update(comment=text)
            edit_report(users[telegram].get('report') + COMMENT.format(text))
            # message_id = select_menu(telegram).get('message_id')
            # reply_message(bot, telegram, message_id, PAYMENT_METHOD, 30)
            # back_to_main_menu_del(bot, telegram)
            # views.send_menu(bot, telegram, MAIN_MENU, 1)
            # try:
            #     del_menu(bot, telegram, message_id)
            # except Exception as e:
            #     print('error', e)
            skip(bot, telegram)
        except Exception as e:
            return back_to_main_menu_del(bot, telegram)
    else:
        builder_menu(bot, telegram)


def show_pompa_confirm(bot, telegram):
    message_id = select_menu(telegram).get('message_id')
    try:
        send_photo(bot, telegram, POMPA_PHOTO, POMPS.format(users[telegram].get('pompa'), 450,
                                                        (users[telegram].get('pompa') * 450)), 14)
    except Exception as e:
        return back_to_main_menu_del(bot, telegram)
    try:
        del_menu(bot, telegram, message_id)
    except Exception as e:
        print('error', e)
    return


def show_selected_bottles(bot, telegram):
    message_id = select_menu(telegram).get('message_id')
    try:
        send_photo(bot, telegram, WATER_PHOTO, BOTTLES.format(users[telegram].get('bottles'), 150,
                                                          (users[telegram].get('bottles') * 150)), 2)
    except Exception as e:
        return back_to_main_menu_del(bot, telegram)
    try:
        del_menu(bot, telegram, message_id)
    except Exception as e:
        print('error', e)
    return True


def show_confirm_pack_bottle(bot, telegram, where=True):
    text = ''
    message_id = select_menu(telegram).get('message_id')
    try:
        text = SHOW_PACKAGE_FOR_CONFIRM.format(
            users[telegram].get('price'), users[telegram].get('term'),
            users[telegram].get('how_much_pack'), users[telegram].get('pack_street'),
            (users[telegram].get('how_much_pack') * users[telegram].get('price')),
            (150 - users[telegram].get('price')) * users[telegram].get('how_much_pack'))
    except Exception as e:
        return back_to_main_menu_del(bot, telegram)
    if not where:
        try:
            return reply_message(bot, telegram, message_id, text, 25)
        except Exception as e:
            print('error', e)
    else:
        send_menu(bot, telegram, text, 25)
        try:
            del_menu(bot, telegram, message_id)
        except Exception as e:
            print('error', e)
        return


def confirm_menu(bot, telegram, first=True):
    try:
        if users[telegram].get('bottles') is None:
            return order_water(bot, telegram)
    except Exception as e:
        print('error', e)
        return back_to_main_menu_del(bot, telegram)

    try:
        text_for_confirm = DATES_FOR_CONFIRM.format(users[telegram].get('name'), users[telegram].get('phone'),
                                                users[telegram].get('street'))
    except Exception as e:
        return back_to_main_menu_del(bot, telegram)
    total = 1
    if users[telegram].get('bottles'):
        text_for_confirm += BOTTLES_FOR_CONFIRM.format(users[telegram].get('bottles'), 150,
                                                       (users[telegram].get('bottles') * 150))
        total = users[telegram].get('bottles') * 150
    if users[telegram].get('pompa'):
        text_for_confirm += POMPS_FOR_CONFIRM.format(users[telegram].get('pompa'), 450,
                                                     (users[telegram].get('pompa') * 450))
        total += users[telegram].get('pompa') * 450

    text_for_confirm += ITOG_CONFIRM.format(total)
    if first:
        reply_message(bot, telegram, select_menu(telegram).get('message_id'), text_for_confirm, 10)
    else:
        message_id = select_menu(telegram).get('message_id')
        send_menu(bot, telegram, text_for_confirm, 10)
        try:
            del_menu(bot, telegram, message_id)
        except Exception as e:
            print('error', e)


def minus_of_bottle(bot, telegram, call_id):
    try:
        if users[telegram]['bottles'] == 1:
            users[telegram]['bottles'] = 1
            alert(bot, call_id, 'Извиняй, половинку не продаем')
        else:
            users[telegram]['bottles'] -= 1
    except Exception as e:
        return back_to_main_menu_del(bot, telegram)
    users_menu = select_menu(telegram)
    try:
        edit_caption_of_photo(bot, BOTTLES.format(users[telegram]['bottles'], 150, (users[telegram]['bottles'] * 150)),
                              telegram, users_menu.get('message_id'), 2)
    except Exception as e:
        print('error', e)


def plus_of_bottle(bot, telegram):
    try:
        users[telegram]['bottles'] += 1
    except Exception as e:
        return back_to_main_menu_del(bot, telegram)
    users_menu = select_menu(telegram)
    try:
        edit_caption_of_photo(bot, BOTTLES.format(users[telegram]['bottles'], 150, (users[telegram]['bottles'] * 150)),
                              telegram, users_menu.get('message_id'), 2)
    except Exception as e:
        print('error', e)


def minus_of_pompa(bot, telegram, call_id):
    try:
        if users[telegram]['pompa'] == 1:
            users[telegram]['pompa'] = 1
            alert(bot, call_id, 'Извиняй, половинку не продаем')
        else:
            users[telegram]['pompa'] -= 1
    except Exception as e:
        return back_to_main_menu_del(bot, telegram)
    users_menu = select_menu(telegram)
    try:
        edit_caption_of_photo(bot, POMPS.format(users[telegram]['pompa'], 450, (users[telegram]['pompa'] * 450)),
                              telegram, users_menu.get('message_id'), 14)
    except Exception as e:
        print('error', e)


def plus_of_pompa(bot, telegram):
    try:
        users[telegram]['pompa'] += 1
    except Exception as e:
        return back_to_main_menu_del(bot, telegram)
    try:
        edit_caption_of_photo(bot, POMPS.format(users[telegram]['pompa'], 450, (users[telegram]['pompa'] * 450)),
                              telegram, select_menu(telegram).get('message_id'), 14)
    except Exception as e:
        print('error', e)


def to_order_bottles(bot, telegram):
    message_id = select_menu(telegram).get('message_id')
    last_order = select_last_street(telegram)
    try:
        if last_order == [] or last_order.get('amount') < users[telegram].get('bottles'):
            send_photo(bot, telegram, POMPA_PHOTO, POMPA, 15)
        else:
            for_street_menu(bot, telegram, select_last_street(telegram), "back_to_order", 0)
    except Exception as e:
        return back_to_main_menu_del(bot, telegram)
    try:
        del_menu(bot, telegram, message_id)
    except Exception as e:
        print('error', e)


def to_order_pompa(bot, telegram):
    message_id = select_menu(telegram).get('message_id')
    for_street_menu(bot, telegram, select_last_street(telegram), 'show_pompa', 0)
    try:
        del_menu(bot, telegram, message_id)
    except Exception as e:
        print('error', e)
    return
    # send_menu(bot, telegram, LOCATION, 8)


def confirm(bot, telegram, call_id):
    pay_menu(bot, telegram)
    # message_id = select_menu(telegram).get('message_id')
    # reply_message(bot, telegram, message_id, WISHES, 28)
    statTime = time.strftime("%H %M")
    # if statTime >= '09 00' and statTime <= '17 30':
    #     alert(bot, call_id, THANKS_FOR_ORDER_IN)
    # else:
    #     alert(bot, call_id, THANKS_FOR_ORDER_OUT)

    text = ''
    data_product = {
        'id': 0,
        'rows': []
    }
    price_water = []
    try:
        if users[telegram].get('bottles'):
            contact_id = views.check_contact_and_get(telegram)
            # contact_id = views.select_contactID(telegram)
            # if contact_id == []:
            #     if bitrix24.get_contact_list(phone_number) == []:
            #         contact_id = bitrix24.add_contact(first_name, second_name, last_name, phone_number)
            #         print(contact_id.get('result'))
            #         views.add_contactID_to_db(telegram, contact_id.get('result'))
            #     else:
            #         print(bitrix24.get_contact_list(phone_number))
            deal = bitrix24.add_deal(TITLE_OF_DEAL, contact_id, price.get('water'))
            # connect_mysql.add_dealID(telegram, deal.get('result'))
            insert_order(**{'telegram': telegram, 'name': users[telegram].get('name'),
                            'phone': users[telegram].get('phone'), 'goods': 'water',
                            'amount': users[telegram].get('bottles'), 'sum': (users[telegram].get('bottles') * price.get('water')),
                            'street': users[telegram].get('street'), 'deal_id': deal.get('result'), 'status': 'NEW'})
            data_product['id'] = deal.get('result')
            data_product['rows'].append(
                {'PRODUCT_ID': product_id.get('water'), 'PRICE': price.get('water'),
                 'QUANTITY': users[telegram].get('bottles')})
            summa = users[telegram].get('bottles') * price.get('water') * 100
            price_water.append(LabeledPrice(label='water19',
                         amount=summa))

            # prices.update({telegram: [LabeledPrice(label='water19',
            #                                        amount=users[telegram].get('bottles') * price.get('water'))]})
            try:
                text = FOR_SEND_ORDER_TO_OTHER_BOT2.format(telegram, users[telegram].get('name'), users[telegram].get('phone'),
                                                           users[telegram].get('street'))
                text += FOR_SEND_BOTTLE_TO_OTHER_BOT.format('вода', users[telegram].get('bottles'),
                                                            (users[telegram].get('bottles') * price.get('water')))
            except Exception as e:
                print('error', e)
    except Exception as e:
        return back_to_main_menu_del(bot, telegram)

    if users[telegram].get('pompa'):
        insert_order(**{'telegram': telegram, 'name': users[telegram].get('name'),
                        'phone': users[telegram].get('phone'), 'goods': 'pompa',
                        'amount': users[telegram].get('pompa'), 'sum': (users[telegram].get('pompa') * price.get('pompa')),
                        'street': users[telegram].get('street'), 'deal_id': deal.get('result'), 'status': 'NEW'})
        data_product['rows'].append(
            {'PRODUCT_ID': product_id.get('pompa'), 'PRICE': price.get('pompa'),
             'QUANTITY': users[telegram].get('pompa')})
        summa = users[telegram].get('pompa') * price.get('pompa') * 100
        price_water.append(LabeledPrice(label='pompa',
                                   amount=summa))
        # prices[telegram].append(LabeledPrice(label='pompa',
        #                                        amount=users[telegram].get('pompa') * price.get('pompa')))
        try:
            text += FOR_SEND_POMPA_TO_OTHER_BOT.format('помпа', users[telegram].get('pompa'),
                                                        (users[telegram].get('pompa') * price.get('pompa')))
        except Exception as e:
            print('error pompa', e)
    prices.update({telegram: price_water})
    bitrix24.add_product_to_deal(data_product)
    users[telegram].update(report=text)
    report(text)


def cancel_the_order(bot, telegram, call_id):
    reply_message(bot, telegram, select_menu(telegram).get('message_id'), CANCEL_THE_ORDER, 12)


def canceled_the_order(bot, telegram, order_number):
    try:
        order = check_order(telegram, order_number)
        if order == []:
            pass
        else:
            delete_the_order(order_number)
        # alert(bot, call_id, CANCELED_THE_ORDER)
    except Exception as e:
        print('error', e)
    basket(bot, telegram, select_menu(telegram).get('message_id'))


def confirm_the_deliver(bot, telegram, order_number):
    try:
        order = check_order(telegram, order_number)
        if order == []:
            pass
        else:
            delete_the_order(order_number)
    except Exception as e:
        print('error', e)
    admin_panel(bot, telegram)


def show_orders(bot, telegram, message_id, call_id):
    orders = select_all_orders()
    if orders == []:
        alert(bot, call_id, NOT_ORDERS)
        reply_message(bot, telegram, select_menu(telegram).get('message_id'), MAIN_MENU, 1)
    else:
        text = build_orders(orders)
        views.just_send_mes(bot, telegram, text)
        # try:
        #     send_menu(bot, telegram, text, 24)
        # except Exception as e:
        #     print('error', e)
        message_id = select_menu(telegram).get('message_id')
        send_menu(bot, telegram, 'Заказы', 4)
        try:
            del_menu(bot, telegram, message_id)
        except Exception as e:
            print('error', e)
        return


def confirm_delivery(bot, telegram, message_id, call_id):
    orders = select_all_orders()
    if orders == []:
        alert(bot, call_id, NOT_ORDERS)
        reply_message(bot, telegram, select_menu(telegram).get('message_id'), MAIN_MENU, 1)
    else:
        text = build_orders(orders)
        message_id = select_menu(telegram).get('message_id')
        try:
            send_menu(bot, telegram, text, 24)
        except Exception as e:
            print('error', e)
        send_menu(bot, telegram, CONFIRM_DELIVER, 13)
        try:
            del_menu(bot, telegram, message_id)
        except Exception as e:
            print('error', e)
        return


def confirm_deliver(bot, telegram, order_number):
    try:
        order = check_order(telegram, order_number)
        if order == []:
            pass
        else:
            delete_the_order(order_number)
    except Exception as e:
        print('error', e)
    confirm_delivery(bot, telegram, select_menu(telegram).get('message_id'), None)


# def back_order_water(bot, telegram):
#     users_menu = select_menu(telegram)
#     message_id = users_menu.get('message_id')
#     try:
#         send_photo(bot, telegram, WATER_PHOTO, BOTTLES.format(users[telegram].get('bottles'),
#                                                           150, (users[telegram]['bottles'] * 150)), 2)
#     except Exception as e:
#         return back_to_main_menu_del(bot, telegram)
#     try:
#         del_menu(bot, telegram, message_id)
#     except Exception as e:
#         print('error', e)


def order_pompa(bot, telegram):
    message_id = select_menu(telegram).get('message_id')
    send_menu(bot, telegram, COUNTER_POMPAS, 17)
    try:
        del_menu(bot, telegram, message_id)
    except Exception as e:
        print('error', e)
    return


def no_need_pompa(bot, telegram, message_id, call_id):
    message_id = select_menu(telegram).get('message_id')
    for_street_menu(bot, telegram, select_last_street(telegram), "back_to_order", 0)
    try:
        del_menu(bot, telegram, message_id)
    except Exception as e:
        print('error', e)
    return


def back_empty_bottle(bot, telegram, message_id, call_id):
    to_order_bottles(bot, telegram)


def pack_three_months(bot, telegram):
    try:
        users[telegram].update(min_pack=21, term='3 мес.', price=140)
    except Exception as e:
        return back_to_main_menu_del(bot, telegram)
    reply_message(bot, telegram, select_menu(telegram).get('message_id'),
                  CIN_PACK_BOTTLES.format(140, 21, '3 мес.'), 19)
    # message_id = select_menu(telegram).get('message_id')
    # send_menu(bot, telegram, CIN_PACK_BOTTLES.format(140, 21, '3 мес.'), 19)
    # del_menu(bot, telegram, message_id)


def pack_six_months(bot, telegram):
    try:
        users[telegram].update(min_pack=42, term='6 мес.', price=130)
    except Exception as e:
        return back_to_main_menu_del(bot, telegram)
    reply_message(bot, telegram, select_menu(telegram).get('message_id'),
                  CIN_PACK_BOTTLES.format(130, 42, '6 мес'), 19)
    # message_id = select_menu(telegram).get('message_id')
    # send_menu(bot, telegram, CIN_PACK_BOTTLES.format(130, 42, '6 мес'), 19)
    # del_menu(bot, telegram, message_id)


def pack_1_year(bot, telegram):
    try:
        users[telegram].update(min_pack=84, term='1 год', price=120)
    except Exception as e:
        return back_to_main_menu_del(bot, telegram)
    reply_message(bot, telegram, select_menu(telegram).get('message_id'),
                  CIN_PACK_BOTTLES.format(120, 84, '1 год'), 19)
    # message_id = select_menu(telegram).get('message_id')
    # send_menu(bot, telegram, CIN_PACK_BOTTLES.format(120, 84, '1 год'), 19)
    # del_menu(bot, telegram, message_id)


def change_adress(bot, telegram, where, index):
    message_id = select_menu(telegram).get('message_id')
    for_street_menu(bot, telegram, select_last_street(telegram), where, index)
    try:
        del_menu(bot, telegram, message_id)
    except Exception as e:
        print('error', e)
    return


def want_to_economize(bot, telegram):
    return reply_message(bot, telegram, select_menu(telegram).get('message_id'), ALL_PACKEGES, 18)


def minus_of_pack_bottle(bot, telegram, call_id):
    try:
        if users[telegram]['how_much_pack'] <= users[telegram]['min_pack']:
            users[telegram]['how_much_pack'] = users[telegram]['min_pack']
            alert(bot, call_id, 'Извиняй, {}бут это минимально возможное количество на {}'.
                  format(users[telegram]['min_pack'], users[telegram]['term']))
        else:
            users[telegram]['how_much_pack'] -= 1
    except Exception as e:
        return back_to_main_menu_del(bot, telegram)
    users_menu = select_menu(telegram)
    try:
        edit_caption_of_photo(bot, SHOW_PACKAGE.format(
            users[telegram]['price'], users[telegram]['term'],
            users[telegram]['how_much_pack'],
            (users[telegram]['how_much_pack'] * int(users[telegram]['price'])),
            (users[telegram]['how_much_pack'] * (150 - int(users[telegram]['price'])))),
            telegram, users_menu.get('message_id'), 20)
    except Exception as e:
        print('error', e)


def plus_of_pack_bottle(bot, telegram):
    try:
        users[telegram]['how_much_pack'] += 1
    except Exception as e:
        return back_to_main_menu_del(bot, telegram)
    users_menu = select_menu(telegram)
    try:
        edit_caption_of_photo(bot, SHOW_PACKAGE.format(
            users[telegram]['price'], users[telegram]['term'],
            users[telegram]['how_much_pack'],
            (users[telegram]['how_much_pack'] * int(users[telegram]['price'])),
            (users[telegram]['how_much_pack'] * (150 - int(users[telegram]['price'])))),
            telegram, users_menu.get('message_id'), 20)
    except Exception as e:
        print('error', e)


def to_order_package(bot, telegram):
    message_id = select_menu(telegram).get('message_id')
    try:
        if users[telegram].get('street') is None:
            return change_adress(bot, telegram, 'order_package', 26)
    except Exception as e:
        print(e)
    try:
        users[telegram].update(pack_street=users[telegram].get('street'))
    except Exception as e:
        return back_to_main_menu_del(bot, telegram)
    show_confirm_pack_bottle(bot, telegram)
    # try:
    #     del_menu(bot, telegram, message_id)
    # except Exception as e:
    #     print('error', e)
    return


def show_pack_bottle(bot, telegram):
    message_id = select_menu(telegram).get('message_id')
    try:
        send_photo(bot, telegram, WATER_PHOTO, SHOW_PACKAGE.
               format(users[telegram]['price'], users[telegram]['term'],
                      users[telegram]['how_much_pack'],
                      (users[telegram]['how_much_pack'] * int(users[telegram]['price'])),
                      (users[telegram]['how_much_pack'] * (150 - int(users[telegram]['price'])))), 20)
    except Exception as e:
        return back_to_main_menu_del(bot, telegram)
    try:
        del_menu(bot, telegram, message_id)
    except Exception as e:
        print('error', e)


def change_the_quantity(bot, telegram):
    message_id = select_menu(telegram).get('message_id')
    try:
        send_menu(bot, telegram, CIN_PACK_BOTTLES.format(users[telegram].get('term'), users[telegram].get('min_pack'),
                                                     users[telegram].get('price'), users[telegram].get('term')), 21)
    except Exception as e:
        return back_to_main_menu_del(bot, telegram)
    try:
        del_menu(bot, telegram, message_id)
    except Exception as e:
        print('error', e)
    return


# def change_adress_pack(bot, telegram):
#     return reply_message(bot, telegram, select_menu(telegram).get('message_id'), LOCATION, 22)


def confirm_pack_add_to_db(bot, telegram, call_id):
    statTime = time.strftime("%y%m")
    statTime += '01'

    # print(int(statTime))
    try:
        price_water = []
        data_product = {
            'id': 0,
            'rows': []
        }
        # contact_id = views.select_contactID(telegram)
        contact_id = views.check_contact_and_get(telegram)
        deal = bitrix24.add_deal(users[telegram]['term'], contact_id, users[telegram]['price'])
        # connect_mysql.add_dealID(telegram, deal.get('result'))

        data_product['id'] = deal.get('result')
        data_product['rows'].append(
            {'PRODUCT_ID': product_id.get(users[telegram]['price']), 'PRICE': users[telegram]['price'],
             'QUANTITY': users[telegram]['how_much_pack']})
        add_package(**{'telegram': telegram, 'name': users[telegram].get('name'),
                       'phone': users[telegram].get('phone'), 'price': users[telegram]['price'],
                       'term': users[telegram]['term'], 'quantity': users[telegram]['how_much_pack'],
                       'sum': (users[telegram]['price'] * users[telegram]['how_much_pack']),
                       'econom': (users[telegram].get('how_much_pack') * (150 - users[telegram]['price'])),
                       'adress': users[telegram].get('pack_street'), 'deal_id': deal.get('result'), 'status': 'NEW'})
        bitrix24.add_product_to_deal(data_product)

        summa = users[telegram]['price'] * users[telegram]['how_much_pack'] * 100
        price_water.append(LabeledPrice(label=users[telegram]['term'],
                                        amount=summa))
        prices.update({telegram: price_water})
    except Exception as e:
        return back_to_main_menu_del(bot, telegram)
    try:
        text = FOR_SEND_PACK_TO_OTHER_BOT.format(telegram, users[telegram].get('name'),
                                             users[telegram].get('phone'), users[telegram]['term'],
                                             users[telegram]['price'], users[telegram]['how_much_pack'],
                                             (users[telegram]['price'] * users[telegram]['how_much_pack']),
                                             (users[telegram].get('how_much_pack') * (150 - users[telegram]['price'])),
                                             users[telegram].get('pack_street'))
    except Exception as e:
        print(e)
        return back_to_main_menu_del(bot, telegram)

    report(text)
    try:
        users[telegram].update(report=text)
    except Exception as e:
        back_to_main_menu_del(bot, telegram)

    # alert(bot, call_id, THANKS_FOR_ORDER_PACK)
    # reply_message(bot, telegram, select_menu(telegram).get('message_id'), WISHES, 28)
    pay_menu(bot, telegram)


def set_bottles(bot, telegram, amount):
    try:
        users[telegram].update(bottles=amount)
    except Exception as e:
        return back_to_main_menu_del(bot, telegram)
    show_selected_bottles(bot, telegram)


def set_pomps(bot, telegram, amount):
    try:
        users[telegram].update(pompa=amount)
    except Exception as e:
        return back_to_main_menu_del(bot, telegram)
    show_pompa_confirm(bot, telegram)


def replay_order(bot, telegram):
    last_order = select_last_street(telegram)
    last_order.pop('order_number')
    users.update({last_order.get('telegram'): last_order})
    users[telegram].update(bottles=last_order.get('amount'))
    text_for_confirm = DATES_FOR_CONFIRM.format(users[telegram].get('name'), users[telegram].get('phone'),
                                                                                   users[telegram].get('street'))
    total = 1
    if users[telegram].get('bottles'):
        text_for_confirm += BOTTLES_FOR_CONFIRM.format(users[telegram].get('bottles'), 150,
                                                       (users[telegram].get('bottles') * 150))
        total = users[telegram].get('bottles') * 150
    text_for_confirm += ITOG_CONFIRM.format(total)
    reply_message(bot, telegram, select_menu(telegram).get('message_id'), text_for_confirm, 27)


def about_water(bot, telegram):
    message_id = select_menu(telegram).get('message_id')
    views.just_send_mes(bot, telegram, ABOUT_WATER)
    send_menu(bot, telegram, MAIN_MENU, 1)
    try:
        del_menu(bot, telegram, message_id)
    except Exception as e:
        print('error', e)
    return


def about_company(bot, telegram):
    reply_message(bot, telegram, select_menu(telegram).get('message_id'), ABOUT_COMPANY, 1)


def set_street(bot, telegram):
    if select_menu(telegram).get('index') == 0:
        try:
            users[telegram].update(street=select_last_street(telegram).get('street'))
        except Exception as e:
            print('error', e)
            return back_to_main_menu_del(bot, telegram)
        confirm_menu(bot, telegram)

    if select_menu(telegram).get('index') == 26:
        try:
            users[telegram].update(pack_street=select_last_street(telegram).get('street'))
        except Exception as e:
            print('error', e)
            return back_to_main_menu_del(bot, telegram)
        show_confirm_pack_bottle(bot, telegram)


def economize(bot, telegram):
    reply_message(bot, telegram, select_menu(telegram).get('message_id'), ALL_PACKEGES, 29)


def pay_menu(bot, telegram):
    message_id = select_menu(telegram).get('message_id')
    reply_message(bot, telegram, message_id, PAYMENT_METHOD, 30)


def yandex_payment(bot, telegram):
    views.invoice(bot, telegram)
    # bot.send_message(message.chat.id,
    #                  "Real cards won't work with me, no money will be debited from your account."
    #                  " Use this test card number to pay for your Time Machine: `4242 4242 4242 4242`"
    #                  "\n\nThis is your demo invoice:", parse_mode='Markdown')


def cash_payment(bot, telegram):
    return back_to_main_menu_del(bot, telegram)


def leave_wishes(bot, telegram):
    message_id = select_menu(telegram).get('message_id')
    reply_message(bot, telegram, message_id, WISHES, 28)


def payment_success(bot, telegram, summa):
    message_id = select_menu(telegram).get('message_id')
    views.send_menu(bot, telegram, WISHES, 28)
    try:
        del_menu(bot, telegram, message_id)
    except Exception as e:
        print(e)
    user = select_user(telegram)
    report_about_paid(USER_PAID.format(user.get('name'), summa, user.get('telegram'), user.get('phone')))


def skip(bot, telegram):
    statTime = time.strftime("%H %M")
    if statTime >= '09 00' and statTime <= '17 30':
        mes = THANKS_FOR_ORDER_IN
    else:
        mes = THANKS_FOR_ORDER_OUT
    message_id = select_menu(telegram).get('message_id')
    views.send_menu(bot, telegram, mes + '\n' + MAIN_MENU, 1)
    try:
        del_menu(bot, telegram, message_id)
    except Exception as e:
        print('error', e)
