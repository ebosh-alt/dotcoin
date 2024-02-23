from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from bot import keyboards as kb
from bot.config import bot, admin_id
from bot.db import users
from bot.states import States
from bot.utils import Filters, SendGreeting
from bot.utils.GetMessage import get_mes

router = Router()


@router.callback_query(Filters.IsUser(), F.data == "change_requisites_user")
async def start(message: CallbackQuery, state: FSMContext):
    id = message.from_user.id
    await bot.edit_message_text(chat_id=id,
                                message_id=message.message.message_id,
                                text=get_mes("requisites"))
    await state.set_state(States.requisites)
    await state.update_data(message_id=message.message.message_id)


@router.message(Filters.IsUser(), States.requisites)
async def requisites(message: Message, state: FSMContext):
    id = message.from_user.id
    data = await state.get_data()
    message_id = data["message_id"]
    user = users.get(id)
    await message.delete()

    if user.requisites is None:
        await bot.delete_message(chat_id=id, message_id=message_id)
        user.requisites = message.text
        users.update(user)
        await SendGreeting.send(id)
        await state.clear()
    else:
        keyboard = kb.create_keyboard({"Подтвердить": f"yesRequisites{id}_{message.text}",
                                       "Отменить": f"noRequisites{id}_{message.text}"})

        await bot.send_message(chat_id=admin_id,
                               text=get_mes("new_requisites", user_id=id,
                                            username=f"@{user.username}" if user.username else "Отсутсвует username",
                                            requisites=user.requisites,
                                            new_requisites=message.text,
                                            count=user.count
                                            ),
                               reply_markup=keyboard)
        await bot.edit_message_text(chat_id=id,
                                    message_id=message_id,
                                    text="Ваша заявка на рассмотрении",
                                    reply_markup=kb.del_mes_kb)


requisites_rt = router
