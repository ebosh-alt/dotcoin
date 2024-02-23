from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile

from bot import keyboards as kb
from bot.config import bot
from bot.db import configuration
from bot.utils import Filters

router = Router()


@router.message(Filters.IsUser(), Command("info"))
async def greeting_user(message: Message, state: FSMContext):
    id = message.from_user.id
    config = configuration()
    if config.path_photo is None:
        await bot.send_message(chat_id=id,
                               text=config.info_text,
                               reply_markup=kb.back_to_start)
    else:
        photo = FSInputFile(config.path_photo)
        await bot.send_photo(chat_id=id,
                             photo=photo,
                             caption=config.info_text,
                             reply_markup=kb.back_to_start)

info_rt = router
