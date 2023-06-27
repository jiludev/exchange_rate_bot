from typing import List

import numpy as np

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from aiogram.filters.callback_data import CallbackData





class Currency(CallbackData, prefix='cur'):
    name: str

    


def split_list(lst: list, n: int):
    res = []
    res_temp = []
    for i, el in enumerate(lst):
        res_temp.append(el)
        if (i+1) % n == 0:
            res.append(res_temp)
            res_temp = []
    res.append(res_temp)
    return res

def get_currencies_ikb(data: dict):

    builder = InlineKeyboardBuilder()
    curs_arr = split_list(list(sorted(data.keys())), 6)
    last_row = curs_arr.pop()
    for row in curs_arr:
        builder.row(
            *[InlineKeyboardButton(text=el, callback_data=Currency(name=el).pack()) for el in row], 
            width=6
        )
    
    if last_length := len(last_row) < 6:
        builder.row(
            *[InlineKeyboardButton(text=el, callback_data=Currency(name=el).pack()) for el in last_row],
            *[InlineKeyboardButton(text=' ', callback_data='IGNORE') for _ in range(6 - last_length)],
            width=6
        ) 
    
    
    return builder.as_markup()        
        
        