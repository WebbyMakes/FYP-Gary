import os
from os import system
from Read_File import ReadFile
from C_S_Base import CSBase

#Socket Libraries
import socket
import tqdm
import os

system('cls')

debugVar = 1    #Set = 1 for printing debug information

#Config File Definition
myConfigFile = ReadFile.ConfigFile("Gary")
myConfigFile = myConfigFile.readInConfigFile(debugVar)     #1 for Debug
#myConfigFile.outputVariable()

#Server Setup
myServer = CSBase.Server()
myServer.checkWorking(debugVar)
s = socket.socket()

myServer.setFileInformation(myConfigFile.TFileName, myConfigFile.TfileLocation, debugVar)

userInput = int(input("| 1: Client | 2: Server | -> "))

if (userInput == 1):
    #Client Function
    myServer.deviceIPSet(myConfigFile.deviceIP, debugVar)
    myServer.portSet(int(myConfigFile.port), debugVar)
    myServer.setServerType("Client", debugVar)

    for i in range(myConfigFile.numRob):
        myServer.serverIPSendSet(myConfigFile.destinationIP[i], debugVar)
        s = myServer.clientConnect(s, debugVar)
        s = myServer.clientSend(s)
elif (userInput == 2):
    #Server Function
    myServer.deviceIPSet(myConfigFile.deviceIP, debugVar)
    myServer.setServerType("Server", debugVar)
    s = myServer.serverListenAndReceive(s)
else:
    print("| Try Again")

print("End of Program")