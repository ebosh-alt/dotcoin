import json
from dataclasses import dataclass
from typing import Optional


@dataclass
class Config:
    start_capital: float = 0.0
    income_yesterday: float = 0.0
    income_today: float = 0.0
    income_all: float = 0.0
    withdrawal: float = 0.0
    replenishment: float = 0.0
    turnover_users: float = 0.0
    turnover: float = 0.0
    turnover_yesterday: float = 0.0
    turnover_today: float = 0.0
    course: float = 0.0
    commission: float = 0.0
    statistics_diagram: Optional[list] = None
    info_text: Optional[str] = None
    path_photo: Optional[str] = None
    requisites: Optional[str] = None


class Configuration:
    def __init__(self, path: str):
        self.path = path

    def __call__(self) -> Config:
        data = self.get()
        config: Config = Config(
            data["start_capital"],
            data["income_yesterday"],
            data["income_today"],
            data["income_all"],
            data["withdrawal"],
            data["replenishment"],
            data["turnover_users"],
            data["turnover"],
            data["turnover_yesterday"],
            data["turnover_today"],
            data["course"],
            data["commission"],
            data["statistics_diagram"],
            data["info_text"],
            data["path_photo"],
            data["requisites"],
        )
        return config

    def get(self) -> dict:
        with open(self.path, "r+", encoding="UTF-8") as f:
            obj: dict = json.load(f)
        return obj

    def save(self, obj) -> None:
        with open(self.path, "w+", encoding="UTF-8") as f:
            json.dump(obj.__dict__, f, indent=4)

    def new_config(self):
        config = Config()
        self.save(config)


if __name__ == '__main__':
    a = Configuration("D:/telegram_bots/dotcoin/bot/db/configuration.json")
    print(a())
