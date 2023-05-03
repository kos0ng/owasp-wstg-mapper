import xlsxwriter
from datetime import datetime

def template(worksheet):
	worksheet.write('A1', 'Hello..')
	worksheet.write('B1', 'Geeks')
	worksheet.write('C1', 'For')
	worksheet.write('D1', 'Geeks')

def export(jsonData):
	now = datetime.now()
	# fileName = now.strftime("%Y_%m_%d_%H_%M_%S.xlsx")
	fileName = "coba.xlsx"
	filePath = f"report/{fileName}"

	workbook = xlsxwriter.Workbook(filePath)
	worksheet = workbook.add_worksheet()

	template(worksheet)

	workbook.close()