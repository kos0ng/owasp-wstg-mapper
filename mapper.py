import json
import re
from export import *

blacklist = [".png", ".jpg", ".jpeg", ".json", ".css", ".js", ".ico"]

regexHeader = ["(?i){}[ ]?:([ \'\"\w-]+)", "(?i)[\/]({})/([\w-]+)"]
regexBody = ["(?i)[\"\']{}[\"\'][ ]?:([ \"\w-]+)", "(?i)[\?\&]?({})=([\w-]+)",]
regexResponse = ["(?i){}[ ]?:([ \'\"\w-]+)"]


def checkReflected(request, response):
	result = []
	for i in regexHeader:
		tmp = re.findall(i.format("([\w]+)"), request['header'])
		for j in tmp:
			val = j[1]
			if(val not in result):
				result.append(val)
	for i in regexBody:
		tmp = re.findall(i.format("([\w]+)"), request['body'])
		for j in tmp:
			val = j[1]
			if(val not in result):
				result.append(val)
	for i in result:
		if(i in response['body']):
			return True
	return False


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
	
	for i in request['header_regex']:
		for j in keyData:
			for k in regexHeader:
				x = re.search(k.format(i), data[j]['request']['header'])
				if(x is not None):
					testData['target'].append(j)
					keyData.remove(j)
	for i in request['body_regex']:
		for j in keyData:
			if(i == "*"):
				testData['target'].append("*")
				return testData
			for k in regexBody:
				x = re.search(k.format(i), data[j]['request']['body'])
				if(x is not None):
					testData['target'].append(j)
					keyData.remove(j)			
	
	for i in response['header_regex']:
		for j in keyData:
			for k in regexResponse:
				x = re.search(k.format(i), data[j]['response']['header'])
				if(x is not None):
					testData['target'].append(j)
					keyData.remove(j)
	for i in response['body_regex']:
		for j in keyData:
			x = re.search(i, data[j]['response']['header'])
			if(x is not None):
				testData['target'].append(j)
				keyData.remove(j)
	
	if(testData["reflected"] == 1) :
		for j in keyData:
			resultCheck = checkReflected(data[j]['request'], data[j]['response'])
			if(resultCheck):
				testData['target'].append(j)
				keyData.remove(j)

	return testData

def assignDetail(testData, data, url):	
	for i in testData:
		test = testData[i]['test']
		if(testData[i]['files'] == 0):
			if(checkBlackList(url)):
				continue
		testHeaderRequest = test['request']['header_regex']
		testBodyRequest = test['request']['body_regex']
		testHeaderResponse = test['response']['header_regex']
		testBodyResponse = test['response']['body_regex']
		check = True
		for j in testHeaderRequest:
			for k in regexHeader:
				x = re.search(k.format(j), data['request']['header'])
				if(x is not None):
					data['testCases'].append(i)
					check = False
					break
			if(check == False):
				break
		if(check):
			for j in testBodyRequest:
				if(j == "*"):
					data['testCases'].append(i)
					break
				for k in regexBody:
					x = re.search(k.format(j), data['request']['body'])
					if(x is not None):
						data['testCases'].append(i)
						check = False
						break
				if(check == False):
					break
		if(check):
			for j in testHeaderResponse:
				for k in regexResponse:
					x = re.search(k.format(j), data['response']['header'])
					if(x is not None):
						data['testCases'].append(i)
						check = False
						break
				if(check == False):
					break
		if(check):
			for j in testBodyResponse:
				x = re.search(j, data['response']['body'])
				if(x is not None):
					data['testCases'].append(i)
					check = False
					break
		if(check):
			if(testData[i]['reflected'] == 1):
				resultCheck = checkReflected(data['request'], data['response'])
				if(resultCheck):
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
		if(i in data): 
			newJson[i] = data[i]
	return newJson


def mapper(data, filePath, reportType, level):
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
		export(baseURL, jsonData, filePath, reportType)
	elif(reportType == 2):
		export(baseURL, data, filePath, reportType)