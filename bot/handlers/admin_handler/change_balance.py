import os

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, FSInputFile

from bot import keyboards as kb
from bot.config import bot
from bot.db import users
from bot.states import States
from bot.utils import GetUsers
from bot.utils.checks import check_is_float

router = Router()


@router.callback_query(F.data == "change_balance")
async def admin_change_balance(message: CallbackQuery, state: FSMContext):
    await state.clear()
    id = message.from_user.id
    await state.set_state(States.change_balance)
    path = GetUsers.excel_user()
    mes = await bot.send_document(chat_id=id, document=FSInputFile(path))
    await bot.edit_message_text(chat_id=id,
                                message_id=message.message.message_id,
                                text="Введите user id нужного пользователя и сумму изменения баланса",
                                reply_markup=kb.back_admin_menu_kb)
    await state.update_data(message_id=[message.message.message_id, mes.message_id])
    os.remove(path)


@router.callback_query(States.change_balance)
async def mes_change_balance(message: Message, state: FSMContext):
    data = await state.get_data()
    message_id = data["message_id"]
    id = message.from_user.id
    user_id, amount = message.text.split(" ")
    if user_id not in users or not check_is_float(amount):
        await bot.edit_message_text(chat_id=id,
                                    message_id=message_id[0],
                                    text="Не правильно введены данные",
                                    reply_markup=kb.admin_menu_kb)
        return
    user_id = int(user_id)
    amount = int(amount)
    user = users.get(user_id)
    user.count -= amount
    # user.balance += amount
    # user.all_balance += amount
    users.update(user)
    await message.delete()
    await bot.delete_message(chat_id=id, message_id=message_id[1])
    await bot.edit_message_text(chat_id=id,
                                message_id=message_id[0],
                                text="Баланс успешно изменен",
                                reply_markup=kb.admin_menu_kb)


change_balance_rt = router
