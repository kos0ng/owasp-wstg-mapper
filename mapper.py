import xml.etree.ElementTree as ET
import argparse
import base64

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
    	data[key]['request'] = request.decode()
    	data[key]['response'] = response.decode()
    	
    return data

def parseHTTP():
	return True

if __name__ == "__main__":
	
	parser = argparse.ArgumentParser(description='Mapper description')
	parser.add_argument("-f", "--filename", type=str)
	args = parser.parse_args()

	data = parseXML(args.filename)