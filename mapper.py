import json
import re
from export import *

def check(key, data, jsonData):
	for i in jsonData:
		tmp = jsonData[i]['test']
		for j in tmp:
			for k in tmp[j]['regex']:
				x = re.search(k, data)
				if(x is not None):
					jsonData[i]['target'].append(key)
					break
			for k in tmp[j]['basic']:
				if(k in data):
					jsonData[i]['target'].append(key)
					break
	return jsonData

def mapper(data, output = None, level = None):
	f = open("data/wstg.json","r").read()
	jsonData = json.loads(f)
	
	for i in data:
		jsonData = check(i, data[i]['request']['header'],jsonData)
		jsonData = check(i, data[i]['request']['body'],jsonData)
		jsonData = check(i, data[i]['response']['header'],jsonData)
		jsonData = check(i, data[i]['response']['body'],jsonData)

	export(jsonData, output, level)