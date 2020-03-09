import pymysql,gensim
from Identify import Identify
import openpyxl

iden = Identify()
accu = 0

#读取excel
try:
    wb = openpyxl.load_workbook('Result3.xlsx')
    sheet = wb.get_active_sheet()
    TOTOL = len(sheet['A'])-1
    for i in range(2,len(sheet['A'])+1):
        shishi = sheet['D'+str(i)].value
        if shishi:
            shicate = iden.identify(shishi)
            sheet['E'+str(i)].value = shicate

        # print(shishi)
        shoushi = sheet['F'+str(i)].value
        if shoushi:
            #print(shoushi)
            shoucate = iden.identify(shoushi)
            sheet['G'+str(i)].value = shoucate

        if (shishi and shicate == 'abstract') or (shoushi and shoucate == 'abstract'):
            sheet['H'+str(i)].value = 1
            if sheet['B'+str(i)].value == 1:
                accu += 1
                sheet['I'+str(i)].value = 1
            else:
                sheet['I'+str(i)].value = 0
        else:
            sheet['H'+str(i)].value = 0
            if sheet['B'+str(i)].value == 0:
                accu += 1
                sheet['I'+str(i)].value = 1
            else:
                sheet['I'+str(i)].value = 0
        print("第"+str(i)+"行完成")
    wb.save('Result3.xlsx')
    accuracy = accu/TOTOL#1407 1982 2040 1846
    print(accuracy)

except BaseException:
    pass