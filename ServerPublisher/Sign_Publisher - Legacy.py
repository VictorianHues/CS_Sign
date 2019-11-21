import time
from bs4 import BeautifulSoup
import paho.mqtt.client as paho

broker = "172.16.14.52"

def onConnect(client, userdate, flags, rc):
    if rc == 0:
        print("Connect ok")
    else:
        print("Bad COnnection: ", rc)


def makeAny(message):
    client = paho.Client("Sign_Publisher")
    client.on_connect = onConnect
    
    print("Connecting to Broker: ", broker)
    client.connect(broker)
    print("Publishing")

    time.sleep(1)
    client.publish("Sign/Any", message)


def makeAnnouncement(message):

    client = paho.Client("Sign_Publisher")
    client.on_connect = onConnect
    
    print("Connecting to Broker: ", broker)
    client.connect(broker)
    print("Publishing")

    client.publish("Sign", "1")
    time.sleep(1)
    client.publish("Sign/Announcement", message)

def makeEvent(date, time, eventName, message):

    client = paho.Client("Sign_Publisher")
    client.on_connect = onConnect
    
    print("Connecting to Broker: ", broker)
    client.connect(broker)
    print("Publishing")
    
    client.publish("Sign", "3")
    client.publish("Sign/Event/Name", eventName)
    client.publish("Sign/Event/Date", date)
    client.publish("Sign/Event/Time", time)
    client.publish("Sign/Event", message)


def makeGreeting(name):
    client = paho.Client("Sign_Publisher")
    client.on_connect = onConnect
    
    print("Connecting to Broker: ", broker)
    client.connect(broker)
    print("Publishing")

    client.publish("Sign", "2")
    time.sleep(1)
    client.publish("Sign/Greeting", name)
    
