from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, FSInputFile

from bot.config import bot, admin_id
from bot.db import users, configuration
from bot.db.TopUp import TopUp
from bot.keyboards import create_keyboard
from bot.states import States
from bot.utils import Filters
from bot.utils.GetMessage import get_mes
from bot import keyboards as kb

router = Router()


@router.callback_query(Filters.IsUser(), F.data == "top_up_balance")
async def start(message: CallbackQuery, state: FSMContext):
    id = message.from_user.id
    await bot.delete_message(chat_id=id,
                             message_id=message.message.message_id)

    mes = await bot.send_message(chat_id=id,
                                 text=get_mes("input_coin_top_up"))
    await state.set_state(States.top_up)
    await state.update_data(topUp=TopUp(message_id=mes.message_id))


@router.message(States.top_up, F.content_type.in_({'text'}))
async def input_coin(message: Message, state: FSMContext):
    id = message.from_user.id
    if message.text.isdigit():
        count = int(message.text)
        data = await state.get_data()
        top_up: TopUp = data["topUp"]
        config = configuration()
        top_up.count = count
        top_up.amount = float(count * config.course)
        # top_up.amount = round(top_up.amount * (config.commission / 100 + 1), 2)
        await bot.delete_message(message_id=message.message_id, chat_id=id)
        await bot.edit_message_text(chat_id=id, message_id=top_up.message_id,
                                    text=get_mes("input_receipt_top_up",
                                                 amount=round(top_up.amount * (config.commission / 100 + 1), 2),
                                                 requisites=config.requisites))
        await state.update_data(topUp=top_up)


@router.message(States.top_up, F.photo)
async def input_photo(message: Message, state: FSMContext):
    id = message.from_user.id
    user = users.get(id)
    data = await state.get_data()
    top_up: TopUp = data["topUp"]
    file = message.photo[-1]
    path = f"bot/receipts/replenishment/{message.photo[-1].file_id}_{message.message_id}.jpg"
    await bot.download(
        file=file,
        destination=path
    )
    photo = FSInputFile(path)
    await state.update_data(topUp=top_up)
    await bot.delete_message(chat_id=id, message_id=message.message_id)
    await bot.edit_message_text(chat_id=id, message_id=top_up.message_id,
                                text="Ваш платеж на проверке администратора",
                                reply_markup=kb.back_to_start)
    config = configuration()

    amount = round(top_up.amount * (config.commission / 100 + 1), 2)
    text = get_mes("top_up_admin",
                   user_id=id,
                   username=f"@{user.username}" if user.username else "Отсутсвует username",
                   count=top_up.count,
                   amount=amount,
                   requisites=user.requisites,
                   all_coin=user.count)
    keyboard = create_keyboard(
        {"Подтвердить": f"yesReplenishment{id}_{top_up.count}_{top_up.amount}",
         "Отменить": f"noReplenishment{id}_{top_up.count}_{top_up.amount}"})
    await bot.send_photo(chat_id=admin_id,
                         photo=photo,
                         caption=text,
                         reply_markup=keyboard)
    await state.clear()


top_up_rt = router
