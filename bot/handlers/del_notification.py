from aiogram import Router, F
from aiogram.types import CallbackQuery

from bot.config import bot

router = Router()


@router.callback_query(F.data == "del_notification")
async def del_notification(message: CallbackQuery):
    await bot.delete_message(message_id=message.message.message_id, chat_id=message.from_user.id)

del_notification_rt = router
