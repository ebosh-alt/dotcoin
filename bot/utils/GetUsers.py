import xlwt

from bot.db import users


def excel_user() -> str:
    book = xlwt.Workbook()

    sheet1 = book.add_sheet("users")
    cols = ["A", "B", "C", "D"]
    txt = ["user_id", "username", "количество дукат", "статус"]
    for num in range(1):
        row = sheet1.row(num)
        for index, col in enumerate(cols):
            value = txt[index]
            row.write(index, value)
    count = 1
    for user in users:
        data = user.data_by_excel()
        row = sheet1.row(count)
        for index, col in enumerate(cols):
            value = data[index]
            row.write(index, value)
        count += 1
    path = "bot/db/users.xls"
    book.save(path)
    return path

