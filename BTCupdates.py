from aiogram import Dispatcher, types
from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent

agent = UserAgent()


async def cmd_subscribe(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Подписаться", callback_data="subscribe"))
    await message.answer("Подписаться на уведомления?", reply_markup=keyboard)


def btcprice_collect():
    response = requests.get(
        url='https://coinmarketcap.com/currencies/bitcoin/',
        headers={'user-agent': f'{agent.random}'})
    soup = BeautifulSoup(response.text, "html.parser")
    price = soup.find('meta', property ='og:description' )
    price_rez = price['content']
    return price_rez


def register_handlers_subscribe(dp: Dispatcher):
    dp.register_message_handler(cmd_subscribe, commands="updates")
