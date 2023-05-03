import xml.etree.ElementTree as ET
import argparse
import base64
from mapper import mapper

def normalizeURL(url):
	
	tmp = url.split("://")
	protocol = tmp[0]
	endpoint = tmp[1]
	endpoint = endpoint.replace("//","/")
	
	return f"{protocol}://{endpoint}"

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
    # print(data)
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
	# header = tmp[0].split("\r\n")
	body = tmp[1]
	# header = parseHeader(header)	
	data = {
		"header" : header,
		"body" : body
	}
	return data

if __name__ == "__main__":
	
	parser = argparse.ArgumentParser(description='Mapper description')
	parser.add_argument("-f", "--filename", type=str)
	args = parser.parse_args()

	if(args.filename != None):
		data = parseXML(args.filename)
		mapper(data)
	else:
		parser.print_help()