from aiogram import Router, F
from aiogram.types import CallbackQuery

from bot import keyboards as kb
from bot.config import bot
from bot.db import users, configuration
from bot.utils import SendGreeting
from bot.utils.GetMessage import get_mes

router = Router()


@router.callback_query((F.data.contains('yesWithdrawal') | (F.data.contains('noWithdrawal'))))
async def withdrawal_admin(message: CallbackQuery):
    id = message.from_user.id
    data = message.data.replace("yesWithdrawal", "").replace("noWithdrawal", "").split("_")
    id_user, count, amount = int(data[0]), int(data[1]), float(data[2])

    user = users.get(id_user)
    config = configuration()
    if "yesWithdrawal" in message.data:
        user.count -= count
        config.all_profit -= amount
        config.profit_today -= amount
        config.withdrawal += amount
        configuration.save(config)
        users.update(user)
        await bot.send_message(chat_id=id_user, text=get_mes("yes_withdrawal"), reply_markup=kb.del_mes_kb)
    else:
        await bot.send_message(chat_id=id_user, text=get_mes("no_withdrawal"), reply_markup=kb.del_mes_kb)
    await bot.answer_callback_query(callback_query_id=message.id,
                                    text=get_mes("answer_admin_user"),
                                    show_alert=False)
    await bot.delete_message(message_id=message.message.message_id, chat_id=id)
    await SendGreeting.send(id_user)


withdrawal_rt = router
