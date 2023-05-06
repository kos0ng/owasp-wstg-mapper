import xlsxwriter
from datetime import datetime
import json

def template(workbook, jsonData):
	
	fileTemplate = open("data/template_wstg.json","r").read()
	jsonTestCase = json.loads(fileTemplate)

	worksheet = workbook.add_worksheet()
	
	title = workbook.add_format({'bold': True})
	title.set_font_size(14)

	worksheet.set_column(0, 0, 25)
	worksheet.set_column(1, 1, 50)
	worksheet.set_column(2, 2, 50)
	worksheet.set_column(3, 3, 50)
	worksheet.set_column(4, 4, 15)
	worksheet.set_column(5, 5, 50)
	worksheet.set_column(6, 6, 30)

	worksheet.set_row(5, 25) 

	mergeFormat = workbook.add_format(
    	{
        	"align": "center",
        	"valign": "vcenter",
    	}
	)

	header = workbook.add_format(
		{
			"bold": True,
			"align": "center",
			"bg_color": "#F97B22",
			"border": 1,
			"valign": "vcenter",
			"text_wrap": True,
		}
	)

	body = workbook.add_format(
		{
			"align": "center",
			"border": 1,
			"valign": "vcenter",
			"text_wrap": True,
		}
	)

	bgRed = workbook.add_format(
		{
			"bold": True,
			"align": "center",
			"bg_color": "red",
			"border": 1,
			"font_color": "white",
			"valign": "vcenter",
		}
	)

	bgGreen = workbook.add_format(
		{
			"bold": True,
			"align": "center",
			"bg_color": "#16FF00",
			"border": 1,
			"valign": "vcenter",
		}
	)

	worksheet.write('A1', 'OWASP: Testing Guide v4.2 Checklist', title)
	
	worksheet.write('A3', 'Target Name : ')
	worksheet.write('A4', 'Pentester Name : ')

	start = 6
	for testCase in jsonTestCase:
		
		# header
		worksheet.write(f'A{start}', testCase['header'], header)
		worksheet.write(f'B{start}', 'Test Name', header)
		worksheet.write(f'C{start}', 'Objectives', header)
		worksheet.write(f'D{start}', 'Endpoint', header)
		worksheet.write(f'E{start}', 'Result', header)
		worksheet.write(f'F{start}', 'Screenshot', header)
		worksheet.write(f'G{start}', 'Notes', header)
		start += 1
		end = start

		# body
		for bodyTest in testCase['body']:
			if(bodyTest in jsonData):
				listEndpoint = jsonData[bodyTest]['target']
				for endpoint in listEndpoint:
					worksheet.write(f'D{end}',endpoint, body)
					worksheet.write(f'E{end}','', body)
					end += 1
				worksheet.merge_range(f"A{start}:A{end-1}", bodyTest, body)
				worksheet.merge_range(f"B{start}:B{end-1}", testCase['body'][bodyTest]['name'], body)
				worksheet.merge_range(f"C{start}:C{end-1}", testCase['body'][bodyTest]['objectives'], body)
				worksheet.merge_range(f"F{start}:F{end-1}", '', body)
				worksheet.merge_range(f"G{start}:G{end-1}", '', body)
			else:
				worksheet.write(f'A{end}', bodyTest, body)
				worksheet.write(f'B{end}', testCase['body'][bodyTest]['name'], body)
				worksheet.write(f'C{end}', testCase['body'][bodyTest]['objectives'], body)
				worksheet.write(f'D{end}', '', body)
				worksheet.write(f'E{end}', '', body)
				worksheet.write(f'F{end}', '', body)
				worksheet.write(f'G{end}', '', body)
				end += 1
			start = end
			
		end += 1
		start = end

	
	worksheet.conditional_format(f'E7:E{end-2}', {'type': 'cell',
                                        'criteria': '==',
                                        'value':    '"VULN"',
                                        'format':   bgRed})
	worksheet.conditional_format(f'E7:E{end-2}', {'type': 'cell',
                                        'criteria': '==',
                                        'value':    '"PASSED"',
                                        'format':   bgGreen})
	worksheet.data_validation(f'E7:E{end-2}', {'validate' : 'list', 'source': ['PASSED', 'VULN']})
	

	return worksheet

def export(jsonData):
	now = datetime.now()
	fileName = now.strftime("Pentest_Checklist_%Y%m%d_%H%M%S.xlsx")
	filePath = f"report/{fileName}"

	workbook = xlsxwriter.Workbook(filePath)

	worksheet = template(workbook, jsonData)

	workbook.close()