import configparser
import openpyxl
from datetime import datetime

#global variables
config_path = './config.ini'
cparser = configparser.ConfigParser()
cparser.read(config_path)


#program
book = openpyxl.load_workbook('output1.xlsx')
worksheet = book['USERS']


for idx, row in enumerate(worksheet.rows):
    dateFollowed = datetime.strptime(row[1].value, "%m/%d/%Y, %H:%M:%S")
    print(row[0].value)
    print((datetime.now() - dateFollowed).days)
    if((datetime.now() - dateFollowed).days >= 1):
      worksheet.delete_rows(idx + 1, 1)
      book.save('output.xlsx')