#!/usr/bin/python
import json
import praw
import requests
import time
import os
header = {'x-requested-with': 'XMLHttpRequest'}
URL = "http://www.fplstatistics.co.uk/Home/AjaxPricesHandler?sEcho=2&iColumns=12&sColumns=%2Cweb_name%2CPClubName%2CPosition%2CStatus%2CpercentSelected%2CCost%2CPriceChangesinGW%2Cunlockdt%2CNTIDelta%2CNTIPERCENTNJD%2CPId&mDataProp_0=0&sSearch_0=&bRegex_0=false&bSearchable_0=true&bSortable_0=false"
#&iDisplayStart=1&iDisplayLength=50

def mainFunction(): 

	user_agent = "houseOfBalloons 1.1" #user_agent

	r = praw.Reddit(user_agent=user_agent) # reddit instance
	r.login(os.environ['REDDIT_USERNAME'], os.environ['REDDIT_PASSWORD']) #login
	risers = getRisers()
	fallers = getFallers()


	if (risers and fallers):
		today = time.strftime("%d %B %Y")
		message = generateMessage(risers, fallers)
		title = " Fantasy Premier League Price Change Predictions (" + today + ")"
		r.submit('fantasypl', title, text = message)
		print "Post Sent!"
		return True
	else:
		print "Risers or fallers was null"
		return False

def generateMessage(risers, fallers):
	today = time.strftime("%d %B %Y")
	newLine = "\r\n\r\n&nbsp;\r\n\r\n"
	hr = "\r\n\r\n---\r\n\r\n"

	message = "**PRICE RISE PREDICTIONS** \r\n"
	message += newLine

	
	message +=  "**Highly Likely Risers** \r\n"
	message += genTable(risers['high'])
	message += newLine
	message +=  "**Likely Risers** \r\n"
	message += genTable(risers['med'])
	message += newLine
	message +=  "**Possible Risers** \r\n"
	message += genTable(risers['low'])
	message += newLine

	message += hr
	message += "**PRICE FALL PREDICTIONS** \r\n"
	message += newLine

	message +=  "\r\n **Highly Likely Fallers** \r\n"
	message += genTable(fallers['high'])
	message += newLine
	message +=  "**Likely Fallers** \r\n"
	message += genTable(fallers['med'])
	message += newLine
	message +=  "**Possible Fallers** \r\n"
	message += genTable(fallers['low'])
	message += newLine
	message += hr
	message += "- Data Source: www.fplstatistics.co.uk  \r\n - I am a bot. Message /u/trent_9002 for any criticism/suggestions."

	return message


def genTable(data):
	if not data:
		message = "\r\n *None for today*\r\n"
		return message
	message = "\r\n"
	message += "Player Name|Club|Position|Ownership(%)|Current Price|Likelihood\r\n"
	message += ":-:|:-:|:-:|:-:|:-:|:-:\r\n"
	for each in data:
		name = each[1]
		club = each[2]
		pos = each[3]
		owners = each[5]
		price = each[6]
		change = each[10]
		message += name + "|" + club + "|" + pos + "|" + owners + "|" + price + "|" + change + "\r\n"
	return message


def getRisers():
	riseUrl = URL + "&iDisplayStart=0&iDisplayLength=50"
	try:
		output = requests.get(riseUrl, headers = header)
	except Exception, e:
		print "Risers wasn't downloaded"
		return False
	result = output.json()
	try:
		result = result["aaData"]
	except Exception, e:
		print "No aaData for risers was found"
		return False
	high = []
	med = []
	low = []
	for elem in result:
		val = elem[10]
		if (float(val) >= 100):
			#high prob fall
			high.append(elem)
		elif (float(val) >= 90):
			med.append(elem)
		elif (float(val) >= 80):
			low.append(elem)
		else:
			break
	retValue = {"high": high, "med": med, "low": low}
	return retValue



def getFallers():
	
	fallUrl = URL + "&iDisplayStart=488&iDisplayLength=588"
	try:
		output = requests.get(fallUrl, headers = header)
	except Exception, e:
		print "Fallers wasn't downloaded"
		return False
	result = output.json()
	try:
		result = result["aaData"]
	except Exception, e:
		print "No aaData for fallers was found"
		return False
	high = []
	med = []
	low = []
	result.reverse()
	for elem in result:
		val = elem[10]
		if (float(val) <= -100):
			#high prob fall
			high.append(elem)
		elif (float(val) <= -95):
			med.append(elem)
		elif (float(val) <= -85):
			low.append(elem)
		else:
			break
	retValue = {"high": high, "med": med, "low": low}
	return retValue


mainFunction()



			



