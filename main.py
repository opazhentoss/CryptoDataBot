import asyncio
import csv
from BTCupdates import btcprice_collect
from aiogram.types.bot_command import BotCommand
from aiogram.utils.exceptions import BotBlocked
from trend import register_handlers_trend
from MostSearch import register_handlers_searched
from BTCupdates import register_handlers_subscribe
import logging
from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

bot = Bot(token="Вставьте токен", parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())
logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/trend", description="Показать максимальные рост и падения за последние сутки"),
        BotCommand(command="/searched", description="Показать какие монеты чаще всего искали в последнее время"),
        BotCommand(command="/updates", description="Ежечасные уведомления о цене BTC")
    ]
    await bot.set_my_commands(commands)


@dp.errors_handler(exception=BotBlocked)
async def error_bot_blocked(update: types.Update, exception: BotBlocked):
    print(f"Меня заблокировал пользователь!\nСообщение: {update}\nОшибка: {exception}")
    return True


@dp.callback_query_handler(text="subscribe")
async def subscribe(call: types.CallbackQuery):
    user_id_str = str(call.from_user.id)
    user_id = [user_id_str]
    detector = 0
    with open('users_id.csv', 'r') as users_id:
        user_reader = csv.reader(users_id)
        for row in user_reader:
            if row == user_id:
                detector = 1

    if detector == 0:
        with open(r'users_id.csv', 'a') as users_id:
            user_writer = csv.writer(users_id)
            user_writer.writerow(user_id)
        await call.message.answer("Вы подписались на уведомления по изменению цены Bitcoin")
        await call.answer()
    else:
        await call.message.answer("Вы уже подписаны")
        await call.answer()


async def notifications(sleep_for):
    while True:
        await asyncio.sleep(sleep_for)
        with open('users_id.csv', 'r') as users_id:
            user_reader = csv.reader(users_id)
            for row in user_reader:
                chat = int(row[0])
                price = btcprice_collect()
                await bot.send_message(chat, f"{price}")

async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    logger.error("Starting bot")

    register_handlers_trend(dp)
    register_handlers_searched(dp)
    register_handlers_subscribe(dp)
    loop = asyncio.get_event_loop()
    loop.create_task(notifications(3600))
    await set_commands(bot)
    await dp.skip_updates()
    await dp.start_polling()


if __name__ == '__main__':
    asyncio.run(main())