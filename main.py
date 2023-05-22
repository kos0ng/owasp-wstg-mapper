import xml.etree.ElementTree as ET
import argparse
import base64
import re
import os
import magic
from uuid import UUID
from mapper import mapper


def isValidUUID(uuid_to_test, version=4):
    try:
        uuid_obj = UUID(uuid_to_test, version=version)
    except ValueError:
        return False
    return str(uuid_obj) == uuid_to_test

def checkFile(path):
	return os.path.isfile(path)

def formatURL(url):
	tmp = url.split("/")
	regexURL = r"[\?]?([\w]+)=([\w-]+)"
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
	return "/".join(formatted)

def normalizeURL(url):
	
	tmp = url.split("://")
	protocol = tmp[0]
	endpoint = tmp[1]
	endpoint = endpoint.replace("//","/")
	
	return f"{protocol}://{formatURL(endpoint)}"


def parseXML(xmlFile):
  
    data = {}
    tree = ET.parse(xmlFile)
    root = tree.getroot()
    
    for item in root:
    	url = item.find('url').text
    	method = item.find('method').text
    	request = item.find('request').text
    	response = item.find('response').text

    	url = normalizeURL(url)
    	
    	key = f"{method} {url}"
    	data[key] = {}

    	if(request == None):
    		request = ""
    		data[key]['request'] = ''
    	else:
    		request = base64.b64decode(request).decode()
    		data[key]['request'] = parseHTTP(request)
    	
    	if(response == None):
    		response =  ""
    		data[key]['response'] = ''
    	else:
    		try:
    			response = base64.b64decode(response).decode()
    			data[key]['response'] = parseHTTP(response)
    		except Exception as e:
    			response = base64.b64decode(response)
    			data[key]['response'] = parseFile(response)
    	data[key]['testCases'] = []
    	
    return data

def parseHeader(header):
	data = {}

	for i in header:
		tmp = i.split(": ")
		if(len(tmp)>1):
			data[tmp[0]] = tmp[1]
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
		"header" : header,
		"body" : magic.from_buffer(body[:2048])
	}
	return data


if __name__ == "__main__":
	
	listURL = []
	parser = argparse.ArgumentParser(description='Mapper description')
	parser.add_argument("-f", "--filename", type=str)
	parser.add_argument("-o", "--output", type=str)
	parser.add_argument("-t", "--type", type=int)
	args = parser.parse_args()

	listType = [None, 1,2]

	if(args.filename != None):
		if(checkFile(args.filename)):
			if(args.type not in listType):
				print("Unknown Type!")
			
			data = parseXML(args.filename)
			mapper(data, args.output, args.type)
		else:
			print(f"File \"{args.filename}\" not found!")
	else:
		parser.print_help()