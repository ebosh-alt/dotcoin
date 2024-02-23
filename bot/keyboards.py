from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder


def create_keyboard(name_buttons: list | dict, *sizes: int) -> types.InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    for name_button in name_buttons:
        if type(name_buttons[name_button]) is tuple:
            if len(name_buttons[name_button]) == 2:
                keyboard.button(
                    text=name_button, url=name_buttons[name_button][0], callback_data=name_buttons[name_button][1]
                )
            else:
                if "http" in name_buttons[name_button]:
                    keyboard.button(
                        text=name_button, url=name_button
                    )
                keyboard.button(
                    text=name_button, callback_data=name_button
                )

        else:

            if "http" in str(name_buttons[name_button]):
                keyboard.button(
                    text=name_button, url=name_buttons[name_button]
                )
            else:
                keyboard.button(
                    text=name_button, callback_data=name_buttons[name_button]
                )
    if len(sizes) == 0:
        sizes = (1,)
    keyboard.adjust(*sizes)
    return keyboard.as_markup(resize_keyboard=True, one_time_keyboard=True)


def create_reply_keyboard(name_buttons: list, one_time_keyboard: bool = False, request_contact: bool = False,
                          *sizes) -> types.ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()

    for name_button in name_buttons:
        if name_button is not tuple:
            keyboard.button(
                text=name_button,
                request_contact=request_contact
            )
        else:
            keyboard.button(
                text=name_button,
                request_contact=request_contact

            )
    if len(sizes) == 0:
        sizes = (1,)
    keyboard.adjust(*sizes)
    return keyboard.as_markup(resize_keyboard=True, one_time_keyboard=one_time_keyboard)


greeting_kb = create_keyboard(
    {"Вывести с баланса": "withdraw_balance",
     "Пополнить баланс": "top_up_balance",
     "Профиль": "profile"},
    2, 1)

del_mes_kb = create_keyboard({"Удалить уведомление": "del_notification"})
back_to_start = create_keyboard({"Назад": "back_to_start"})
profile_kb = create_keyboard({"Изменить реквизиты": "change_requisites_user", "Назад": "back_to_start"})
admin_menu_kb = create_keyboard({"Общие данные": "info_project",
                                 "Изменить реквизиты": "change_requisites",
                                 "Изменить комиссию": "change_commission",
                                 "Бан/разбан пользователя": "ban_unban",
                                 "Изменить капитализацию": "set_capitalization",
                                 "Рассылка": "mailing",
                                 "Изменить информацию": "change_info",
                                 },
                                2, 2, 2)
back_admin_menu_kb = create_keyboard({"Меню": "admin_menu"})
confirm_admin_kb = create_keyboard({"Подтвердить": "yes_change", "В меню": "admin_menu"},1,1)

