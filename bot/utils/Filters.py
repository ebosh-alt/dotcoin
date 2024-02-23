from aiogram import Router
from aiogram.filters import Filter
from aiogram.types import Message, User

from bot.config import admin_id
from bot.db import users

router = Router()


class IsAdmin(Filter):
    async def __call__(self, message: Message, event_from_user: User) -> bool:
        if event_from_user.id == admin_id:
            return True
        return False


class IsUser(Filter):
    async def __call__(self, message: Message, event_from_user: User) -> bool:
        if event_from_user.id not in users:
            return True
        user = users.get(event_from_user.id)
        return bool(user.status)
