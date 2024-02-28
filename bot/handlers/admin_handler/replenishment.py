from aiogram import Router, F
from aiogram.types import CallbackQuery

from bot import keyboards as kb
from bot.config import bot, link_chat
from bot.db import users, configuration
from bot.utils import SendGreeting
from bot.utils.GetMessage import get_mes

router = Router()


@router.callback_query((F.data.contains('yesReplenishment') | (F.data.contains('noReplenishment'))))
async def payment(message: CallbackQuery):
    id = message.from_user.id
    data = message.data.replace("yesReplenishment", "").replace("noReplenishment", "").split("_")
    id_user, count, amount = int(data[0]), int(data[1]), float(data[2])
    user = users.get(id_user)
    config = configuration()
    if "yesReplenishment" in message.data:
        user.count += count
        config.turnover += amount
        config.turnover_users += amount
        config.replenishment += amount
        if not user.buy:
            await bot.send_message(chat_id=id_user, text=get_mes("first_buy", link=link_chat), reply_markup=kb.del_mes_kb)
            user.buy = True
        await bot.send_message(chat_id=id_user, text=get_mes("yes_replenishment"), reply_markup=kb.del_mes_kb)
        users.update(user)
        configuration.save(config)
    else:
        await bot.send_message(chat_id=id_user, text=get_mes("no_replenishment"), reply_markup=kb.del_mes_kb)
    await bot.answer_callback_query(callback_query_id=message.id,
                                    text=get_mes("answer_admin_user"),
                                    show_alert=False)
    await bot.delete_message(message_id=message.message.message_id, chat_id=id)
    await SendGreeting.send(id_user)


replenishment_rt = router
