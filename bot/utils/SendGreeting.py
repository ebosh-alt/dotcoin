import random

from aiogram.types import CallbackQuery, FSInputFile

from bot.config import bot
from bot.db import configuration
from bot.utils.GetMessage import get_mes
from bot import keyboards as kb
from bot.utils.Diagram import Diagram
import datetime

import matplotlib.pyplot as plt


async def send(id: int, message: CallbackQuery = None):
    config = configuration()
    if config.turnover_users == 0:
        percent = 0
    else:
        percent = round(config.turnover_users * 100 / config.turnover, 2)
    value = config.statistics_diagram
    value.append(config.turnover_today)
    dm = Diagram(value=value)
    photo = dm()
    if type(message) is CallbackQuery:
        await bot.delete_message(chat_id=id, message_id=message.message.message_id)
    await bot.send_photo(chat_id=id,
                         photo=photo,
                         caption=get_mes("greeting",
                                         turnover=config.turnover,
                                         turnoverUsers=config.turnover_users,
                                         percent=percent,
                                         replenishment=config.replenishment,
                                         withdrawal=config.withdrawal,
                                         income=config.income_all,
                                         course=config.course),
                         reply_markup=kb.greeting_kb)
