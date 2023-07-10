import json
import re
from export import *

blacklist = [".png", ".jpg", ".jpeg", ".json", ".css", ".js", ".ico", ".woff", ".woff2"]

regexHeader = ["(?i){}[ ]?:([ \'\"\w-]+)", "(?i)[/]({})/([\w-]+)", "(?i)[/]({})$", "(?i)[?&]?({})=([\w-]+)", "(?i)[?&]?([\w-]+)=({})"]
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
	
	chk = []
	for j in keyData:
		check = False
		for i in request['header_regex']:
			for k in regexHeader:
				x = re.search(k.format(i), j)
				# print("header",x, k.format(i),j)
				if(x is not None):
					testData['target'].append(j)
					chk.append(j)
					check = True
					break
				else:
					x = re.search(k.format(i), data[j]['request']['header'])
					if(x is not None):
						testData['target'].append(j)
						chk.append(j)
						check = True
						break
			if(check):
				break

	for i in chk:
		keyData.remove(i)
	chk = []

	for j in keyData:
		check = False
		for i in request['body_regex']:
			if(i == "*"):
				testData['target'].append("*")
				return testData
			for k in regexBody:
				x = re.search(k.format(i), data[j]['request']['body'])
				# print("body",x,k.format(i),data[j]['request']['body'])
				if(x is not None):
					testData['target'].append(j)
					chk.append(j)
					check = True
					break
			if(check):
				break
	
	for i in chk:
		keyData.remove(i)
	
	chk = []

	for j in keyData:
		check = False
		for i in response['header_regex']:
			for k in regexResponse:
				x = re.search(k.format(i), data[j]['response']['header'])
				if(x is not None):
					testData['target'].append(j)
					chk.append(j)
					check = True
					break
			if(check):
				break
	
	for i in chk:
		keyData.remove(i)
	
	chk = []

	for j in keyData:
		check = False
		for i in response['body_regex']:
			x = re.search(i, data[j]['response']['header'])
			if(x is not None):
				testData['target'].append(j)
				chk.append(j)
				check = True
				break
		if(check):
			break
	
	for i in chk:
		keyData.remove(i)

	fix = []
	if(testData["reflected"] == 1) :
		for j in testData['target']:
			resultCheck = checkReflected(data[j]['request'], data[j]['response'])
			if(resultCheck):
				fix.append(j)
		testData['target'] = fix
			
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
				x = re.search(k.format(j), url)
				if(x is not None):
					data['testCases'].append(i)
					check = False
					break
				else:
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
		if(check == False):
			if(testData[i]['reflected'] == 1):
				resultCheck = checkReflected(data['request'], data['response'])
				if(resultCheck == False):
					data['testCases'].remove(i)
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
	
	# for i in data:
	# 	print(i)
	
	if(level != 0):
		dataLevel = open(f"level/level{level}.data","r").read().split("\n") # check list level on main.py
		jsonData = filterTest(jsonData, dataLevel)

	if(reportType == 1):
		for i in jsonData:
			jsonData[i] = assignSimple(jsonData[i], data)
	elif(reportType == 2):
		cnt = 0
		if(level == 0 or level == 1):
			allEndpoint = []
			for i in jsonData:
				if(cnt < 23):
					allEndpoint.append(i)
					cnt += 1
				else:
					break
			for i in allEndpoint:
				del jsonData[i]
			for i in data:
				data[i] = assignDetail(jsonData, data[i], i)
			data['*'] = {}
			data['*']['testCases'] = allEndpoint
			jsonData = json.loads(f)
		else:
			for i in data:
				data[i] = assignDetail(jsonData, data[i], i)
	baseURL = getBaseURL(data)
	export(baseURL, data, jsonData, filePath, reportType)