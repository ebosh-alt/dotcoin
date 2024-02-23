import json
from dataclasses import dataclass


@dataclass
class Config:
    requisites: str = None
    commission: float = 1.5
    capitalization: float = 5000.00
    course: float = 0.1
    profit_today: float = 0.0
    all_profit: float = 0.0
    income: float = 0.0
    replenishment: float = 0.0
    withdrawal: float = 0.0
    info_text: str = None
    path_photo: str = None


class Configuration:
    def __init__(self, path: str):
        self.path = path

    def __call__(self) -> Config:
        data = self.get()
        config: Config = Config(data["requisites"],
                                data["commission"],
                                data["capitalization"],
                                data["course"],
                                data["profit_today"],
                                data["all_profit"],
                                data["income"],
                                data["replenishment"],
                                data["withdrawal"],
                                data["info_text"],
                                data["path_photo"],
                                )
        return config

    def get(self) -> dict:
        with open(self.path, "r+", encoding="UTF-8") as f:
            obj = json.load(f)
        return obj

    def save(self, obj) -> None:
        with open(self.path, "w+", encoding="UTF-8") as f:
            json.dump(obj.__dict__, f, indent=4)

    def new_config(self):
        config = Config()
        self.save(config)
