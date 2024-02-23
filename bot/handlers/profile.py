from aiogram import Router, F
from aiogram.types import CallbackQuery

from bot import keyboards as kb
from bot.config import bot
from bot.db import users
from bot.utils import Filters
from bot.utils.GetMessage import get_mes

router = Router()


@router.callback_query(Filters.IsUser(), F.data == "profile")
async def profile(message: CallbackQuery):
    id = message.from_user.id
    user = users.get(id)

    await bot.edit_message_text(message_id=message.message.message_id,
                                chat_id=id,
                                text=get_mes("profile",
                                             username=user.username,
                                             id=user.id,
                                             # balance=user.count,
                                             # allBalance=user.all_balance,
                                             countCoin=user.count,
                                             requisites=user.requisites),
                                reply_markup=kb.profile_kb)

profile_rt = router