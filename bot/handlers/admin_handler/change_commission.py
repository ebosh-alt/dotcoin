from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot import keyboards as kb
from bot.config import bot
from bot.db import configuration
from bot.states import States
from bot.utils.checks import check_is_float

router = Router()


@router.callback_query(F.data == "change_commission")
async def admin_change_commission(message: CallbackQuery, state: FSMContext):
    await state.clear()
    id = message.from_user.id
    await bot.edit_message_text(chat_id=id,
                                message_id=message.message.message_id,
                                text="Введите новый курс")
    await state.set_state(States.change_commission)
    await state.update_data(message_id=message.message.message_id)


@router.message(States.change_commission)
async def mes_change_commission(message: Message, state: FSMContext):
    id = message.from_user.id
    data = await state.get_data()
    message_id = data["message_id"]
    if not check_is_float(message.text):
        await message.delete()
        await bot.edit_message_text(chat_id=id,
                                    message_id=message_id,
                                    text=f"Не правильно введены данные",
                                    reply_markup=kb.admin_menu_kb)
        return
    await state.update_data(commission=float(message.text))
    await message.delete()
    await bot.edit_message_text(chat_id=id,
                                message_id=message_id,
                                text=f"Введенные данные: {float(message.text)}",
                                reply_markup=kb.confirm_admin_kb)


@router.callback_query(States.change_commission, F.data == "yes_change")
async def confirm_ban_unban(message: CallbackQuery, state: FSMContext):
    id = message.from_user.id
    data = await state.get_data()
    message_id = data["message_id"]
    commission = data["commission"]
    config = configuration()
    config.commission = commission
    configuration.save(config)
    await state.clear()
    await bot.edit_message_text(chat_id=id,
                                message_id=message_id,
                                text=f"Установлен новая комиссия: `{config.commission}`",
                                reply_markup=kb.admin_menu_kb)


change_commission_rt = router
