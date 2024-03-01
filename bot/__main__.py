import asyncio
import schedule
import logging
from time import sleep
from threading import Thread

from bot.db import configuration
from bot.handlers import routers
from bot.config import bot, dp

stop = True


async def main() -> None:
    for router in routers:
        dp.include_router(router)

    await dp.start_polling(bot)


def schedule_checker():
    global stop
    while stop is True:
        schedule.run_pending()
        sleep(1)


def clear_profit_today():
    print("clear")
    config = configuration()
    del config.statistics_diagram[0]
    config.statistics_diagram.append(config.turnover)
    config.course = round(config.course + (config.income_today / config.turnover_yesterday), 2)
    config.income_yesterday = config.income_today
    config.turnover_yesterday = config.turnover
    config.income_today = 0
    configuration.save(config)


if __name__ == "__main__":
    try:
        logging.basicConfig(level=logging.INFO,
                            filename="logging.log",
                            filemode="w",
                            format="%(levelname)s %(asctime)s %(message)s",
                            encoding='utf-8')
        schedule.every().day.at("21:00").do(clear_profit_today)
        thr = Thread(target=schedule_checker)
        thr.start()
        asyncio.run(main())
    except KeyboardInterrupt:
        stop = False
