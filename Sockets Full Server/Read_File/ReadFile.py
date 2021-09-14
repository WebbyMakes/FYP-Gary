import os
from tabulate import tabulate

class ConfigFile:
    def __init__(self, name):
        self.name = name
        self.absPath  = "C:\\Users\\Capta\\Desktop\\Big FYP File\\Sockets Full Server\\"
        self.fileName = "serverConfig.txt"

        self.deviceIP = None
        self.numRob = 0
        self.destinationIP = [None]
        self.port = 0

        #Use of 'T' for Transfer File
        self.TFileName = ""
        self.TfileLocation = ""
        self.TfullFileName = ""
        self.TfileSize = 0

    def readInConfigFile(self, debug):  #debug = 1 for output values
        f = open(self.absPath + "\\" + self.fileName, "r")
        myFile = f.readlines()
        f.close()

        lineNumber = 1

        self.deviceIP = myFile[lineNumber].split(": ")        #Get Device IP from file
        self.deviceIP = self.deviceIP[1].strip()
        lineNumber += 1

        self.numRob = int(myFile[lineNumber])                    #Number of Destinations, and their IPs
        lineNumber += 1

        self.destinationIP = [None] * self.numRob

        for i in range(int(self.numRob)):
            buffer = myFile[lineNumber].split(": ")           #Get Robot[i] destination IP
            buffer2 = buffer[1].strip()
            self.destinationIP[i] = buffer2
            lineNumber += 1

        self.port = myFile[lineNumber].split(": ")            #Get Port from file
        self.port = self.port[1].strip()
        lineNumber += 1
        lineNumber += 1 #Blank Line

        self.TfileName = myFile[lineNumber].split(": ")      #Get File Name from file
        self.TfileName = self.TfileName[1].strip()
        lineNumber += 1

        self.TfileLocation = myFile[lineNumber].split(": ")     #Get File Location of sending file (for transmission over sockets)
        self.TfileLocation = self.TfileLocation[1].strip()
        lineNumber += 1

        if (debug == 1):
            print("| Config File Read In Successfully")

        return self

    def outputVariable(self):
        table = []
        table.append(["Config File Contents", ""])
        table.append(["-- IP Information --", ""])
        table.append(["Device IP", self.deviceIP])
        table.append(["Number of Robots", str(self.numRob)])
        for i in range(self.numRob):
            string = "Robot " + str(i + 1) + " IP"
            table.append([string, str(self.destinationIP[i])])
        table.append(["Port:", str(self.port)])
        table.append(["-- Sockets File Information --", ""])
        table.append(["Transfer File Name:", str(self.TfileName)])
        table.append(["Transfer File Location", str(self.TfileLocation)])

        print(tabulate(table))
