import gspread
import logging


gp = gspread.service_account(filename='services/TAVI.json')
# gp = gspread.service_account(filename='anketa.json')

# Open Google spreadsheet
# gsheet = gp.open('@bazunovaleksey')
gsheet = gp.open('TAVI Регистр СЗФО РФ 2025')


# select worksheet
# sheet = gsheet.worksheet("TAVI")
sheet = gsheet.worksheet("2025")


# добавить значения
def append_order(order):
    """
    Добавление нового записи
    :return:
    """
    logging.info(f'append_order')
    sheet.append_row(order)

if __name__ == '__main__':
    append_order()