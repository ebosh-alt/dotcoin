import os

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, FSInputFile

from bot import keyboards as kb
from bot.config import bot
from bot.db import configuration
from bot.states import States
from bot.utils.checks import check_is_float

router = Router()


@router.callback_query(F.data == "change_info")
async def admin_set_capitalization(message: CallbackQuery, state: FSMContext):
    await state.clear()
    id = message.from_user.id
    await state.set_state(States.change_info)
    await bot.edit_message_text(chat_id=id,
                                message_id=message.message.message_id,
                                text="Введите новую информация",
                                reply_markup=kb.back_admin_menu_kb)
    await state.update_data(message_id=message.message.message_id)


@router.message(States.change_info, F.content_type.in_({'text'}))
async def mes_change_info(message: Message, state: FSMContext):
    id = message.from_user.id
    data = await state.get_data()
    message_id = data["message_id"]
    await state.update_data(text=message.text)
    await message.delete()
    await bot.edit_message_text(chat_id=id,
                                message_id=message_id,
                                text=f"Введенные данные: {message.text}",
                                reply_markup=kb.confirm_admin_kb)


@router.message(States.change_info, F.photo)
async def photo_change_info(message: Message, state: FSMContext):
    id = message.from_user.id
    data = await state.get_data()
    message_id = data["message_id"]
    file = message.photo[-1]
    path = f"bot/db/info.jpg"
    await bot.download(
        file=file,
        destination=path
    )
    photo = FSInputFile(path)
    await message.delete()
    await bot.delete_message(chat_id=id,
                             message_id=message_id)
    mes = await bot.send_photo(chat_id=id,
                               photo=photo,
                               caption=f"Введенные данные: {message.caption}",
                               reply_markup=kb.confirm_admin_kb)
    await state.update_data(message_id=mes.message_id)
    await state.update_data(text=message.caption)
    await state.update_data(path=path)


@router.callback_query(States.change_info, F.data == "yes_change")
async def confirm_ban_unban(message: CallbackQuery, state: FSMContext):
    id = message.from_user.id
    data = await state.get_data()
    message_id = data["message_id"]
    text = data.get("text", None)
    path = data.get("path", None)
    config = configuration()
    # if config.path_photo is not None:
    #     os.remove(config.path_photo)
    config.info_text = text
    config.path_photo = path
    configuration.save(config)
    await state.clear()
    await bot.delete_message(chat_id=id, message_id=message_id)
    await bot.send_message(chat_id=id,
                           text="Информация изменена",
                           reply_markup=kb.admin_menu_kb)


change_info_rt = router
