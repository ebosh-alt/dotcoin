from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot import keyboards as kb
from bot.config import bot
from bot.db import configuration
from bot.states import States
from bot.utils.checks import check_is_float

router = Router()


@router.callback_query(F.data == "set_capitalization")
async def admin_set_capitalization(message: CallbackQuery, state: FSMContext):
    await state.clear()
    id = message.from_user.id
    await state.set_state(States.set_capitalization)
    await bot.edit_message_text(chat_id=id,
                                message_id=message.message.message_id,
                                text="Введите сумму изменения капитализации",
                                reply_markup=kb.back_admin_menu_kb)
    await state.update_data(message_id=message.message.message_id)


@router.message(States.set_capitalization)
async def mes_set_capitalization(message: Message, state: FSMContext):
    id = message.from_user.id
    data = await state.get_data()
    message_id = data["message_id"]
    if not check_is_float(message.text):
        await bot.edit_message_text(chat_id=id,
                                    message_id=message_id,
                                    text=f"Не правильно введены данные",
                                    reply_markup=kb.admin_menu_kb)
        return
    await state.update_data(capitalization=float(message.text))

    await message.delete()
    await bot.edit_message_text(chat_id=id,
                                message_id=message_id,
                                text=f"Введенные данные: {float(message.text)}",
                                reply_markup=kb.confirm_admin_kb)


@router.callback_query(States.set_capitalization, F.data == "yes_change")
async def confirm_ban_unban(message: CallbackQuery, state: FSMContext):
    id = message.from_user.id
    data = await state.get_data()
    message_id = data["message_id"]
    profit = data["capitalization"]
    config = configuration()
    config.all_profit += float(profit)
    config.all_profit = round(config.all_profit, 2)
    config.income += float(profit)
    configuration.save(config)
    await state.clear()
    await bot.edit_message_text(chat_id=id,
                                message_id=message_id,
                                text=f"Капитилизация изменена: `{config.all_profit + config.capitalization}`\n"
                                     f"Текущая прибыль: `{config.all_profit}`",
                                reply_markup=kb.admin_menu_kb)


set_capitalization_rt = router
