from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot import keyboards as kb
from bot.config import bot
from bot.db import configuration
from bot.states import States
from bot.utils.checks import check_is_float

router = Router()


@router.callback_query(F.data == "new_income")
async def admin_set_capitalization(message: CallbackQuery, state: FSMContext):
    await state.clear()
    id = message.from_user.id
    await state.set_state(States.new_income)
    await bot.edit_message_text(chat_id=id,
                                message_id=message.message.message_id,
                                text="Введите сумму изменения капитализации",
                                reply_markup=kb.back_admin_menu_kb)
    await state.update_data(message_id=message.message.message_id)


@router.message(States.new_income)
async def mes_set_capitalization(message: Message, state: FSMContext):
    id = message.from_user.id
    data = await state.get_data()
    message_id = data["message_id"]
    if not check_is_float(message.text):
        await bot.edit_message_text(chat_id=id,
                                    message_id=message_id,
                                    text="Не правильно введены данные",
                                    reply_markup=kb.admin_menu_kb)
        return
    await state.update_data(income=float(message.text))

    await message.delete()
    await bot.edit_message_text(chat_id=id,
                                message_id=message_id,
                                text=f"Введенные данные: {float(message.text)}",
                                reply_markup=kb.confirm_admin_kb)


@router.callback_query(States.new_income, F.data == "yes_change")
async def confirm_ban_unban(message: CallbackQuery, state: FSMContext):
    id = message.from_user.id
    data = await state.get_data()
    message_id = data["message_id"]
    income = data["income"]
    config = configuration()
    config.income_today += income
    config.income_all += income
    config.turnover += income
    config.turnover_today += income
    configuration.save(config)
    await state.clear()
    await bot.edit_message_text(chat_id=id,
                                message_id=message_id,
                                text=f"Капитилизация изменена: `{config.turnover}`\n"
                                     f"Прибыль за сегодня: `{config.income_today}`"
                                     f"Общая прибыль: `{config.income_all}`",
                                reply_markup=kb.admin_menu_kb)

new_income_rt = router
