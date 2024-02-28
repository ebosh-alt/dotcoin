from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, FSInputFile

from bot.config import bot, admin_id
from bot.db import users, configuration
from bot.db.Withdrawal import Withdrawal
from bot.keyboards import create_keyboard
from bot.states import States
from bot.utils import Filters
from bot.utils.GetMessage import get_mes
from bot import keyboards as kb

router = Router()


@router.callback_query(Filters.IsUser(), F.data == "withdraw_balance")
async def withdrawal_balance(message: CallbackQuery, state: FSMContext):
    id = message.from_user.id
    user = users.get(id)
    await state.set_state(States.withdrawal)
    await bot.edit_message_text(chat_id=id,
                                message_id=message.message.message_id,
                                text=get_mes("withdrawal_count", count=user.count))
    withdrawal = Withdrawal(message_id=message.message.message_id)

    await state.update_data(withdrawal=withdrawal)


@router.message(States.withdrawal, F.content_type.in_({'text'}))
async def input_coin_requisites(message: Message, state: FSMContext):
    id = message.from_user.id
    user = users.get(id)
    data = await state.get_data()
    withdrawal = data["withdrawal"]
    config = configuration()
    count = int(message.text)
    if count > user.count:
        await bot.edit_message_text(chat_id=id,
                                    message_id=withdrawal.message_id,
                                    text=get_mes("error_withdrawal.md", count=user.count))
        return
    withdrawal.count = count
    withdrawal.amount = float(
        withdrawal.count * round(config.course + config.income_yesterday / config.turnover_yesterday,
                                 2))
    await bot.edit_message_text(chat_id=id,
                                message_id=withdrawal.message_id,
                                text=get_mes("withdrawal_receipts",
                                             count=withdrawal.count,
                                             requisites=config.requisites,
                                             amount=round(withdrawal.amount * (1 - config.commission / 100), 2)))
    await bot.delete_message(chat_id=id, message_id=message.message_id)
    await state.update_data(withdrawal=withdrawal)


@router.message(States.withdrawal, F.photo)
async def receipts_withdrawal(message: Message, state: FSMContext):
    id = message.from_user.id
    user = users.get(id)
    data = await state.get_data()
    withdrawal = data["withdrawal"]
    file = message.photo[-1]
    path = f"bot/receipts/withdrawal/{message.photo[-1].file_id}_{message.message_id}.jpg"
    await bot.download(
        file=file,
        destination=path
    )
    photo = FSInputFile(path)
    await state.update_data(withdrawal=withdrawal)
    await bot.delete_message(chat_id=id, message_id=message.message_id)
    await bot.edit_message_text(chat_id=id, message_id=withdrawal.message_id,
                                text="Ваш перевод на проверке администратора", reply_markup=kb.back_to_start)
    config = configuration()
    amount = round(withdrawal.amount * (1 - config.commission / 100), 2)
    text = get_mes("withdrawal_admin",
                   user_id=id,
                   username=f"@{user.username}" if user.username else "Отсутсвует username",
                   count=withdrawal.count,
                   amount=amount,
                   requisites=user.requisites,
                   all_coin=user.count)
    keyboard = create_keyboard(
        {"Подтвердить": f"yesWithdrawal{id}_{withdrawal.count}_{withdrawal.amount}",
         "Отменить": f"noWithdrawal{id}_{withdrawal.count}_{withdrawal.amount}"})
    await bot.send_photo(chat_id=admin_id,
                         photo=photo,
                         caption=text,
                         reply_markup=keyboard)
    await state.clear()


withdrawal_rt = router
