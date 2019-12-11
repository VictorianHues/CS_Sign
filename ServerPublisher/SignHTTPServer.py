
#SimpleServer.py
#Study http://docs.python.org/3/library/socket.html  for more info on sockets

from netTools import *
from Sign_Publisher import *
from bs4 import BeautifulSoup
import threading
import time
import random


def processRequest(s, addr):

    HTTPmsg = s.recv(10000)
    print(HTTPmsg.decode("ascii"))
    HTTPmsg = HTTPmsg.decode("ascii")

    response = ""
    
    if HTTPmsg[:3] == "GET":

        HTTPmsg = HTTPmsg[4:]
        spaceLoc = HTTPmsg.find(" ")
        resource = HTTPmsg[:spaceLoc]
        resource = resource.strip("/")

        if resource[-4:].lower() == "html":
            response = "HTTP/1.0 200 OK\n"
            response += "Content-Type: text/html\n"
            response +="\n" #

            inFile = open(resource, "r")
            response += inFile.read()
            s.send(response.encode("ascii"))

        elif resource[-3:].lower() == "jpg":
            response = "HTTP/1.0 200 OK\n"
            response += "Content-Type: image/jpeg\n"
            response += "\n"
            s.send(response.encode("ascii"))
            infile = open(resource, "rb")
            s.send(infile.read())
        elif resource[-3:].lower() == "php":
            response = "HTTP/1.0 200 OK\n"
            response += "Content-Type: text/html\n"
            response +="\n" #

            inFile = open(resource, "r")
            response += inFile.read()
            s.send(response.encode("ascii"))


##################################################
    elif HTTPmsg[:4] == "POST":

        HTTPmsg = HTTPmsg[5:]
        spaceLoc = HTTPmsg.find(" ")
        resource = HTTPmsg[:spaceLoc]
        resource = resource.strip("/")


##################################################
        if resource[-4:].lower() == "html":
            dataLoc = HTTPmsg.split("\n")
            inputData = dataLoc[-1]
            response = "HTTP/1.0 200 OK\n"
            response += "Content-Type: text/html\n"
            response +="\n" 

            formList = []
            current = ""
            for i in range(len(inputData)):
                if inputData[i-1] == "=":
                    current = ""
                if inputData[i] == "&":
                    formList.append(current)
                    print(current)
                    current = ""
                else:
                    current += inputData[i]
            formList.append(current)


            ##############If a signage request is recieved################
            if formList[0] == "signage":
                html = open("SignageTemplate.html").read()
                signList = open("SignList.txt", "r+")
                soup = BeautifulSoup(html, "html.parser")
                    

                lineRead = signList.readlines()
                for line in lineRead: # Read each line
                    newLine = []
                    newLine = soup.new_tag('br')

                    soup.body.append(newLine)
                    soup.body.append(line)

                open("Signage.html", "w").write(str(soup))

                inFile = open(resource, "r")
                response += inFile.read()
                s.send(response.encode("ascii"))
                signList.close()

            ####################Delete a Specific Sign#######################
            elif formList[0] == "delete":
                html = open("SubTemplate.html").read()
                signList = open("SignList.txt", "r")
                soup = BeautifulSoup(html, "html.parser")

                deleteNum = int(formList[1])
                lineRead = signList.readlines()
                signList.close()
                
                signList = open("SignList.txt", "w")
                for line in lineRead:
                    lineList = line.split(" ", 1)
                    signNum = int(lineList[0])
                    if signNum != deleteNum:
                        signList.write(line)
                    else:
                        newLine = []
                        newLine = soup.new_tag('br')
                        soup.body.append(newLine)
                        soup.body.append(line)
                signList.close()

                open("Sub.html", "w").write(str(soup))
                inFile = open(resource, "r")
                response += inFile.read()
                s.send(response.encode("ascii"))

                signList.close()
                
            ############If a Form Page is Recieved#################
            else:
                #######Return page with data to user########
                html = open("AddedTemplate.html").read()
                signList = open("SignList.txt", "r+")
                soup = BeautifulSoup(html, "html.parser")
                    
                lineWrite = ""

                lineRead = signList.readlines()
                currentNum = 1
                locFound = 0;

                for line in lineRead: # Read each line
                    lineList = line.split(" ", 1)
                    signNum = int(lineList[0])
                    if locFound == 0:
                        if currentNum != signNum:
                            locFound = 1;
                        else:
                            currentNum = currentNum + 1
                lineWrite += str(currentNum)
                lineWrite += ' '
                signList.close()

                
                signList = open("SignList.txt", "a+")
                newLine = []
                newLine = soup.new_tag('br')
                
                soup.body.append(newLine)
                for i in range(len(formList)):
                    newLine[i] = soup.new_tag('br')
                    newLine[i].string = formList[i]
                    soup.body.append(newLine[i])
                    lineWrite += formList[i]
                    lineWrite += ' '

                open("Added.html", "w").write(str(soup))

                inFile = open(resource, "r")
                response += inFile.read()
                s.send(response.encode("ascii"))

                lineWrite += '\n'
                signList.write(lineWrite)
                makeSign(inputData)

                signList.close()

        elif resource[-3:].lower() == "jpg":
            response = "HTTP/1.0 200 OK\n"
            response += "Content-Type: image/jpeg\n"
            response += "\n"
            s.send(response.encode("ascii"))
            infile = open(resource, "rb")
            s.send(infile.read())
        
            
    
    else:
        response  = "HTTP/1.0 501 Not Implemented\n"
        response += "\n"
        response += "ERROR\n"
        response += "\n"

        s.send(response.encode("ascii"))

        
    s.close()
    

def HTTPServer():
    
    serversocket = socket(AF_INET, SOCK_STREAM)
    serversocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    host = getIPAddress()
    print("Listening on: ", host, ":2080")
    serversocket.bind((host, 2080))

    serversocket.listen(1)

    while True:
        print("Waiting for connection....")
        clientsocket,addr = serversocket.accept()
        print ("Connnection from", addr) 
        threading.Thread(target=processRequest, args=(clientsocket, addr)).start()
            
    serversocket.close()


HTTPServer()


