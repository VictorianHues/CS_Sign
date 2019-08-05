import time
import bs4
import paho.mqtt.client as paho

broker = "192.168.1.33"

def onConnect(client, userdate, flags, rc):
    if rc == 0:
        print("Connect ok")
    else:
        print("Bad COnnection: ", rc)


def makeAnnouncement(message):

    client = paho.Client("Sign_Publisher")
    client.on_connect = onConnect
    
    print("Connecting to Broker: ", broker)
    client.connect(broker)
    print("Publishing")
    client.loop_start()
    
    client.publish("Announcement", message)
    
    client.loop_stop()

def makeEvent(date, time, eventName, message):

    client = paho.Client("Sign_Publisher")
    client.on_connect = onConnect
    
    print("Connecting to Broker: ", broker)
    client.connect(broker)
    print("Publishing")
    client.loop_start()
    
    client.publish("Event", message)
    client.publish("Date", date)
    client.publish("Name", eventName)
    client.publish("Time", time)
    
    client.loop_stop()


def makeGreeting(Name):
    client = paho.Client("Sign_Publisher")
    client.on_connect = onConnect
    
    print("Connecting to Broker: ", broker)
    client.connect(broker)
    print("Publishing")
    client.loop_start()
    
    client.publish("Name", name)
    
    client.loop_stop()
    
