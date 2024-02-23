from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot import keyboards as kb
from bot.config import bot
from bot.db import configuration
from bot.states import States

router = Router()


@router.callback_query(F.data == "change_requisites")
async def admin_change_requisites(message: CallbackQuery, state: FSMContext):
    await state.clear()
    id = message.from_user.id
    await state.set_state(States.change_requisites)
    await state.update_data(message_id=message.message.message_id)
    await bot.edit_message_text(chat_id=id,
                                message_id=message.message.message_id,
                                text="Введите новые реквизиты",
                                reply_markup=kb.back_admin_menu_kb)


@router.message(States.change_requisites)
async def mes_change_requisites(message: Message, state: FSMContext):
    id = message.from_user.id
    data = await state.get_data()
    message_id = data["message_id"]
    await state.update_data(requisites=message.text)
    await message.delete()
    await bot.edit_message_text(chat_id=id,
                                message_id=message_id,
                                text=f"Введенные данные: {message.text}",
                                reply_markup=kb.confirm_admin_kb)


@router.callback_query(States.change_requisites, F.data == "yes_change")
async def confirm_ban_unban(message: CallbackQuery, state: FSMContext):
    id = message.from_user.id
    data = await state.get_data()
    message_id = data["message_id"]
    requisites = data["requisites"]
    config = configuration()
    config.requisites = requisites
    configuration.save(config)
    await state.clear()

    await bot.edit_message_text(chat_id=id,
                                message_id=message_id,
                                text=f"Установлены новые реквизиты: `{config.requisites}`",
                                reply_markup=kb.admin_menu_kb)


change_requisites_rt = router
