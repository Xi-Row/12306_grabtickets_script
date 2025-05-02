import openpyxl
def init_station_code(file):
    wb = openpyxl.load_workbook(file)
    ws = wb.active
    # transform str to lst then to dict
    lst = []
    for row in ws.rows:
        sub_lst = []
        for cell in row:
            sub_lst.append(cell.value)
        lst.append(sub_lst)
    return dict(lst)

# city_code_dic = init_station_code('station_code.xlsx')
