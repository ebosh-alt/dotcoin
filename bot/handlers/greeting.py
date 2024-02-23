from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot import keyboards as kb
from bot.config import bot, link_to_bot, ref_award, admin_id
from bot.db import users, User
from bot.states import States
from bot.utils import SendNotifications, Filters, SendGreeting
from bot.utils.GetMessage import get_mes

router = Router()


@router.message(Filters.IsUser(), Command("start"))
async def greeting_user(message: Message, state: FSMContext):
    id = message.from_user.id
    if id not in users:
        user = User(id=id)
        user.name = message.from_user.first_name
        user.username = message.from_user.username
        user.ref_link = f"{link_to_bot}?start={id}"
        ref_bos = message.text.split()[-1]
        if ref_bos.isdigit():
            ref_bos_id = int(ref_bos)
            ref_bos = users.get(ref_bos_id)
            ref_bos.balance += ref_award
            ref_bos.all_balance += ref_award
            await SendNotifications.send(id=ref_bos_id, text=get_mes("ref_award", amount=ref_award))
            mes = await bot.send_message(chat_id=admin_id,
                                         text=get_mes("ref_award_admin",
                                                      user_id=ref_bos_id,
                                                      username=f"@{ref_bos.username}" if ref_bos.username else "Отсутсвует username",
                                                      requisites=ref_bos.requisites,
                                                      count=ref_award,
                                                      all_coin=ref_bos.count),
                                         reply_markup=kb.del_mes_kb)
            await state.set_state(States.requisites)
            await state.update_data(message_id=mes.message_id)
            users.update(ref_bos)
        mes = await bot.send_message(chat_id=id, text=get_mes("requisites"))
        await state.set_state(States.requisites)
        await state.update_data(message_id=mes.message_id)
        users.add(user)
    else:
        user = users.get(id)
        if message.from_user.username != user.username:
            user.username = message.from_user.username
            users.update(user)
        await SendGreeting.send(id)
        await state.clear()


greeting_rt = router
