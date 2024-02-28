import datetime

import matplotlib.pyplot as plt
from matplotlib import dates
from aiogram.types import FSInputFile


class Diagram:
    def __init__(self, value):
        self.path = "bot/db/diagram.png"
        self.value: list = value

    def __call__(self) -> FSInputFile:
        self.create_diagram()
        photo = FSInputFile(self.path)
        return photo

    def create_diagram(self) -> None:
        days = dates.DayLocator()
        time_fmt = dates.DateFormatter('%d.%m')
        bw = 0.7
        event = self.get_date()
        fig, ax = plt.subplots()
        plt.title('Инфографика')
        plt.ylim(0, max(self.value) + min(self.value))
        plt.bar(event[0], self.value[0], bw, color='g')
        for i in range(1, len(self.value)):
            if self.value[i] >= self.value[i - 1]:
                plt.bar(event[i], self.value[i], bw, color='g')
            else:
                plt.bar(event[i], self.value[i], bw, color='r')
        ax.xaxis.set_major_formatter(time_fmt)
        ax.xaxis.set_minor_locator(days)

        plt.savefig(self.path, bbox_inches="tight",
                    pad_inches=0.7, transparent=True)

    def get_date(self) -> list:
        now = datetime.datetime.now()
        event = []
        for i in range(len(self.value)-1, -1, -1):
            event_el = now - datetime.timedelta(days=i)
            year, month, day = event_el.year, event_el.month, event_el.day
            event.append(datetime.datetime(year, month, day))
        return event



