from aiogram import Router, F
from aiogram.types import CallbackQuery

from bot.utils import SendGreeting

router = Router()


@router.callback_query(F.data == "back_to_start")
async def back_to_start(message: CallbackQuery):
    id = message.from_user.id
    await SendGreeting.send(id, message)


bacs_rt = router
