#Author : Vivek Kumar
#Email : kumarvivek7204[at]gmail[dot]com

#References : 
#1)http://home.iitk.ac.in/~saiwal/python/send-sms-way2sms-python/
#2)stackoverflow.com


#Script to automatically fetch cricket score every 2 minutes from cricbuzz and send it as a message to any number using way2sms
#change url of match from cricbuzz in line 51
import mechanize
import csv
import re
from bs4 import BeautifulSoup as bs
from getpass import getpass
import os
from socket import error as SocketError
import errno
import sys
import urllib2
import cookielib
from getpass import getpass
from stat import *
import schedule
import time
#Number of balls thrown in current innings
def getOver(overstr):
	for i in range(0,len(overstr)):
		if overstr[i] == '(':
			break
	for j in range(i,len(overstr)):
		if overstr[j] == '.':
			break
	return int(overstr[(i+1):j])*6 + int(overstr[j+1])


#Login and Password of way2sms
username = "Mobile number"
passwd = "password"
#Mobile number for message to be sent at 
number = "number"
#previousBall = 0
reload(sys)
sys.setdefaultencoding('utf-8')
#Function to fetch scoreboard (current score, current batsman along with score, Runrate, )
def job():
	browser = mechanize.Browser()
	browser.set_handle_robots(False)
	browser.addheaders = [('user-agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0'), ('accept','text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')]
	#paste url of live match from cricbuzz here	
	response = browser.open("url")
	#response contains entire html of webpage in an object form
	soup = bs(response.read(),"lxml")
	#soup converts it to html form 
	data=soup.find("div",{"class":"cb-min-lv"})
	#data contains html of scoreboard section
	#if data is empty ==> match has ended => give previous result
	scoreHTML = data.find("div",{"class":"cb-min-bat-rw"})
	score = scoreHTML.text
	score = ' '.join(score.split())
	textInProgress = data.find("div",{"class":"cb-text-inprogress"}).text.strip().encode('ascii')
	batsmanScoreHTML = data.findAll("div",{"class":"cb-min-itm-rw"})
	data1 = batsmanScoreHTML[0].findAll("div",{"class":"cb-col"})
	data2 = batsmanScoreHTML[1].findAll("div",{"class":"cb-col"})
	player1 = data1[0].text.strip().encode('ascii')
	run1 = data1[1].text.strip().encode('ascii')
	ball1 = data1[2].text.strip().encode('ascii')
	player2 = data2[0].text.strip().encode('ascii')
	run2 = data2[1].text.strip().encode('ascii')
	ball2 = data2[2].text.strip().encode('ascii')
	#player1 is name of batsman1, ball1 is number of balls played by batsman1 and run1 is run scored by batsman1
	batscore = player1 + ": "+ str(run1) + "("+str(ball1)+")" + "  "+player2 + ": "+ str(run2) + "("+str(ball2)+")" 
	result = str(score) + "\n" + str(batscore) + "\n" + str(textInProgress)
	#print result
	#print previousBall
	#currentBall = getOver(score)
	#print currentBall
	#if currentBall != previousBall:
	#	previousBall = currentBall
	print result

	#This Section containse code to send message and is taken from http://home.iitk.ac.in/~saiwal/python/send-sms-way2sms-python/
	url ='http://site24.way2sms.com/Login1.action?'
	data = 'username='+username+'&password='+passwd+'&Submit=Sign+in'
	cj= cookielib.CookieJar()
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
	opener.addheaders=[('user-agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0'), ('accept','text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')]
	try:
	    usock =opener.open(url, data)
	except IOError:
	    print "error"
	jession_id =str(cj).split('~')[1].split(' ')[0]
	send_sms_url = 'http://site24.way2sms.com/smstoss.action?'
	send_sms_data = 'ssaction=ss&Token='+jession_id+'&mobile='+number+'&message='+result+'&msgLen=136'
	opener.addheaders=[('Referer', 'http://site25.way2sms.com/sendSMS?Token='+jession_id)]
	try:
	    sms_sent_page = opener.open(send_sms_url,send_sms_data)
	except IOError:
	    print "error"
	    #return()

	print "success"
#This section contains code to schedule the task
schedule.every(2).minutes.do(job)
while True:
    schedule.run_pending()
    time.sleep(1)


