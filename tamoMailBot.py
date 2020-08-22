from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import threading
import time

username = ""
password = ""
manualID = 18
sender = ""

def login(chrome, username, password):
    chrome.find_element_by_xpath("//*[@id='UserName']").send_keys(username)
    chrome.find_element_by_xpath("//*[@id='Password']").send_keys(password)
    chrome.find_element_by_xpath("//*[@id='main_form']/div/div[3]/a").click()

def sendMail(chrome, uid, title, msg):
    try:
        chrome.get(url + "/Pranesimai")
        time.sleep(1)
        chrome.find_element_by_xpath("//*[@id='messages_tab']/ul/li[3]/a").click()
        time.sleep(2)
        chrome.find_element_by_xpath("/html/body/div[5]/div[2]/div[2]/div[2]/div/div/div[2]/form/div/div[1]/div/div/div[1]/select").click()
        chrome.find_element_by_xpath("//*[@id='GavejoTipas']/option[6]").click()
        time.sleep(2)
        chrome.find_element_by_xpath("//*[@id='SukurtiPranesimaForm']/div/div[1]/div/div/div[3]/div[" + uid.__str__() + "]/div/div/child::input[@type='checkbox']").send_keys(Keys.SPACE)
        chrome.find_element_by_xpath("//*[@id='Pavadinimas']").send_keys(title)
        chrome.find_element_by_xpath("//*[@id='message_text_area']").send_keys(msg)
        chrome.find_element_by_xpath("//*[@id='SukurtiPranesimaBtn']").click()
    except:
        print("Įvyko klaida su laiško siuntimu")

def mailingThread(chrome, uid, title):
    i = 0
    while True:
        i += 1
        print(i)
        sendMail(chrome, uid, title, i.__str__())

def readMail(chrome, sender):
    chrome.get(url + "/Pranesimai")
    try:
        chrome.find_elements_by_class_name("msg_item_notread")[0].click()
        time.sleep(2.2)
        if(sender in chrome.find_element_by_xpath("/html/body/div[5]/div[2]/div[2]/div[2]/div/div/div/div[2]/div/form/div[3]/div/div/div/p[1]").text):
            chrome.find_element_by_xpath("/html/body/div[5]/div[2]/div[2]/div[2]/div/div/div/div[2]/div/form/div[1]/div/a[3]").click()
            time.sleep(2.2)
            chrome.find_element_by_xpath("/html/body/div[12]/div/div[5]/button[2]").click()
    except:
        print("Klaida skaitant/trinant laišką! (gali būti, kad laiškų nėra)")

def readingThread(chrome, sender):
    while True:
        readMail(chrome, sender)

url = "https://dienynas.tamo.lt"

chrome_options = webdriver.ChromeOptions()
#chrome_options.add_argument("--headless")
mailing = webdriver.Chrome(options=chrome_options)
mailing.get(url)
try:
    mailing.find_element_by_xpath("//*[@id='CybotCookiebotDialogBodyButtonAccept']").click()
except:
    print("No cookie confirm box?")
login(mailing, username, password)
mailThread = threading.Thread(target=mailingThread, args=[mailing, manualID, "bandymas"])
mailThread.start()

reading = webdriver.Chrome(options=chrome_options)
reading.get(url)
try:
    reading.find_element_by_xpath("//*[@id='CybotCookiebotDialogBodyButtonAccept']").click()
except:
    print("No cookie confirm box?")
login(reading, username, password)
readThread = threading.Thread(target=readingThread, args=[reading, sender])
readThread.start()