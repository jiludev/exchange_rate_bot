from datetime import date

from aiogram import Router, F, html
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


from aiogram3b8_calendar import SimpleCalCallback, SimpleCalendar

from structures.keyboards.currencies import get_currencies_ikb, Currency
from structures.api import get_currencies_data

currency_router = Router(name='currnecy')


class Exchange(StatesGroup):
    waiting_from_currency = State()
    waiting_to_currency =  State()
    waiting_for_date = State()


@currency_router.message(Command('getcurrencies'))
async def currency_command_handler(message: Message, state: FSMContext):
    if await state.get_state() is None:
    
        currencies = await get_currencies_data('currencies')

        await message.answer('Please choose a base currency',
                            reply_markup=get_currencies_ikb(currencies))

        await state.update_data(curs_data=currencies)
        await state.set_state(Exchange.waiting_from_currency)


@currency_router.callback_query(F.data == 'IGNORE')
async def answer_ignore_callback(query: CallbackQuery):
    await query.answer()


@currency_router.callback_query(Exchange.waiting_from_currency, Currency.filter())
async def base_currency_handler(query: CallbackQuery, state: FSMContext, callback_data: Currency):
    await state.update_data(from_cur=callback_data.name)
    await state.set_state(Exchange.waiting_to_currency)
    state_data = await state.get_data()
    curs_data = state_data.get('curs_data')
    await query.message.edit_text(f'Please choose related to {callback_data.name} currency',
                                  reply_markup=get_currencies_ikb(curs_data))
    await query.answer()
    
    
@currency_router.callback_query(Exchange.waiting_to_currency, Currency.filter())
async def related_currency_handler(query: CallbackQuery, state: FSMContext, callback_data: Currency):
    await state.update_data(to_cur=callback_data.name)
    await state.set_state(Exchange.waiting_for_date)
    state_data = await state.get_data()
    from_cur = state_data['from_cur']
    to_cur = callback_data.name
    await query.message.edit_text(f'Please choose a date for exchange rate <b>{from_cur} > {to_cur}</b>',
                                  reply_markup=SimpleCalendar.start_calendar(),
                                  parse_mode='html')
    await query.answer()
    
    
@currency_router.callback_query(Exchange.waiting_for_date, SimpleCalCallback.filter())
async def date_handler(query: CallbackQuery, state: FSMContext, callback_data: Currency):
    cur_date = await SimpleCalendar.process_selection(query, callback_data)
    state_data = await state.get_data()
    from_cur = state_data['from_cur']
    to_cur = state_data['to_cur']
    if cur_date:
        if date(1990, 1, 4) < cur_date <= date.today():
            cur_query = f'{cur_date.strftime("%Y-%m-%d")}?from={from_cur}&to={to_cur}'
            currency_rate = await get_currencies_data(cur_query)
            
            await query.message.edit_text(
                "Date: <code>{date}</code>\n\n\
                <code>{base}: {amount}</code>\n\
                <code>{related}: {.2f}</code>\n\n\n\
                /getcurrencies".format(currency_rate['rates'][to_cur],
                                       date=currency_rate['date'],
                                       base=currency_rate['base'],
                                       amount=currency_rate['amount'],
                                       related=list(currency_rate['rates'].keys())[0]),           
                parse_mode='html'
            )
            await state.clear()
        else:
            await query.message.edit_text(f'Please choose a <b>correct</b> for exchange rate <code>{from_cur} > {to_cur}</code>',
                                          parse_mode='html')        
    