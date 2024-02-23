from aiogram.methods import SendMessage
from bot import keyboards as kb
from bot.config import bot


async def send(text: str, id: int):
    await bot.send_message(chat_id=id, text=text, reply_markup=kb.del_mes_kb)
