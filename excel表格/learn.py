import xlwt

def set_style(name, height, bold=False):
    style = xlwt.XFStyle()
    font = xlwt.Font
    font.name = name
    font.bold = bold
    font.colour_index = 4
    style.font = font
    return style

def write_excel():
    f = xlwt.Workbook()
    sheet1 = f.add_sheet('学生', cell_overwrite_ok=True)
    row0