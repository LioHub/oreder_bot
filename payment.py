# import telebot
# from telebot.types import LabeledPrice
# from telebot.types import ShippingOption
#
#
# provider_token = '390540012:LIVE:4167'  # @BotFather -> Bot Settings -> Payments 390540012:LIVE:4167
# # prices = [LabeledPrice(label='Working Time Machine', amount=1000), LabeledPrice('Gift wrapping', 500)]
# prices = [LabeledPrice(label='Working Time Machine', amount=6000)]
#
# # shipping_options = [
# #     ShippingOption(id='instant', title='WorldWide Teleporter').add_price(LabeledPrice('Teleporter', 1000)),
# #     ShippingOption(id='pickup', title='Local pickup').add_price(LabeledPrice('Pickup', 300))]
#
#
# # a = ShippingOption(id='instant', title='WorldWide Teleporter')
# # a.add_price(LabeledPrice('Teleporter', 1000))
# # b = ShippingOption(id='pickup', title='Local pickup')
# # b.add_price(LabeledPrice('Pickup', 300))
# # shipping_options = [a, b]
#
#
# @bot.message_handler(commands=['buy'])
# def command_pay(message):
#     bot.send_message(message.chat.id,
#                      "Real cards won't work with me, no money will be debited from your account."
#                      " Use this test card number to pay for your Time Machine: `4242 4242 4242 4242`"
#                      "\n\nThis is your demo invoice:", parse_mode='Markdown')
#     bot.send_invoice(message.chat.id, title='Working Time Machine',
#                      description='Want to visit your great-great-great-grandparents?'
#                                  ' Make a fortune at the races?'
#                                  ' Shake hands with Hammurabi and take a stroll in the Hanging Gardens?'
#                                  ' Order our Working Time Machine today!',
#                      provider_token=provider_token,
#                      currency='RUB',
#                      photo_url='http://erkelzaar.tsudao.com/models/perrotta/TIME_MACHINE.jpg',
#                      photo_height=512,  # !=0/None or picture won't be shown
#                      photo_width=512,
#                      photo_size=512,
#                      is_flexible=False,  # True If you need to set up Shipping Fee
#                      prices=prices,
#                      start_parameter='time-machine-example',
#                      invoice_payload='HAPPY FRIDAYS COUPON')
#
#
# # @bot.shipping_query_handler(func=lambda query: True)
# # def shipping(shipping_query):
# #     print(shipping_query)
# #     bot.answer_shipping_query(shipping_query.id, ok=True, shipping_options=shipping_options,
# #                               error_message='Oh, seems like our Dog couriers are having a lunch right now. Try again later!')
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