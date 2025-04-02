import gspread
import logging


gp = gspread.service_account(filename='services/anketa.json')
# gp = gspread.service_account(filename='anketa.json')

# Open Google spreadsheet
gsheet = gp.open('@bazunovaleksey')


# select worksheet
sheet = gsheet.worksheet("TAVI")


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