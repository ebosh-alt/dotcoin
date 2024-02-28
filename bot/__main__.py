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
    config = configuration()
    config.profit_today = 0
    if len(config.capitalization_statistics) > 12:
        del config.capitalization_statistics[0]
        config.capitalization_statistics.append(config.turnover)
    else:
        config.capitalization_statistics.append(config.turnover)
    config.income_yesterday = config.income
    config.turnover_yesterday = config.turnover
    configuration.save(config)




if __name__ == "__main__":
    try:
        logging.basicConfig(level=logging.INFO,
                            # filename=""
                            filemode="w",
                            format="%(levelname)s %(asctime)s %(message)s",
                            encoding='utf-8')
        # check_by_diagram()
        schedule.every().day.at("00:00").do(clear_profit_today)
        thr = Thread(target=schedule_checker)
        thr.start()
        asyncio.run(main())
    except KeyboardInterrupt:
        stop = False
