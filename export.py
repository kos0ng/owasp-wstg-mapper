import xlsxwriter
from datetime import datetime

def template(workbook):
	
	worksheet = workbook.add_worksheet()
	
	title = workbook.add_format({'bold': True})
	title.set_font_size(14)

	# bigFont = workbook.add_format()
	# bigFont.set_font_size(10)

	worksheet.set_column(0, 0, 25)
	worksheet.set_column(1, 1, 50)
	worksheet.set_column(2, 2, 50)
	worksheet.set_column(3, 3, 50)
	worksheet.set_column(4, 4, 15)
	worksheet.set_column(5, 5, 50)
	worksheet.set_column(6, 6, 30)

	worksheet.set_row(5, 25) 

	merge_format = workbook.add_format(
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

	bg_red = workbook.add_format(
		{
			"bold": True,
			"align": "center",
			"bg_color": "red",
			"border": 1,
			"font_color": "white",
			"valign": "vcenter",
		}
	)

	bg_green = workbook.add_format(
		{
			"bold": True,
			"align": "center",
			"bg_color": "#16FF00",
			"border": 1,
			"valign": "vcenter",
		}
	)

	worksheet.merge_range("A1:F1", "Merged Range", merge_format)

	worksheet.write('A1', 'OWASP: Testing Guide v4.2 Checklist', title)
	
	worksheet.write('A3', 'Target Name : ')
	worksheet.write('A4', 'Pentester Name : ')

	# header
	worksheet.write('A6', 'Information Gathering', header)
	worksheet.write('B6', 'Test Name', header)
	worksheet.write('C6', 'Objectives', header)
	worksheet.write('D6', 'Endpoint', header)
	worksheet.write('E6', 'Result', header)
	worksheet.write('F6', 'Screenshot', header)
	worksheet.write('G6', 'Notes', header)

	# body
	worksheet.write('A7','WSTG-INFO-01', body)
	worksheet.write('B7','Conduct Search Engine Discovery Reconnaissance for Information Leakage', body)
	worksheet.write('C7','- Identify what sensitive design and configuration information of the application, system, or organization is exposed directly (on the organization\'s website) or indirectly (via third-party services).', body)
	worksheet.write('D7','https://google.com/a', body)
	#worksheet.data_validation('B2:B'+str(1+n_rows), {'validate' : 'list', 'source': ['a', 'b']})
	
	worksheet.conditional_format('E7:E100', {'type': 'cell',
                                        'criteria': '==',
                                        'value':    '"VULN"',
                                        'format':   bg_red})
	worksheet.conditional_format('E7:E100', {'type': 'cell',
                                        'criteria': '==',
                                        'value':    '"PASSED"',
                                        'format':   bg_green})
	worksheet.data_validation('E7:E10', {'validate' : 'list', 'source': ['PASSED', 'VULN']})

	worksheet.write('E7','', body)
	
	worksheet.write('F7','', body)
	worksheet.write('G7','', body)


	# worksheet.write('E8','', body)

	# worksheet.merge_range("A7:A8", "Merged Range", merge_format)

	
	





	

	return worksheet

def export(jsonData):
	now = datetime.now()
	# fileName = now.strftime("%Y_%m_%d_%H_%M_%S.xlsx")
	fileName = "coba.xlsx"
	filePath = f"report/{fileName}"

	workbook = xlsxwriter.Workbook(filePath)

	worksheet = template(workbook)

	workbook.close()