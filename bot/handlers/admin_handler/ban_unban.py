import os

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, FSInputFile

from bot import keyboards as kb
from bot.config import bot
from bot.db import users
from bot.states import States
from bot.utils import GetUsers

router = Router()


@router.callback_query(F.data == "ban_unban")
async def admin_ban_unban(message: CallbackQuery, state: FSMContext):
    await state.clear()
    id = message.from_user.id
    await state.set_state(States.ban_unban)
    path = GetUsers.excel_user()
    mes = await bot.send_document(chat_id=id, document=FSInputFile(path))
    await bot.edit_message_text(chat_id=id,
                                message_id=message.message.message_id,
                                text="Введите user id нужного пользователя",
                                reply_markup=kb.back_admin_menu_kb)
    await state.update_data(message_id=[message.message.message_id, mes.message_id])
    os.remove(path)


@router.message(States.ban_unban)
async def admin_ban_unban(message: Message, state: FSMContext):
    id = message.from_user.id
    data = await state.get_data()
    message_id = data["message_id"]
    user_id = int(message.text)
    await message.delete()
    await state.update_data(user_id=user_id)
    await bot.delete_message(chat_id=id, message_id=message_id[1])
    await bot.edit_message_text(chat_id=id,
                                message_id=message_id[0],
                                text=f"Введенные данные: {user_id}",
                                reply_markup=kb.confirm_admin_kb)


@router.callback_query(States.ban_unban, F.data == "yes_change")
async def confirm_ban_unban(message: CallbackQuery, state: FSMContext):
    id = message.from_user.id
    data = await state.get_data()
    message_id = data["message_id"]
    user_id = data["user_id"]
    user = users.get(user_id)
    user.status = not user.status
    users.update(user)
    await state.clear()
    await bot.edit_message_text(chat_id=id,
                                message_id=message_id[0],
                                text=f"Статус пользователя `{message.text}` изменен",
                                reply_markup=kb.admin_menu_kb)


ban_unban_rt = router
