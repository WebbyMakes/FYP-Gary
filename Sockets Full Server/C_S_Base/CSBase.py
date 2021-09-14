#Client/Server Base code
#This file will combine the client and server capabilities and allows to swap between client and server capabilities

#Terms | Client = The SENDER of a file | Server = The RECEIVER of a file
#Import libraries
#from os import system
#system('cls')

import socket
import tqdm
import os
from tabulate import tabulate

fileName = "testData.csv"
fileLocation = "C:\\Users\\Capta\\Desktop\\Lil Gary\\Sockets Server\\Base Test\\clientTest" #Change this - Maybe store this in a variable
fullFileName = fileLocation + "\\" + fileName
filesize = os.path.getsize(fullFileName)    #Get size of file

class Server:
    def __init__(self):
        self.serverType = "Undefined"
        self.serverStatus = "Undefined"
        self.SEPARATOR = "<SEPARATOR>"
        self.BUFFER_SIZE = 4096 #Send 4096 bytes each time 'step'

        #IP Addresses
        self.deviceIP = "192.168.0.107"     #IP of current device
        self.serverIP = "192.168.0.107"     #IP of device to send to (Base Server)
        self.port = 5001                    #Port to use
        self.fileName = ""                  #File Name
        self.location = ""                  #Location of file
        self.fullFileName = ""              #FileName + Location
        self.fileSize = 0                   #Calculated Size of File

        #Connections
        #self.clientSocket = None            #Defined Client Socket
        #self.address = None                 #Addresses connected
    
    def checkWorking(self, debug):
        error = False

        if (error == True):
            if (debug == 1):
                print("| Server Failed to Start")
        else:
            if (debug == 1):
                print("| Server Started")
            self.serverStatus = "Idle"

    def getServerInformation(self):
        table = [
            ['Server Type', self.serverType],
            ['Server Status', self.serverStatus],
            ['Buffer Size (bytes)', self.BUFFER_SIZE],
            ['Device IP', self.deviceIP],
            ['Server IP', self.serverIP],
            ['Port', self.port],
            ['File Name', self.fileName],
            ['File Address', self.location],
            ['Absolute File Location', self.fullFileName],
            ['Size of File (bytes)', self.fileSize]
        ]
        print(tabulate(table))

    def getServerStatus(self):
        table = [
            ['Server Type', self.serverType],
            ['Server Status', self.serverStatus]
        ]
        print(tabulate(table))

    def setFileInformation(self, fileName, fileLocation, debug):
        self.fileName = fileName
        self.location = fileLocation
        self.fullFileName = fileLocation + "\\" + fileName
        self.fileSize = os.path.getsize(self.fullFileName)
        if (debug == 1):
            print("| File Information Set")

    def setServerType(self, sType, debug):
        if (sType == "Client"):
            self.serverType = "Client"
        elif (sType == "Server"):
            self.serverType = "Server"
        else:
            self.serverType = "Undefined"
            print("| Server Type Failed to set")
        if (debug == 1):
            print("| Server set as " + str(self.serverType))
    
    def deviceIPSet(self, deviceIP, debug):
        self.deviceIP = deviceIP
        if(debug == 1):
            print("| Device IP Set")

    def serverIPSendSet(self, sendIP, debug):
        self.serverIP = sendIP
        if (debug == 1):
            print("| Destination IP Set")

    def portSet(self, port, debug):
        self.port = port
        if (debug == 1):
            print("| Port Set")
    def clientConnect(self, s, debug):
        if (self.serverType == "Client"):
            try:
                print(f"| [+] Connecting to {self.serverIP}:{self.port}")
                s.connect((self.serverIP, self.port))
                print("| [+] Connected to Server.")
                self.serverStatus == "Connected"
                return s
            except ConnectionRefusedError:
                if (debug == 1):
                    print("| Server could not connect")
                return s
            except TimeoutError:
                if (debug == 1):
                    print("| Connection Timed Out")
                return s
        else:
            print("| Can only use if server is a client")
            return s
    
    def clientSend(self, s):
        error = False
        if (self.fileName == "" or self.location == "" or self.fullFileName == ""):
            error = True
        elif (self.serverType != "Client"):
            error = True
        elif (self.serverStatus != "Connected"):
            error = True
        
        if (error == False):
            s.send(f"{self.fileName}{self.SEPARATOR}{self.fileSize}".encode())

            progress = tqdm.tqdm(range(self.fileSize), f"sending{self.fileName}", unit = "B", unit_sccale = True, unit_divisor = 1024)
            with open(self.fileName, "rb") as f:
                while True:
                    bytes_read = f.read(self.BUFFER_SIZE)   #Read the bytes in from file
                    if not bytes_read:
                        break                           #File transmitting is done
                    s.sendall(bytes_read)               #We use sendall to assure transmission in busy networks
                    progress.update(len(bytes_read))    #Update Progress Bar
            s.close     #Close the socket
        elif (self.serverStatus != "Connected" and error == True):
            print("| Server Not Connected")
            self.serverStatus = "Not Connected"
        else:
            print("| Unknown Error Detected")
        return s

    def serverListenAndReceive(self, s):
        s.bind((self.deviceIP, self.port))    #Bind the socket to out local address
        s.listen(5)     #Allows our server to accept connections, the number corresponds to the number of unaccepted connections that the system will allow before refusing new connections
        print(f"[*] Listening as {self.deviceIP}:{self.port}")

        clientSocket, address = s.accept()   #Accept connection if there is any

        print(f"[+] {address} is connected")  #If this line is executed, that means the sender is connected    

        #Receive the file info = receive using client socket, not server socket
        received = clientSocket.recv(self.BUFFER_SIZE).decode()
        fileName, fileSize = received.split(self.SEPARATOR)

        #Could replace this with just straight file name
        fileName = os.path.basename(self.fileName)  #Remove absolute path is present

        fileNameDump = fileName + "Dump"

        fileSize = int(fileSize)    #Convert to Integer

        #Start receiving the file from the socket and writing to the file stream
        progress = tqdm.tqdm(range(fileSize), f"Receiving {fileName}", unit = "B", unit_scale = True, unit_diviser = 1024)
        with open(fileNameDump, "wb") as f:
            while True:
                #Read 1024 bytes from the socket (receive)
                bytes_read = clientSocket.recv(self.BUFFER_SIZE)
                if not bytes_read:
                    break   #If nothing is received, file transmitting is done
                f.write(bytes_read) #Write to the file the bytes we just received
                progress.update(len(bytes_read))
        
        clientSocket.close()
        s.close()

        return s       

def testRun():
    myServer = Server()
    myServer.checkWorking()
    s = socket.socket()

    myServer.setFileInformation("testData.csv", "C:\\Users\\Capta\\Desktop\\Lil Gary\\Sockets Server\\Base Test\\C_S_Base")

    userInput = int(input("1: Client | 2: Server"))

    if (userInput == 1):
        #Client Fuction
        myServer.setServerType("Client")
        s = myServer.clientConnect(s)
        s = myServer.clientSend(s)
    elif (userInput == 2):
        #Server Function
        myServer.setServerType("Server")
        s = myServer.serverListenAndReceive(s)
    else:
        print("| Try Again")

    #Check Information is Set Properly
    myServer.getServerInformation()
    myServer.getServerStatus()
