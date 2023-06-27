from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

help_router = Router(name='help')

WELCOME_MESSAGE = '''
Welcome to the Currency Exchange Bot!🤖💱

You can use this bot to get information about currency exchange rates.
The bot will provide you with the exchange rate by date
If you need any assistance, just type /help and I'll be here to assist you!
'''

HELP_MESSAGE = '''
I'm here to help you with currency exchange rates! 💱
I'm use The Frankfurter API.
This API tracks foreign exchange references rates published by the European Central Bank.
The data refreshes around 16:00 CET every working day.
You can get exchange rate since 4 January 1999.
To get the exchange rate for a specific currency pair, type the /getcurrencies command


If you have any questions or need further assistance, feel free to ask @contact ! 😊
'''


@help_router.message(Command('start'))
async def get_start_information(message: Message): 
    await message.answer(text=WELCOME_MESSAGE)
    
    
    
@help_router.message(Command('help'))
async def get_help(message: Message):
    await message.answer(text=HELP_MESSAGE)