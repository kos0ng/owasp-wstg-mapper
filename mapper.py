import json
import re
from export import *

blacklist = [".png", ".jpg", ".jpeg", ".json", ".css", ".js", ".ico"]

def removeFilesURL(keys):
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

def checkBlackList(url):
	for i in blacklist:
		if(i in url):
			return True
	return False

def assignSimple(testData, data):
	keyData = list(data.keys())
	if(testData['files'] == 0):
		keyData = removeFilesURL(keyData)
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

def assignDetail(testData, data, url):	
	for i in testData:
		test = testData[i]['test']
		if(testData[i]['files'] == 0):
			if(checkBlackList(url)):
				continue
		testRequest = test['request']['regex']
		testResponse = test['response']['regex']
		check = True
		for j in testRequest:
			x = re.search(j, data['request']['header'])
			if(x is None):
				x = re.search(j, data['request']['body'])
				if(x is not None):
					data['testCases'].append(i)
			else:
				data['testCases'].append(i)
		if(check):
			for j in testResponse:
				x = re.search(j, data['response']['header'])
				if(x is None):
					x = re.search(j, data['response']['body'])
					if(x is not None):
						data['testCases'].append(i)
				else:
					data['testCases'].append(i)
	return data

def getBaseURL(data):
	for i in data:
		tmp = i.split("//")
		result = tmp[-1].split("/")
		return result[0]

def filterTest(data, dataLevel):
	newJson = {}
	for i in dataLevel:
		if(i in data): # should be deleted 
			newJson[i] = data[i]
	return newJson


def mapper(data, output, reportType, level):
	f = open("data/wstg.json","r").read()
	jsonData = json.loads(f)

	if(level != 0):
		dataLevel = open(f"level/level{level}.data","r").read().split("\n") # check list level on main.py
		jsonData = filterTest(jsonData, dataLevel)

	if(reportType == 1):
		for i in jsonData:
			jsonData[i] = assignSimple(jsonData[i], data)
	elif(reportType == 2):
		for i in data:
			data[i] = assignDetail(jsonData, data[i], i)

	baseURL = getBaseURL(data)
	if(reportType == 1):
		export(baseURL, jsonData, output, reportType)
	elif(reportType == 2):
		export(baseURL, data, output, reportType)