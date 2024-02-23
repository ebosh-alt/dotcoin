from dataclasses import dataclass


@dataclass
class Withdrawal:
    count: int | None = None
    message_id: int | None = None
