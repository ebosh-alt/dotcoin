from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot import keyboards as kb
from bot.config import bot
from bot.db import configuration
from bot.states import States
from bot.utils.GetMessage import get_mes

router = Router()


@router.callback_query(F.data == "info_project")
async def admin_info_project(message: CallbackQuery, state: FSMContext):
    await state.clear()
    id = message.from_user.id
    config = configuration()
    # course = round(config.course + config.income_yesterday / config.turnover_yesterday, 2)
    await bot.edit_message_text(chat_id=id,
                                message_id=message.message.message_id,
                                text=get_mes("info_project",
                                             requisites=config.requisites,
                                             commission=config.commission,
                                             capitalization=config.start_capital,
                                             current_capitalization=config.turnover,
                                             course=config.course,
                                             profit_today=config.income_today,
                                             income=config.income_all,
                                             replenishment=config.replenishment,
                                             withdrawal=config.withdrawal,
                                             ),
                                reply_markup=kb.back_admin_menu_kb)


info_project_rt = router
"""
  course = start_course * ((cur_capitalization) / capitalization)
  course - курс
  start_course - изначальный курс
  cur_capitalization - текущая капитализация
  capitalization - изначальная капитализация
"""
