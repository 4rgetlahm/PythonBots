import json
import sys
import threading

from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.proxy import *
import datetime
from datetime import date, time
import calendar
import time
from random import randrange
import threading

def proxyThread(proxyFile, threadID):
    with open(proxyFile, 'r') as f:
        proxylist = json.load(f)
    for currentProxy in proxylist:
        currdate = datetime.datetime.now()
        generateURL += calendar.day_abbr[currdate.weekday()]
        generateURL += " " + calendar.month_abbr[currdate.today().month] + " " + str(currdate.today().day) + " " + str(
            currdate.today().year)
        generateURL += " " + currdate.strftime("%H:%M:%S")
        generateURL += " GMT+0200 (Eastern European Standard Time)"

        print(currentProxy)
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--proxy-server=%s' % currentProxy)
        chrome_options.add_argument("--headless")
        try:
            chrome = webdriver.Chrome(options=chrome_options)
            #chrome.get("https://www.delfi.lt/apps/duokzaiba/mokykla/297/")   #vote by clicking
            #chrome.find_element_by_xpath("/html/body/div[1]/div[2]/div[4]/div/div[1]/span[1]").click()
            chrome.get(generateURL) #vote by going to vote api url
            if chrome.find_element_by_xpath("/html/body").text == "1":
                writefile = open("proxyFixed.txt", "a") 
                writefile.write('"' + currentProxy + '",\n')
                writefile.close()
            #time.sleep(10)
            chrome.quit()
        except Exception as e:
            print("Loading error, proxy: " + currentProxy)
    #rand = randrange(100)
    #print("SLEEP FOR: " + str(rand) +"s")
    print("BOT " + threadID + " HAS FINISHED !")

for i in range(1,33):
    print(i)
    currentThread = threading.Thread(target=proxyThread, args=["proxylist" + i.__str__() +".json", i])
    currentThread.start()