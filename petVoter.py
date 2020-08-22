import json
import sys
import threading
import requests
import threading
import time

def proxyThread(proxyFile, threadID):
    with open(proxyFile, 'r') as f:
        proxylist = json.load(f)
    for currentProxy in proxylist:
        proxy = { 'http' : currentProxy,
          'https' : currentProxy}
        url = 'https://www.delfi.lt/apps/augintinis/api/vote/'
        header ={
            'Content-Length' : '138',
            'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36 OPR/67.0.3575.115',
            'Origin' : 'https://www.delfi.lt',
            'Referer' : 'https://www.delfi.lt/apps/augintinis/dalyvis/51870'
        }
        print(currentProxy)
        session = requests.Session()
        error = False
        try:
            session.head('https://www.delfi.lt/apps/augintinis/dalyvis/51870', proxies=proxy)
        except:
            print("Proxy/load error at: " + currentProxy)
            error = True
        if error == False:
            for i in range(1, 10):
                try:
                    req = session.post(url, headers=header, data={'id' : '51870'}, proxies=proxy)
                    print(req.text)
                    if req.text is not None:
                        writefile = open("proxyFixed.txt", "a") 
                        writefile.write('"' + currentProxy + '",\n')
                        writefile.close()
                        time.sleep(1)
                except:
                    print("Proxy/load error at: " + currentProxy)
                    break
    print("BOT " + threadID.__str__() + " HAS FINISHED !")

for i in range(1,19):
    print(i)
    currentThread = threading.Thread(target=proxyThread, args=["proxylist" + i.__str__() +".json", i])
    currentThread.start()