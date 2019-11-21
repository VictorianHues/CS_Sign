import time
from bs4 import BeautifulSoup
import paho.mqtt.client as paho


broker = "172.16.14.52"

signList = []
currentSign = 0
current = ""
currentType = ""

def onMessage(client, userdata, message):
    print("STAART TEST")
    time.sleep(1)
    msg = str(message.payload.decode("utf-8"))
    print("recieved message:", msg)
    currentSign = currentSign + 1
    print(currentSign)
    signList.append(currentSign)
    current = str(currentSign) + ".html"
    currentType = msg
    print(current)

def onMessageAnnouncement(client, userdata, message):
    print("TEST")
    time.sleep(1)
    msg = str(message.payload.decode("utf-8"))
    print("recieved message:", msg)

    with open("Announce.html") as inf:
        text = inf.read()
        soup = BeautifulSoup(text)
        
    soup.body.append("\n")
    soup.body.append(msg)

    with open("test.html", "w") as outf:
        outf.write(str(soup))

def onMessageGreeting(client, userdata, message):
    print("TEST")
    time.sleep(1)
    msg = str(message.payload.decode("utf-8"))
    print("recieved message:", msg)

    with open("Greet.html") as inf:
        text = inf.read()
        soup = BeautifulSoup(text)

    soup.body.append("\n")
    soup.body.append(msg)

    with open("test.html", "w") as outf:
        outf.write(str(soup))

def onMessageEvent(client, userdata, message):
    print("TEST")
    time.sleep(1)
    msg = str(message.payload.decode("utf-8"))
    print("recieved message:", msg)

    with open("Event.html") as inf:
        text = inf.read()
        soup = BeautifulSoup(text)
    
    soup.body.append("\n")
    soup.body.append(msg)

    with open("test.html", "w") as outf:
        outf.write(str(soup))

def onMessageDate(client, userdata, message):
    print("TEST")
    time.sleep(1)
    msg = str(message.payload.decode("utf-8"))
    print("recieved message:", msg)

    with open("test.html") as inf:
        text = inf.read()
        soup = BeautifulSoup(text)

    soup.body.append("\n")
    soup.body.append(msg)

    with open("test.html", "w") as outf:
        outf.write(str(soup))

def onMessageName(client, userdata, message):
    print("TEST")
    time.sleep(1)
    msg = str(message.payload.decode("utf-8"))
    print("recieved message:", msg)

    with open("test.html") as inf:
        text = inf.read()
        soup = BeautifulSoup(text)

    soup.body.append("\n")
    soup.body.append(msg)

    with open("test.html", "w") as outf:
        outf.write(str(soup))

def onMessageTime(client, userdata, message):
    print("TEST")
    time.sleep(1)
    msg = str(message.payload.decode("utf-8"))
    print("recieved message:", msg)

    with open("test.html") as inf:
        text = inf.read()
        soup = BeautifulSoup(text)

    soup.body.append("\n")
    soup.body.append(msg)

    with open(current, "w") as outf:
        outf.write(str(soup))

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
        else:
            current += msg[i]

    if formList[0] == "event":
        with open("Event.html") as inf:
            text = inf.read()
            soup = BeautifulSoup(text)

    soup.body.append("\n")
    for i in range(len(formList)):
        soup.body.append(formList[i])
        print(formList[i])

    with open(current, "w") as outf:
        outf.write(str(soup))


    
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
    client.message_callback_add("Sign/Announcement", onMessageAnnouncement)
    client.message_callback_add("Sign/Greeting", onMessageGreeting)
    client.message_callback_add("Sign/Event", onMessageEvent)
    client.message_callback_add("Sign/Event/Date", onMessageDate)
    client.message_callback_add("Sign/Event/Name", onMessageName)
    client.message_callback_add("Sign/Event/Time", onMessageTime)

    client.loop_start()

    client.subscribe("Sign/#")

    while(True):
        time.sleep(4)
        print("Checking for Messages")
    
    client.loop_stop()



signConnect()


##
##def checkList():
##
##    currentNum = 1
##    more = True
##    
##    while more == True:
##        try:
##            f = open(currentNum + ".html")
##            f.close()
##            signList.append(currentNum)
##            currentNum++
##        except IOError:
##            more = False
##

