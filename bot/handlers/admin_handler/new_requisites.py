from aiogram import Router, F
from aiogram.types import CallbackQuery

from bot import keyboards as kb
from bot.config import bot
from bot.db import users, configuration
from bot.utils import SendGreeting
from bot.utils.GetMessage import get_mes

router = Router()


@router.callback_query((F.data.contains('yesRequisites') | (F.data.contains('noRequisites'))))
async def new_requisites_admin(message: CallbackQuery):
    id = message.from_user.id
    data = message.data.replace("yesRequisites", "").replace("noRequisites", "").split("_")
    id_user, requisites = int(data[0]), data[1]

    user = users.get(id_user)
    if "yesRequisites" in message.data:
        user.requisites = requisites
        users.update(user)
        await bot.send_message(chat_id=id_user, text=get_mes("yes_requisites"), reply_markup=kb.del_mes_kb)
    else:
        await bot.send_message(chat_id=id_user, text=get_mes("no_requisites"), reply_markup=kb.del_mes_kb)
    await bot.answer_callback_query(callback_query_id=message.id,
                                    text=get_mes("answer_admin_user"),
                                    show_alert=False)
    await bot.delete_message(message_id=message.message.message_id, chat_id=id)

    await SendGreeting.send(id_user)


new_requisites_rt = router
