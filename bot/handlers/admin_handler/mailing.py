import os

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, FSInputFile

from bot import keyboards as kb
from bot.config import bot, admin_id
from bot.db import users
from bot.states import States

router = Router()


@router.callback_query(F.data == "mailing")
async def admin_mailing(message: CallbackQuery, state: FSMContext):
    await state.clear()
    id = message.from_user.id
    await state.set_state(States.mailing)
    await bot.edit_message_text(chat_id=id,
                                message_id=message.message.message_id,
                                text="Пришлите фото/текст",
                                reply_markup=kb.back_admin_menu_kb)
    await state.update_data(message_id=message.message.message_id)


@router.message(States.mailing, F.content_type.in_({'text'}))
async def mes_mailing(message: Message, state: FSMContext):
    id = message.from_user.id
    data = await state.get_data()
    message_id = data["message_id"]
    for user in users:
        if user.status and user.id != admin_id:
            try:
                await bot.send_message(chat_id=user.id,
                                       text=message.text,
                                       reply_markup=kb.del_mes_kb,
                                       parse_mode=None)
            except Exception as e:
                await bot.send_message(chat_id=id,
                                       text=str(e),
                                       reply_markup=kb.del_mes_kb)
    await message.delete()
    await bot.delete_message(chat_id=id, message_id=message_id)
    await bot.send_message(chat_id=id,
                           text="Рассылка закончилась",
                           reply_markup=kb.admin_menu_kb)


@router.message(States.mailing, F.photo)
async def mes_mailing(message: Message, state: FSMContext):
    id = message.from_user.id
    data = await state.get_data()
    message_id = data["message_id"]

    file = message.photo[-1]
    path = f"bot/mailing/{message.photo[-1].file_id}_{message.message_id}.jpg"
    await bot.download(
        file=file,
        destination=path
    )
    photo = FSInputFile(path)
    await message.delete()
    for user in users:
        if user.status and user.id != admin_id:
            try:
                await bot.send_photo(chat_id=user.id,
                                     photo=photo,
                                     caption=message.caption,
                                     reply_markup=kb.del_mes_kb,
                                     parse_mode=None)
            except Exception as e:
                await bot.send_message(chat_id=id, text=str(e), reply_markup=kb.del_mes_kb)
    await bot.delete_message(chat_id=id, message_id=message_id)
    await bot.send_message(chat_id=id,
                           text="Рассылка закончилась",
                           reply_markup=kb.admin_menu_kb)
    # os.remove(path)


mailing_rt = router
