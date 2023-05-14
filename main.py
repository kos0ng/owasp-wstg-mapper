import xml.etree.ElementTree as ET
import argparse
import base64
import re
from uuid import UUID
from mapper import mapper


def isValidUUID(uuid_to_test, version=4):
    try:
        uuid_obj = UUID(uuid_to_test, version=version)
    except ValueError:
        return False
    return str(uuid_obj) == uuid_to_test

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
    	request = base64.b64decode(request)
    	response = base64.b64decode(response)
    	
    	key = f"{method} {url}"
    	
    	data[key] = {}
    	data[key]['request'] = parseHTTP(request.decode())
    	data[key]['response'] = parseHTTP(response.decode())    	
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

if __name__ == "__main__":
	
	listURL = []
	parser = argparse.ArgumentParser(description='Mapper description')
	parser.add_argument("-f", "--filename", type=str)
	parser.add_argument("-o", "--output", type=str)
	parser.add_argument("-l", "--level", type=int)
	args = parser.parse_args()

	if(args.filename != None):
		data = parseXML(args.filename)
		mapper(data, args.output, args.level)
	else:
		parser.print_help()