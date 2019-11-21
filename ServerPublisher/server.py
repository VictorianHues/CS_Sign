import http.server
import socketserver
import time
import paho.mqtt.client as paho

PORT = 8080
Handler = http.server.SimpleHTTPRequestHandler
##broker = "192.168.1.33"
##
##
##client = paho.Client("Announcement Server")
##client.on_message = onMessage
##client.on_connect = onConnect
##
##print("Connecting to Broker: ", broker)
##client.connect(broker)
##print("Subscribing")
##client.loop_start()
##client.subscribe("TEST")
##    
####client.publish("testHTML", "Blue")


with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("serving at port", PORT)
    print("Checking for Messages")
    httpd.serve_forever()

client.loop_stop()



##def onMessage(client, userdata, message):
##    time.sleep(1)
##    msg = str(message.payload.decode("utf-8"))
##    print("recieved message:", msg)
##    if msg == "Test1":
##        client.publish("TEST", "Test1")
##    if msg == "Test2":
##        client.publish("TEST", "Test2")
##
##
##def onConnect(client, userdate, flags, rc):
##    if rc == 0:
##        print("Connect ok")
##    else:
##        print("Bad Connection: ", rc)
