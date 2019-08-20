import requests
import json
import time

proect_sv = 'proektsv.bitrix24.ru/rest/26/pcw309lfbp2d2d79'
# test = 'testjj.bitrix24.ru/rest/1/wczorpkc6n2spne0'

url_deal_add = 'https://proektsv.bitrix24.ru/rest/26/pcw309lfbp2d2d79/crm.deal.add.json/'
url_deal_list = 'https://proektsv.bitrix24.ru/rest/26/pcw309lfbp2d2d79/crm.deal.list/'
url_deal_get = 'https://proektsv.bitrix24.ru/rest/26/pcw309lfbp2d2d79/crm.deal.get/'

url_contact_add = 'https://proektsv.bitrix24.ru/rest/26/pcw309lfbp2d2d79/crm.contact.add.json/'
url_contact_list = 'https://proektsv.bitrix24.ru/rest/26/pcw309lfbp2d2d79/crm.contact.list/'

url_product_add = 'https://proektsv.bitrix24.ru/rest/26/pcw309lfbp2d2d79/crm.product.add.json/'
url_product_list = 'https://proektsv.bitrix24.ru/rest/26/pcw309lfbp2d2d79/crm.product.list/'

url_set_product = 'https://proektsv.bitrix24.ru/rest/26/pcw309lfbp2d2d79/crm.deal.productrows.set.json/'


# url_deal_add = 'https://testjj.bitrix24.ru/rest/1/wczorpkc6n2spne0/crm.deal.add.json/'
# url_deal_list = 'https://testjj.bitrix24.ru/rest/1/wczorpkc6n2spne0/crm.deal.list/'
# url_deal_get = 'https://testjj.bitrix24.ru/rest/1/wczorpkc6n2spne0/crm.deal.get/'
#
# url_contact_add = 'https://testjj.bitrix24.ru/rest/1/wczorpkc6n2spne0/crm.contact.add.json/'
# url_contact_list = 'https://testjj.bitrix24.ru/rest/1/wczorpkc6n2spne0/crm.contact.list/'
#
# url_product_add = 'https://testjj.bitrix24.ru/rest/1/wczorpkc6n2spne0/crm.product.add.json/'
# url_product_list = 'https://testjj.bitrix24.ru/rest/1/wczorpkc6n2spne0/crm.product.list/'
#
# url_set_product = 'https://testjj.bitrix24.ru/rest/1/wczorpkc6n2spne0/crm.deal.productrows.set.json/'


# Для добавления новой сделки
def add_deal(name, contact_id, price):
    data = {'fields': {
        "TITLE": name,
        "TYPE_ID": "GOODS",
        "STAGE_ID": "NEW",
        "COMPANY_ID": 1,
        "CONTACT_ID": contact_id,
        "OPENED": "YES",
        "ASSIGNED_BY_ID": 26,
        "PROBABILITY": 80,
        "CURRENCY_ID": "RUB",
        "OPPORTUNITY": price,
        "BEGINDATE": time.time()
    },
        'params': {"REGISTER_SONET_EVENT": "Y"}}
    response = requests.post(url_deal_add, json=data)
    results = json.loads(response.content.decode('utf8'))
    return results


# Добавление контактов
def add_contact(name, second_name, last_name, phone):
    data = {
        "fields": {
            "NAME": name,
            "SECOND_NAME": second_name,
            "LAST_NAME": last_name,
            "OPENED": "Y",
            "ASSIGNED_BY_ID": 26,
            "TYPE_ID": "CLIENT",
            "SOURCE_ID": "SELF",
            "PHONE": [{"VALUE": phone, "VALUE_TYPE": "WORK"}],
            "COMMENT": "FROM telegram"
        },
        "params": {"REGISTER_SONET_EVENT": "Y"}}
    response = requests.post(url_contact_add, json=data)
    results = json.loads(response.content.decode('utf8'))
    return results


# Для добавления нового продукта(товара)
def add_product(name, price, sort):
    data = {'fields': {
            "NAME": name,
            "CURRENCY_ID": "RUB",
            "PRICE": price,
            "SORT": sort
    }}
    response = requests.post(url_product_add, json=data)
    results = json.loads(response.content.decode('utf8'))
    return results


# Добавление контактов
def add_product_to_deal(data):
    # deal_id, product_id, price, quantity
    # data = {
    #     'id': deal_id,
    #     'rows':
    #         [
    #             {"PRODUCT_ID": product_id, "PRICE": price, "QUANTITY": quantity}
    #         ]
    # }
    response = requests.post(url_set_product, json=data)
    results = json.loads(response.content.decode('utf8'))
    return results


# Для вывода списка сделок
def get_deal_list():
    response = requests.get(url_deal_list)
    results = json.loads(response.content.decode('utf8'))
    for result in results.get('result'):
        print(result)


# Для вывода списка контактов
def get_contact_list(phone):
    param = {"select": ['ID', "PHONE", 'NAME'], 'filter': {"PHONE": phone}}
    response = requests.post(url_contact_list, json=param)
    return json.loads(response.content.decode('utf8')).get('result')


def get_contact_list_all():
    response = requests.post(url_contact_list)
    return json.loads(response.content.decode('utf8')).get('result')


# Для вывода списка товаров
def get_product_list():
    # response = requests.get('https://testjj.bitrix24.ru/rest/1/wczorpkc6n2spne0/crm.product.list/')
    response = requests.get(url_product_list)
    results = json.loads(response.content.decode('utf8'))
    print(results)
    for result in results.get('result'):
        print(result)

def get_deal_state(id):
    response = requests.get(url_deal_get, params=id)
    result = json.loads(response.content.decode('utf8'))
    return result


# Для добавления новой сделки
# data = {'fields': {
#     "TITLE": name,
#     "TYPE_ID": "GOODS",
#     "STAGE_ID": "NEW",
#     "COMPANY_ID": 1,
#     "CONTACT_ID": contact_id,
#     "OPENED": "YES",
#     "ASSIGNED_BY_ID": 1,
#     "PROBABILITY": 80,
#     "CURRENCY_ID": "RUB",
#     "OPPORTUNITY": price,
#     "BEGINDATE": time.time()
# },
#     'params': {"REGISTER_SONET_EVENT": "Y"}}
# add_deal(data)

# print(get_product_list())

# print(add_product('Pompa', 450, 500))

# print(get_contact_list_all())
# for res in get_contact_list_all():
#     print(res)
#
# deal = add_deal('water 19', 13, 150)
#
# data_product = {
#     'id': 0,
#     'rows': []
# }
# # deal.get('result')
# data_product['id'] = deal.get('result')
# data_product['rows'].append(
#     {'PRODUCT_ID': 1, 'PRICE': 150, 'QUANTITY': 5})
#
# data_product['rows'].append(
#     {'PRODUCT_ID': 11, 'PRICE': 450, 'QUANTITY': 2})
# print(data_product)
# add_product_to_deal(data_product)


# get_deal_list()


#
# results = json.loads(res.content.decode('utf8')).get('result')
# print(res)
# print(results.get('STAGE_ID'))

# response = requests.get('https://testjj.bitrix24.ru/rest/1/wczorpkc6n2spne0/crm.product.list/')
# res = requests.get('https://proektsv.bitrix24.ru/rest/26/pcw309lfbp2d2d79/profile/')
# res = requests.get('https://proektsv.bitrix24.ru/rest/26/pcw309lfbp2d2d79/crm.product.list/')
# print(json.loads(res.content.decode('utf8')).get('result'))
# print(add_contact('Add', None, None, '+79685266354'))

# res = get_contact_list('+79685246354')
# print(res)
# https://proektsv.bitrix24.ru/rest/26/pcw309lfbp2d2d79/profile/

# res = requests.get('https://proektsv.bitrix24.ru/rest/26/pcw309lfbp2d2d79/crm.contact.list/')
# res = json.loads(res.content.decode('utf8')).get('result')
# for re in res:
#     print(re)

# def add_dea(name, contact_id, price):
#     data = {'fields': {
#         "TITLE": name,
#         "TYPE_ID": "GOODS",
#         "STAGE_ID": "NEW",
#         "COMPANY_ID": 1,
#         "CONTACT_ID": contact_id,
#         "OPENED": "YES",
#         "ASSIGNED_BY_ID": 26,
#         "PROBABILITY": 80,
#         "CURRENCY_ID": "RUB",
#         "OPPORTUNITY": price,
#         "BEGINDATE": time.time()
#     },
#         'params': {"REGISTER_SONET_EVENT": "Y"}}
#     response = requests.post('https://proektsv.bitrix24.ru/rest/26/pcw309lfbp2d2d79/crm.deal.add.json/', json=data)
#     results = json.loads(response.content.decode('utf8'))
#     return results
# print(add_dea('test', None, 150))
# NEW
# '1'
# WON


# # "crm.deal.get",
# id = {'id': 2110}
# res = requests.get('https://proektsv.bitrix24.ru/rest/26/pcw309lfbp2d2d79/crm.deal.get/', params=id)
# res = json.loads(res.content.decode('utf8')).get('result')
# print(res)
# # for re in res:
# #     print(re)
#
# res = requests.get('https://proektsv.bitrix24.ru/rest/26/pcw309lfbp2d2d79/crm.product.list/')
# res = json.loads(res.content.decode('utf8')).get('result')
# # print(res)
# for re in res:
#     print(re)
# print(get_deal_state({'id': 120}).get('result').get('STAGE_ID'))
# print(get_deal_list())

# print(get_contact_list(79285269999))
# 732
#
# [{'ID': '90', 'NAME': 'Маликат и Иман', 'PHONE':
#     [{'ID': '100', 'VALUE_TYPE': 'WORK', 'VALUE': '79282777609', 'TYPE_ID': 'PHONE'},
#      {'ID': '520', 'VALUE_TYPE': 'WORK', 'VALUE': '79188491359', 'TYPE_ID': 'PHONE'}]},
#  {'ID': '764', 'NAME': 'Iman', 'PHONE':
#      [{'ID': '1116', 'VALUE_TYPE': 'WORK', 'VALUE': '79188491359', 'TYPE_ID': 'PHONE'}]}]