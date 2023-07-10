import xml.etree.ElementTree as ET
import argparse
import base64
import re
import os
import magic
import glob
from uuid import UUID
from mapper import mapper
from datetime import datetime
import time
from requests_toolbelt.multipart import decoder


def isValidUUID(uuid_to_test, version=4):
    try:
        uuid_obj = UUID(uuid_to_test, version=version)
    except ValueError:
        return False
    return str(uuid_obj) == uuid_to_test

def checkFile(path):
	return os.path.isfile(path)

def formatURL(url):
	tmp2 = url.split("/")
	tmp3 = tmp2[-1].split("?")
	if(tmp3[0] == '' and len(tmp3) == 2):
		tmp = tmp2[:-1] + [tmp3[1]]
	else:
		tmp = tmp2[:-1] + tmp3
	regexURL = r"[\?]?([\w]+)=([\w-]+)?"
	partURL = []
	for i in tmp:
		result = re.findall(regexURL, i)
		if(result != []):
			partURL.append(result)
		else:
			partURL.append(i)
	formatted = []
	for i in partURL:
		if(isinstance(i, list)):
			parameter = []
			for j in i:
				parameter.append(j[0] + "=<value>")
			formatted.append("?" + "&".join(parameter))
		elif(i.isdigit()):
			formatted.append("<value>")
		elif(isValidUUID(i)):
			formatted.append("<value>")
		else:
			formatted.append(i)
	# print(url, formatted)
	return "/".join(formatted)

def normalizeURL(url):
	
	tmp = url.split("://")
	protocol = tmp[0]
	endpoint = tmp[1]
	endpoint = endpoint.replace("//","/")
	
	return f"{protocol}://{formatURL(endpoint)}"


def parseXML(xmlFile, filterUrl = None):
  
    data = {}
    tree = ET.parse(xmlFile)
    root = tree.getroot()
    count = 0
    
    for item in root:
    	count += 1
    	url = item.find('url').text
    	method = item.find('method').text
    	request = item.find('request').text
    	response = item.find('response').text

    	url = normalizeURL(url)

    	key = f"{method} {url}"

    	if(filterUrl != None):
    		if(filterUrl in key):
    			
	    		data[key] = {}

    			if(request == None):
    				request = ""
    				data[key]['request'] =  {'header' :'', 'body' : ''}
    			else:
    				try:
    					request = base64.b64decode(request).decode()
    					data[key]['request'] = parseHTTP(request)
    					
    				except Exception as e:
    					request = base64.b64decode(request)
    					data[key]['request'] = parseMultiPart(request)
    	
    			if(response == None):
    				response =  ""
    				data[key]['response'] =  {'header' :'', 'body' : ''}
    			else:
    				try:
    					response = base64.b64decode(response).decode()
    					data[key]['response'] = parseHTTP(response)
    				except Exception as e:
    					response = base64.b64decode(response)
    					data[key]['response'] = parseFile(response)
    			data[key]['testCases'] = []
    	else:
	    	data[key] = {}

    		if(request == None):
    			request = ""
    			data[key]['request'] = ''
    		else:
    			try:
    				request = base64.b64decode(request).decode()
    				data[key]['request'] = parseHTTP(request)
    			except Exception as e:
    				request = base64.b64decode(request)
    				data[key]['request'] = parseMultiPart(request)
    	
    		if(response == None):
    			response =  ""
    			data[key]['response'] =  {'header' :'', 'body' : ''}
    		else:
    			try:
    				response = base64.b64decode(response).decode()
    				data[key]['response'] = parseHTTP(response)
    			except Exception as e:
    				response = base64.b64decode(response)
    				data[key]['response'] = parseFile(response)
    		data[key]['testCases'] = []
    print(f"total traffic : {count}")
    return data

def parseHeader(header):
	data = {}

	for i in header.split(b"\r\n"):
		tmp = i.split(b": ")
		if(len(tmp)>1):
			data[tmp[0].decode()] = tmp[1].decode()
		else:
			data['url'] = tmp[0]
	return data

def parseHTTP(data):
	tmp = data.split("\r\n\r\n")
	header = tmp[0]
	body = tmp[1]	
	data = {
		"header" : header,
		"body" : body
	}
	return data

def parseFile(data):
	tmp = data.split(b"\r\n\r\n")
	header = tmp[0]
	body = tmp[1]
	data = {
		"header" : header.decode(),
		"body" : magic.from_buffer(body[:2048])
	}
	return data

def parseMultiPart(data):
	tmp = data.split(b"\r\n\r\n-")
	if(len(tmp) == 1):
		return {'header' :'', 'body' : ''}
	header = parseHeader(tmp[0])
	body = tmp[1]
	multipart_data = decoder.MultipartDecoder(body, header['Content-Type'])
	resp = ""
	if(len(multipart_data.parts) ==  1):
		resp += f"filetype={magic.from_buffer(multipart_data.parts[0].content[:2048])}"
	else:
		for i in multipart_data.parts:
			resp += f"filetype={magic.from_buffer(i.content[:2048])}&"
	data = {
		"header" : tmp[0].decode(),
		"body" : resp
	}
	return data

if __name__ == "__main__":
	
	listURL = []
	parser = argparse.ArgumentParser(description='OSTGMapper, an automated security testing guide mapper based on pattern. Built to reduce time of manually mapping possible security tests for web applications. Currently support OWASP WSTG v4.2.')
	parser.add_argument("-i", "--input", type=str, help="Exported XML file from burpsuite")
	parser.add_argument("-f", "--filter", type=str, help="Filter URL based on string")
	parser.add_argument("-t", "--type", type=int, help="Report type you want to choose")
	parser.add_argument("-l", "--level", type=int, help="List of test cases you want to map")
	parser.add_argument("-o", "--output", type=str, help="Filename for the report (output)")
	args = parser.parse_args()

	listType = [1, 2]
	listLevel = [0]
	for i in glob.glob("level/level[0-9].data"):
		try:
			level = i.split("level/level")[1].split(".data")[0]
		except Exception as e:
			level = i.split("level\\level")[1].split(".data")[0]
		listLevel.append(int(level))

	if(args.type == None):
		args.type = 1
	if(args.level == None):
		args.level = 0

	if(args.input != None):
		if(checkFile(args.input)):
			if(args.type not in listType):
				print("Unknown Type!")
				exit()
			if(args.level not in listLevel):
				print("Unknown Level!")
				exit()
			if(args.output != None):
				if(args.output.endswith(".xlsx")):
					fileName = args.output
				else:
					fileName = args.output + ".xlsx"
			else:
				now = datetime.now()
				fileName = now.strftime("Pentest_Checklist_%Y%m%d_%H%M%S.xlsx")
			
			filePath = f"report/{fileName}"
			
			if(checkFile(filePath)):
				option = input(f"Replace file {filePath} ? (Y/N) : ")
				if(option.upper() == "Y"):
					start = time.time()
					data = parseXML(args.input, args.filter)
					mapper(data, filePath, args.type, args.level)
					end = time.time()
					print(f"Process time : {round(end-start,2)} second")
				elif(option.upper() == "N"):
					start = time.time()
					arrFilePath = filePath.split(".")
					filePath = arrFilePath[0] + "_2." + arrFilePath[1]
					data = parseXML(args.input, args.filter)
					mapper(data, filePath, args.type, args.level)
					end = time.time()
					print(f"Process time : {round(end-start,2)} second")
				else:
					print("Option unknown!")
			else:
				start = time.time()
				data = parseXML(args.input, args.filter)
				mapper(data, filePath, args.type, args.level)
				end = time.time()
				print(f"Process time : {round(end-start,2)} second")
		else:
			print(f"File \"{args.input}\" not found!")
	else:
		print("\nargument -i or --input is mandatory\n")
		parser.print_help()