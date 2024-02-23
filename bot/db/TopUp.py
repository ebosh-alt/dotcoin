from dataclasses import dataclass, field


@dataclass
class TopUp:
    count: int = 0
    amount: float = 0.0
    message_id: int = 0
