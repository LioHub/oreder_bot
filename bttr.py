import requests, json, time

url_deal_add = 'https://testjj.bitrix24.ru/rest/1/wczorpkc6n2spne0/crm.deal.add.json/'

# Для добавления новой сделки
data = {'fields': {
    "TITLE": "Пакет на 3 месяца Вода 19л",
    "TYPE_ID": "GOODS",
    "STAGE_ID": "NEW",
    "COMPANY_ID": 1,
    # "CONTACT_ID": +79635896583,
    "CONTACT_ID": 7,
    "OPENED": "YES",
    "ASSIGNED_BY_ID": 1,
    "PROBABILITY": 10,
    "CURRENCY_ID": "RUB",
    "OPPORTUNITY": 140,
    "BEGINDATE": time.time(),
    "CLOSEDATE": time.time() + 1000
},
    'params': {"REGISTER_SONET_EVENT": "Y"}}

# a = requests.post(url, json=data)
# print('dd', json.loads(a.content.decode('utf8')))


# Для вывода списка сделок
a = requests.get('https://testjj.bitrix24.ru/rest/1/wczorpkc6n2spne0/crm.deal.list/')
results = json.loads(a.content.decode('utf8'))
for result in results.get('result'):
    print(result)


# Для вывода списка контактов
a = requests.get('https://testjj.bitrix24.ru/rest/1/wczorpkc6n2spne0/crm.contact.list/')
results = json.loads(a.content.decode('utf8'))
print(results)
for result in results.get('result'):
    print(result)


# Для добавления нового продукта(товара)
# dates = {'fields': {
#         "NAME": "Пакет 3 месяца",
#         "CURRENCY_ID": "RUB",
#         "PRICE": 130,
#         "SORT": 500
# }}
#
# a = requests.post('https://testjj.bitrix24.ru/rest/1/wczorpkc6n2spne0/crm.product.add.json/', json=dates)
# results = json.loads(a.content.decode('utf8'))
# print(results)
# # Для вывода списка товаров
a = requests.get('https://testjj.bitrix24.ru/rest/1/wczorpkc6n2spne0/crm.product.list/')
results = json.loads(a.content.decode('utf8'))
print(results)
for result in results.get('result'):
    print(result)
    # 'ID': '1', 'NAME': 'Water', 'ACTIVE'
    # {'ID': '3', 'NAME': 'Пакет 3 месяца'


# Добавление контактов
# data = {'fields':
#     {
#         "NAME": "Глеб",
#         "SECOND_NAME": "Егорович",
#         "LAST_NAME": "Титов",
#         "OPENED": "Y",
#         "ASSIGNED_BY_ID": 1,
#         "TYPE_ID": "CLIENT",
#         "SOURCE_ID": "SELF",
#         # "PHOTO": { "fileData": document.getElementById('photo') },
#         "PHONE": [{"VALUE": "555888", "VALUE_TYPE": "WORK"}]
#     },
#     'params': {"REGISTER_SONET_EVENT": "Y"}}
#
# a = requests.post('https://testjj.bitrix24.ru/rest/1/wczorpkc6n2spne0/crm.contact.add.json/', json=data)
# results = json.loads(a.content.decode('utf8'))
# print(results)



# /library
# from bitrix24 import Bitrix24
# bx24 = Bitrix24('testjj.bitrix24.ru', '1', '8StjNyW25rV30NZf27wKlmxdkiDOG1Up4gOLcDf2t2wianfRf6''local.5b90f1f62bf757.85852246'
#
#                 )
# print(bx24.call_method('crm.deal.list'))
# # print(bx24.call_method('crm.deal.add', fields))
#
# # Код приложения: local.5b90f1f62bf757.85852246
# #
# # Ключ приложения: 8StjNyW25rV30NZf27wKlmxdkiDOG1Up4gOLcDf2t2wianfRf6


# Добавление контактов
# data = {
#     'id': 57,
#     'rows':
#         [
#             # {"PRODUCT_ID": 689, "PRICE": 100.00, "QUANTITY": 4},
#             {"PRODUCT_ID": 9, "PRICE": 130.00, "QUANTITY": 42}
#         ]
# }

a = requests.post('https://testjj.bitrix24.ru/rest/1/wczorpkc6n2spne0/crm.deal.productrows.set.json/', json=data)
results = json.loads(a.content.decode('utf8'))
print(results)
#
# "crm.deal.productrows.set",
# {
#     id: id,
#     rows:
#         [
#             {"PRODUCT_ID": 689, "PRICE": 100.00, "QUANTITY": 4},
#             {"PRODUCT_ID": 690, "PRICE": 400.00, "QUANTITY": 1}
#         ]
# },


# Сделака
{'ID': '53',
 'TITLE': 'Пакет на 3 месяца Вода 19л',
 'TYPE_ID': 'GOODS',
 'STAGE_ID': 'NEW',
 'PROBABILITY': '10',
 'CURRENCY_ID': 'RUB',
 'OPPORTUNITY': '140.00',
 'TAX_VALUE': None,
 'LEAD_ID': None,
 'COMPANY_ID': '1',
 'CONTACT_ID': '7',
 'QUOTE_ID': None,
 'BEGINDATE': '2018-09-08T03:00:00+03:00',
 'CLOSEDATE': '',
 'ASSIGNED_BY_ID': '1',
 'CREATED_BY_ID': '1',
 'MODIFY_BY_ID': '1',
 'DATE_CREATE': '2018-09-08T16:04:42+03:00',
 'DATE_MODIFY': '2018-09-08T16:04:42+03:00',
 'OPENED': 'Y',
 'CLOSED': 'N',
 'COMMENTS': None,
 'ADDITIONAL_INFO': None,
 'LOCATION_ID': None,
 'CATEGORY_ID': '0',
 'STAGE_SEMANTIC_ID': 'P',
 'IS_NEW': 'Y',
 'IS_RECURRING': 'N',
 'IS_RETURN_CUSTOMER': 'Y',
 'ORIGINATOR_ID': None,
 'ORIGIN_ID': None,
 'UTM_SOURCE': None,
 'UTM_MEDIUM': None,
 'UTM_CAMPAIGN': None,
 'UTM_CONTENT': None,
 'UTM_TERM': None}