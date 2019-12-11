import time
from bs4 import BeautifulSoup
import paho.mqtt.client as paho

broker = "172.16.14.52"

def onConnect(client, userdate, flags, rc):
    if rc == 0:
        print("Connect ok")
    else:
        print("Bad COnnection: ", rc)


def makeSign(message):
    client = paho.Client("Sign_Publisher")
    client.on_connect = onConnect
    
    print("Connecting to Broker: ", broker)
    client.connect(broker)
    print("Publishing")

    time.sleep(1)
    client.publish("Sign/Any", message)

def deleteSign(message):
    client = paho.Client("Sign_Publisher")
    client.on_connect = onConnect
    
    print("Connecting to Broker: ", broker)
    client.connect(broker)
    print("Publishing")

    time.sleep(1)
    client.publish("Sign/Delete", message)
