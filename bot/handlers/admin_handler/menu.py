import os

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from bot import keyboards as kb
from bot.config import bot
from bot.db import configuration
from bot.utils import Filters

router = Router()


@router.callback_query(F.data == "admin_menu")
@router.message(Filters.IsAdmin(), Command("admin"))
async def admin(message: Message | CallbackQuery, state: FSMContext):
    id = message.from_user.id
    if type(message) is CallbackQuery:
        await message.message.delete()
        config = configuration()
        cur_state = await state.get_state()
        if config.path_photo is not None and cur_state == "change_info":
            os.remove(config.path_photo)
    await state.clear()
    await bot.send_message(chat_id=id, text="Добро пожаловать в админ панель", reply_markup=kb.admin_menu_kb)


menu_admin_rt = router
