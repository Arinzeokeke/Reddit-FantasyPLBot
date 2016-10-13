#!/usr/bin/python
import json
import praw
import requests
import time
import os
from bs4 import BeautifulSoup
from config_skel import *
header = {'x-requested-with': 'XMLHttpRequest'}
URL = "http://www.fplstatistics.co.uk/Home/AjaxPricesHandler?sEcho=2&iColumns=12&sColumns=%2Cweb_name%2CPClubName%2CPosition%2CStatus%2CpercentSelected%2CCost%2CPriceChangesinGW%2Cunlockdt%2CNTIDelta%2CNTIPERCENTNJD%2CPId&mDataProp_0=0&sSearch_0=&bRegex_0=false&bSearchable_0=true&bSortable_0=false"
#&iDisplayStart=1&iDisplayLength=50

def mainFunction(): 
	if not os.path.isfile("config_skel.py"):
		print "You must create a config file with your username and password."
		print "Please see config_file.py"
		exit(1)

	user_agent = "houseOfBalloons 1.0" #user_agent

	r = praw.Reddit(user_agent=user_agent) # reddit instance
	r.login(REDDIT_USERNAME, REDDIT_PASS) #login

	subreddit = r.get_subreddit('fantasypl') #FantasyPL subreddit

	risers = getRisers()
	fallers = getFallers()
	print risers
	print fallers

	if (risers and fallers):
		message = generateMessage(risers, fallers)
		print message
		r.send_message('totallyjeffstrongman', 'PRAW Thread', message)
		print "Message Sent!"
		return True
	else:
		return False

def generateMessage(risers, fallers):
	today = time.strftime("%d %B %Y")

	message = "### ** Fantasy Premier League Price Rise/Fall Predictions (" + today + ")\r\n**"
	message +=  "\r\n\t\t ###Highly Likely Risers\r\n"
	message += genTable(risers['high'])
	message +=  "\r\n\t\t ### Likely Risers\r\n"
	message += genTable(risers['med'])
	message +=  "\r\n\t\t ### Possible Risers\r\n"
	message += genTable(risers['low'])

	message +=  "\r\n\n ### Highly Likely Fallers\r\n"
	message += genTable(fallers['high'])
	message +=  "\r\n\t\t ### Likely Fallers\r\n"
	message += genTable(fallers['med'])
	message +=  "\r\n\t\t ### Possible Fallers\r\n"
	message += genTable(fallers['low'])
	message += "\r\n\r\n - Data Source: www.fplstatistics.co.uk  \r\n - I am a bot. Message /u/trent_9002 for any criticism/suggestions."
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
		return False
	result = output.json()
	try:
		result = result["aaData"]
	except Exception, e:
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
		return False
	result = output.json()
	try:
		result = result["aaData"]
	except Exception, e:
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
		elif (float(val) <= -90):
			med.append(elem)
		elif (float(val) <= -80):
			low.append(elem)
		else:
			break
	retValue = {"high": high, "med": med, "low": low}
	return retValue

mainFunction()



			



