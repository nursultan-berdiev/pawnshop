from xlsxwriter.workbook import Workbook

background = '#ebfcff'
border = 1


def add_custom_format(format):
    format.set_bg_color(background)
    format.set_border(border)
    format.set_bold()
    return format


def number_format(book):
    num_format = book.add_format({'num_format': '#####0'})
    add_custom_format(num_format)
    return num_format


def money_format(book):
    mon_format = book.add_format({'num_format': '#,###,##0'})
    add_custom_format(mon_format)
    return mon_format


def date_format(book):
    date = book.add_format({'num_format': 'dd.mm.yyyy'})
    add_custom_format(date)
    return date


def style_format(book):
    style = book.add_format()
    add_custom_format(style)
    return style
