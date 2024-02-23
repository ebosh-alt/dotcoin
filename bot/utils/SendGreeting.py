from aiogram.types import CallbackQuery

from bot.config import bot
from bot.db import configuration
from bot.utils.GetMessage import get_mes
from bot import keyboards as kb


async def send(id: int, message: CallbackQuery = None):
    config = configuration()
    all_capital = config.capitalization + config.all_profit
    prev_capital = config.capitalization + config.all_profit - config.profit_today
    percent = round(((all_capital - prev_capital) / prev_capital) * 100, 2)

    if type(message) is CallbackQuery:
        await bot.delete_message(chat_id=id, message_id=message.message.message_id)
    await bot.send_message(chat_id=id,
                           text=get_mes("greeting",
                                        capitalization=config.capitalization + config.all_profit,
                                        profit=round(config.profit_today, 2),
                                        percent=percent,
                                        replenishment=config.replenishment,
                                        withdrawal=round(config.withdrawal, 2),
                                        income=config.income),
                           reply_markup=kb.greeting_kb)
