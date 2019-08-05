import time
import bs4
import paho.mqtt.client as paho


broker = "192.168.1.33"


def onMessage(client, userdata, message):
    time.sleep(1)
    msg = str(message.payload.decode("utf-8"))
    outFile = open("myhtml.html", "w")
    print("recieved message:", msg)

    outFile.close()


def onConnect(client, userdate, flags, rc):
    if rc == 0:
        print("Connect ok")
    else:
        print("Bad COnnection: ", rc)
                                     

def signConnect():

    client = paho.Client("Sign_Subscriber")
    client.on_message = onMessage
    client.on_connect = onConnect
    
    print("Connecting to Broker: ", broker)
    client.connect(broker)
    print("Subscribing")
    client.loop_start()

    if client.subscribe("Announcement") == True:
        announce(message)
    if client.subscribe("Event") == True:
        
    if client.subscribe("Greeting") == True:
        
    
    while(True):
        time.sleep(4)
        print("Checking for Messages")
    
    client.loop_stop()

def announce(message):
    with open("1.html") as inf:
        text = inf.read()
        soup = BeautifulSoup(text)
    soup.head.append("TEST")

    with open("Test.html", "w") as outf:
        outf.write(str(soup))

