#!/usr/bin/env python
# coding=utf-8

from button import contact_menu
from button import location_menu
from button import back_to_main_menu
from button import inline_main_menu
from button import inline_order_water
from button import inline_basket_menu
from button import inline_admin_menu
from button import inline_instruction_menu
from button import inline_back_menu
from button import inline_location_menu
from button import inline_confirm_menu
from button import inline_basket_empty_menu
from button import inline_cancel_menu
from button import inline_confirm_deliver_menu
from button import inline_pompa_menu
from button import inline_backer_menu
from button import inline_packages_menu
from button import inline_cin_pack_menu
from button import inline_pack_bottle_menu
from button import inline_confirm_pack_menu
from button import inline_replay_confirm
from button import inline_comment_menu
from button import inline_pre_payment_menu

# provider_token = '390540012:LIVE:4167'
provider_token = '390540012:LIVE:4565'  # - origin
users = {}
prices = {0: []}

menu = {
    1: {'button': inline_main_menu(), 'index': 1},
    2: {'button': inline_order_water('order'), 'index': 2},
    3: {'button': inline_basket_menu(), 'index': 3},
    4: {'button': inline_admin_menu(), 'index': 4},
    5: {'button': inline_instruction_menu(), 'index': 5},
    6: {'button': contact_menu(), 'index': 6},
    7: {'button': inline_back_menu('back_to_main_menu_del'), 'index': 7},
    8: {'button': inline_location_menu("back_to_order"), 'index': 8},
    9: {'button': location_menu(), 'index': 9},
    10: {'button': inline_confirm_menu(), 'index': 10},
    11: {'button': inline_basket_empty_menu(), 'index': 11},
    12: {'button': inline_cancel_menu(), 'index': 12},
    13: {'button': inline_confirm_deliver_menu(), 'index': 13},
    14: {'button': inline_order_water('pompa'), 'index': 14},
    15: {'button': inline_pompa_menu(), 'index': 15},
    16: {'button': inline_back_menu('back_to_main_menu_del'), 'index': 16},
    17: {'button': inline_backer_menu(), 'index': 17},
    18: {'button': inline_packages_menu('package'), 'index': 18},
    19: {'button': inline_cin_pack_menu('to_packages'), 'index': 19},
    20: {'button': inline_pack_bottle_menu(), 'index': 20},
    21: {'button': inline_cin_pack_menu('to_show_pack_bottle'), 'index': 21},
    22: {'button': inline_location_menu("back_to_package_bottle"), 'index': 22},
    23: {'button': inline_location_menu("back_to_package_bottle"), 'index': 23},
    24: {'button': back_to_main_menu(), 'index': 24},
    25: {'button': inline_confirm_pack_menu(), 'index': 25},
    27: {'button': inline_replay_confirm(), 'index': 27},
    28: {'button': inline_comment_menu(), 'index': 28},
    29: {'button': inline_packages_menu('bottles'), 'index': 29},
    30: {'button': inline_pre_payment_menu(), 'index': 30}
}