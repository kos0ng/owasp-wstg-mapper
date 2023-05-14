import json
import re
from export import *

def removeFilesURL(blacklist, keys):
	sanitized = []
	for i in keys:
		check = True
		for j in blacklist:
			if(i.endswith(j)):
				check = False
				break
		if(check):
			sanitized.append(i)
	return sanitized

def assign(testData, data):
	keyData = list(data.keys())
	if(testData['files'] == 0):
		blacklist = [".png", ".jpg", ".jpeg", ".json", ".css", ".js", ".ico"]
		keyData = removeFilesURL(blacklist, keyData)
	testCase = testData['test']
	request = testCase['request']
	response = testCase['response']
	for i in request['regex']:
		for j in keyData:
			x = re.search(i, data[j]['request']['header'])
			if(x is None):
				x = re.search(i, data[j]['request']['body'])
				if(x is not None):
					testData['target'].append(j)
					keyData.remove(j)
			else:
				testData['target'].append(j)
				keyData.remove(j)
	for i in response['regex']:
		for j in keyData:
			x = re.search(i, data[j]['response']['header'])
			if(x is None):
				x = re.search(i, data[j]['response']['body'])
				if(x is not None):
					testData['target'].append(j)
					keyData.remove(j)
			else:
				testData['target'].append(j)
				keyData.remove(j)
	return testData

def mapper(data, output = None, level = None):
	f = open("data/wstg.json","r").read()
	jsonData = json.loads(f)
	for i in jsonData:
		jsonData[i] = assign(jsonData[i], data)
	export(jsonData, output, level)