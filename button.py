#!/usr/bin/env python
# coding=utf-8

from telebot import types


def contact_menu():
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text="Отправить номер телефона", request_contact=True))
    return keyboard


def location_menu():
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text="Отправить свою локацию", request_location=True))
    return keyboard


def back_to_main_menu():
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text="В начало"))
    return keyboard


# _________Инлайн_кнопки___________


def inline_main_menu():
    try:
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text="Заказать воду", callback_data="start: order_water"))
        keyboard.add(types.InlineKeyboardButton(text="История заказов", callback_data="start: basket"))
        # keyboard.add(types.InlineKeyboardButton(text="Админ панель", callback_data="start: admin_panel"))
        keyboard.add(types.InlineKeyboardButton(text="Помощь❓", callback_data="start: instruction"))
        return keyboard
    except Exception as e:
        print(e)
    return False


def inline_order_water(type_of_order):
    try:
        keyboard = types.InlineKeyboardMarkup()

        keyboard.add(*[types.InlineKeyboardButton(text='➖', callback_data=type_of_order + ': minus'),
                       types.InlineKeyboardButton(text='Заказать', callback_data=type_of_order + ': select'),
                       types.InlineKeyboardButton(text='➕', callback_data=type_of_order + ': plus')])
        keyboard.add(types.InlineKeyboardButton(text="Отменить", callback_data="back: back_to_main_menu_del"))
        return keyboard
    except Exception as e:
        print(e)
    return False
# keyboard.add(types.InlineKeyboardButton(text="Ввести другое", callback_data=type_of_order + ': input'))

def inline_basket_menu():
    try:
        keyboard = types.InlineKeyboardMarkup()
        # keyboard.add(types.InlineKeyboardButton(text="Отменить заказ🔚", callback_data="basket: cancel_the_order"))
        keyboard.add(types.InlineKeyboardButton(text="Повторить последний заказ", callback_data="basket: replay_order"))
        keyboard.add(types.InlineKeyboardButton(text="Назад", callback_data="back: back_to_main_menu"))
        return keyboard
    except Exception as e:
        print(e)
    return False


def inline_instruction_menu():
    try:
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text="Узнать о воде", callback_data="instruction: about_water"))
        keyboard.add(types.InlineKeyboardButton(text="Контакты компании", callback_data="instruction: about_company"))
        # keyboard.add(types.InlineKeyboardButton(text="Назад", callback_data="back: back_to_main_menu"))
        return keyboard

        # Get_points1 = types.InlineQueryResultArticle(
        #     id='1', title="Все хорошо",
        #     description="Good(^^)",
        #     input_message_content=types.InputTextMessageContent(
        #         message_text="good work"),
        #     # thumb_url=minus_icon, thumb_width=48, thumb_height=48
        # )
        #
        # Get_points2 = types.InlineQueryResultArticle(
        #     id='1', title="Все хорошо",
        #     description="Bad(>_<)",
        #     input_message_content=types.InputTextMessageContent(
        #         message_text="bad, try decide, ok?"),
        #     # thumb_url=minus_icon, thumb_width=48, thumb_height=48
        # )
        #
        # Get_points3 = types.InlineQueryResultArticle(
        #     id='1', title="Завершить",
        #     description="><",
        #     input_message_content=types.InputTextMessageContent(
        #         message_text="okay, let's finish"),
        #     # thumb_url=minus_icon, thumb_width=48, thumb_height=48
        # )
    except Exception as e:
        print(e)
    return False


def inline_admin_menu():
    try:
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text="Заказы", callback_data="admin: orders"))
        keyboard.add(types.InlineKeyboardButton(text="Подтвердить доставку", callback_data="admin: confirm_delivery"))
        keyboard.add(types.InlineKeyboardButton(text="Назад", callback_data="back: back_to_main_menu"))
        return keyboard
    except Exception as e:
        print(e)
    return False


def inline_back_menu(type_of_back):
    try:
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(*[types.InlineKeyboardButton(text="1", callback_data='bottles: 1'),
                       types.InlineKeyboardButton(text="2", callback_data='bottles: 2'),
                       types.InlineKeyboardButton(text="3", callback_data='bottles: 3')])
        keyboard.add(types.InlineKeyboardButton(text="Хочу сэкономить", callback_data='bottles: economize'))
        keyboard.add(types.InlineKeyboardButton(text="Повторить последний заказ", callback_data="basket: replay_order"))
        keyboard.add(types.InlineKeyboardButton(text="Назад", callback_data='back: ' + type_of_back))
        return keyboard
    except Exception as e:
        print(e)
    return False


def inline_location_menu(where):
    try:
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text="Назад", callback_data="location: {}".format(where)))
        # keyboard.add(types.InlineKeyboardButton(text="Отменить", callback_data="back_to_main_menu_del"))
        return keyboard
    except Exception as e:
        print(e)
    return False


def inline_location_menu2(street, where):
    try:
        keyboard = types.InlineKeyboardMarkup()
        # keyboard.add(types.InlineKeyboardButton(text=street, callback_data="location: street {}".format(street)))
        keyboard.add(types.InlineKeyboardButton(text=street, callback_data="location: street"))
        keyboard.add(types.InlineKeyboardButton(text="Назад", callback_data="location: {}".format(where)))
        # keyboard.add(types.InlineKeyboardButton(text="Отменить", callback_data="back_to_main_menu_del"))
        return keyboard
    except Exception as e:
        print(e)
    return False


def inline_confirm_menu():
    try:
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text="Подтвердить", callback_data="confirm: confirm"))
        keyboard.add(types.InlineKeyboardButton(text="Изменить адрес", callback_data="confirm: change_adress"))
        keyboard.add(types.InlineKeyboardButton(text="Хочу сэкономить", callback_data="confirm: want_to_economize"))
        keyboard.add(types.InlineKeyboardButton(text="Отменить", callback_data="back: back_to_main_menu"))
        return keyboard
    except Exception as e:
        print(e)
    return False


def inline_basket_empty_menu():
    try:
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text="Заказать", callback_data="start: order_water"))
        keyboard.add(types.InlineKeyboardButton(text="Назад", callback_data="back: back_to_main_menu"))
        return keyboard
    except Exception as e:
        print(e)
    return False


def inline_cancel_menu():
    try:
        keyboard = types.InlineKeyboardMarkup()
        # keyboard.add(types.InlineKeyboardButton(text="Назад", callback_data="start: basket"))
        keyboard.add(types.InlineKeyboardButton(text="Отменить", callback_data="back: back_to_main_menu"))
        return keyboard
    except Exception as e:
        print(e)
    return False


def inline_confirm_deliver_menu():
    try:
        keyboard = types.InlineKeyboardMarkup()
        # keyboard.add(types.InlineKeyboardButton(text="Назад", callback_data="start: admin_panel"))
        keyboard.add(types.InlineKeyboardButton(text="Отменить", callback_data="back: back_to_main_menu"))
        return keyboard
    except Exception as e:
        print(e)
    return False


def inline_pompa_menu():
    try:
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(*[types.InlineKeyboardButton(text="Да, заказать", callback_data="pompa: order_pompa"),
                       types.InlineKeyboardButton(text="Нет, спасибо", callback_data="pompa: no_need")])
        keyboard.add(types.InlineKeyboardButton(text="Назад", callback_data="pompa: back_to_water"))
        keyboard.add(types.InlineKeyboardButton(text="Отменить", callback_data="back: back_to_main_menu_del"))
        return keyboard
    except Exception as e:
        print(e)
    return False


def inline_order_pompa_water():
    try:
        keyboard = types.InlineKeyboardMarkup()

        keyboard.add(*[types.InlineKeyboardButton(text='➖', callback_data='order: minus_of_bottle'),
                       types.InlineKeyboardButton(text='Заказать', callback_data='order: select'),
                       types.InlineKeyboardButton(text='➕', callback_data='order: plus_of_bottle')])
        keyboard.add(types.InlineKeyboardButton(text="Отменить", callback_data="back: back_to_main_menu_del"))
        return keyboard
    except Exception as e:
        print(e)
    return False


# keyboard.add(types.InlineKeyboardButton(text="Ввести другое", callback_data="order: input"))

def inline_backer_menu():
    try:
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(*[types.InlineKeyboardButton(text="1", callback_data='pomps: 1'),
                       types.InlineKeyboardButton(text="2", callback_data='pomps: 2'),
                       types.InlineKeyboardButton(text="3", callback_data='pomps: 3')]
                     )
        keyboard.add(types.InlineKeyboardButton(text="Назад", callback_data='back: pompa_ques'))
        # keyboard.add(types.InlineKeyboardButton(text="В начало", callback_data="back: back_to_main_menu_del"))
        return keyboard
    except Exception as e:
        print(e)
    return False


def inline_packages_menu(type):
    try:
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text="На 3 мес. - 140р", callback_data='package: 3_months'))
        keyboard.add(types.InlineKeyboardButton(text="На 6 мес. - 130р", callback_data='package: 6_months'))
        keyboard.add(types.InlineKeyboardButton(text="На 1 год - 120р.", callback_data='package: 1_year'))
        keyboard.add(types.InlineKeyboardButton(text="Назад", callback_data=type + ': back_to_confirm_order'))
        return keyboard
    except Exception as e:
        print(e)
    return False


def inline_cin_pack_menu(where):
    try:
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text="Назад", callback_data='back: {}'.format(where)))
        return keyboard
    except Exception as e:
        print(e)
    return False


def inline_pack_bottle_menu():
    try:
        keyboard = types.InlineKeyboardMarkup()

        keyboard.add(*[types.InlineKeyboardButton(text='➖', callback_data='package: minus_of_pack_bottle'),
                       types.InlineKeyboardButton(text='Заказать', callback_data='package: to_order_package'),
                       types.InlineKeyboardButton(text='➕', callback_data='package: plus_of_pack_bottle')])
        keyboard.add(types.InlineKeyboardButton(text="Отменить пакет", callback_data="package: back_to_confirm_order"))
        return keyboard
    except Exception as e:
        print(e)
    return False
# keyboard.add(types.InlineKeyboardButton(text="Ввести другое", callback_data="package: change_the_quantity"))

def inline_confirm_pack_menu():
    try:
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text="Подтвердить", callback_data="confirm_package: confirm_pack_add_to_db"))
        keyboard.add(types.InlineKeyboardButton(text="Изменить адрес", callback_data="confirm_package: change_adress_pack"))
        keyboard.add(types.InlineKeyboardButton(text="Отменить пакет", callback_data="package: back_to_confirm_order"))
        return keyboard
    except Exception as e:
        print(e)
    return False


def inline_replay_confirm():
    try:
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text="Подтвердить", callback_data="replay: confirm"))
        # keyboard.add(types.InlineKeyboardButton(text="Изменить адрес", callback_data="replay: change_adress"))
        keyboard.add(types.InlineKeyboardButton(text="Отменить", callback_data="back: back_to_main_menu"))
        return keyboard
    except Exception as e:
        print(e)
    return False


def inline_comment_menu():
    try:
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text="Пропустить", callback_data="payment: skip"))
        return keyboard
    except Exception as e:
        print(e)
    return False


def inline_pre_payment_menu():
    try:
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text="Банковской картой", callback_data="payment: yandex"))
        keyboard.add(types.InlineKeyboardButton(text="Наличными", callback_data="payment: wish"))
        return keyboard
    except Exception as e:
        print(e)
    return False


#
# def inline_payment_menu():
#     try:
#         keyboard = types.InlineKeyboardMarkup()
#         keyboard.add(types.InlineKeyboardButton(text="Оплатить", callback_data="payment: pay_menu"))
#         return keyboard
#     except Exception as e:
#         print(e)
#     return False
