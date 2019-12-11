import os
import time
from bs4 import BeautifulSoup
import paho.mqtt.client as paho


broker = "172.16.14.52"

signList = []
currentSign = 0
current = ""
currentType = ""

def onMessage(client, userdata, message):
    print("START TEST")
    time.sleep(1)
    msg = str(message.payload.decode("utf-8"))
    print("recieved message:", msg)
    currentSign = currentSign + 1
    print(currentSign)
    signList.append(currentSign)
    current = str(currentSign) + ".html"
    currentType = msg
    print(current)

def onMessageDelete(client, userdata, message):
    time.sleep(1)
    msg = str(message.payload.decode("utf-8"))
    print("recieved message:", msg)

    formList = []
    current = ""
    for i in range(len(msg)):
        if msg[i-1] == "=":
            current = ""
        if msg[i] == "&":
            formList.append(current)
            print(current)
            current = ""
        elif msg[i] == "+":
            current += " "
        else:
            current += msg[i]
    formList.append(current)

    formDelete = formList[1]
    print("DELETE")

    dir_path = os.path.dirname(os.path.realpath(__file__))
    for root, dirs, files in os.walk(dir_path): 
    for file in files:  
        if file.startswith(str(formDelete)): 
            os.remove(file)
        
    



def onMessageAny(client, userdata, message):
    time.sleep(1)
    msg = str(message.payload.decode("utf-8"))
    print("recieved message:", msg)

    formList = []
    current = ""
    for i in range(len(msg)):
        if msg[i-1] == "=":
            current = ""
        if msg[i] == "&":
            formList.append(current)
            print(current)
            current = ""
        elif msg[i] == "+":
            current += " "
        else:
            current += msg[i]
    formList.append(current)

    template = ""
    if formList[0] == "event":
        print("EVENT")
        template = "Event.html"
        output = formList[5]
        output += ".html"
    elif formList[0] == "announce":
        print("ANNOUNCEMENT")
        template = "Announce.html"
        output = "Announce1.html"
        output = formList[2]
        output += ".html"
    elif formList[0] == "greet":
        print("GREETING")
        template = "Greet.html"
        output = "Greet1.html"
        output = formList[2]
        output += ".html"


    html = open(template).read()
    soup = BeautifulSoup(html)
        

    newLine = []
    newLine = soup.new_tag('br')

    soup.body.append(newLine)
    for i in range(len(formList)):
        newLine[i] = soup.new_tag('br')
        newLine[i].string = formList[i]
        soup.body.append(newLine[i])
        ##soup.body.append(formList[i])
        print(formList[i])

    open(output, "w").write(str(soup))


    
def onConnect(client, userdate, flags, rc):
    if rc == 0:
        print("Connect ok")
    else:
        print("Bad Connection: ", rc)
                                     

def signConnect():

    client = paho.Client("Sign_Subscriber")
    client.on_message = onMessage
    client.on_connect = onConnect
    
    print("Connecting to Broker: ", broker)
    client.connect(broker)
    print("Subscribing")

    client.message_callback_add("Sign/Any", onMessageAny)
    client.message_callback_add("Sign/Delete", onMessageDelete)

    client.loop_start()

    client.subscribe("Sign/#")

    while(True):
        time.sleep(4)
        print("Checking for Messages")
    
    client.loop_stop()



signConnect()
