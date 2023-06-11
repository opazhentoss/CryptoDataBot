from aiogram import Dispatcher, types
from trendcollect import collect_data
from aiogram.utils.markdown import hlink, hbold


async def trend(message: types.Message):
    data = collect_data()
    for item in data:
        link_part = item.get("slug")
        link = f"https://coinmarketcap.com/ru/currencies/{link_part}/"
        answ = f'{hlink(item.get("name"), link)}\n' \
               f'{hbold("Price change24h: ")}{item.get("priceChange24h")}%\n'
        await message.answer(answ)


def register_handlers_trend(dp: Dispatcher):
    dp.register_message_handler(trend, commands="trend")
