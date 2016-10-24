import serial # @UnresolvedImport
from time import sleep

class MegaCommunicator():
    
    port = serial.Serial("/dev/ttyAMA0",baudrate=9600,timeout=3.0)
    
    def __init__(self):
        self.gloveSensor = 0
        self.frontSensor = 0
        self.leftSensor = 0
        self.rightSensor = 0
        self.distance_N = 0
        self.distance_NE = 0
        self.distance_E = 0
        self.distance_SE = 0
        self.distance_S = 0
        self.distance_SW = 0
        self.distance_W = 0
        self.distance_NW = 0
        self.orientation_tag = 0
        self.checkSum = 0
        self.theorySum = 0
        self.check_flag = 0
    
    def readlineCR(self):
        rv = ''
        while True:
            ch = self.port.read()
            rv += ch
            if ch == '\r' or ch == '':
                return rv

    #wait for mega to start up
    def startup(self):
        print ('Saying Hello')
        self.port.write(bytes('H', 'UTF-8'))
        print ('Arduino is reading..')
        
        while True:
            #ch = self.readlineCR()
            ch = self.port.read()
            print (ch.decode('utf-8'))
            if ch == b'A':
                print('Pi reads:')
                print(ch.decode('utf-8'))
                print('Sending ACK')
                self.port.write(bytes('A', 'UTF-8'))
                print ('Mega is ready')
                break
                    
    def pollData(self):
        while True:
            print ('Polling...')
            self.port.write(bytes('P', 'UTF-8'))
            self.gloveSensor = self.port.readline().decode('utf-8').replace('\r\n',"")
            self.frontSensor = self.port.readline().decode('utf-8').replace('\r\n',"")
            self.leftSensor = self.port.readline().decode('utf-8').replace('\r\n',"")
            self.rightSensor = self.port.readline().decode('utf-8').replace('\r\n',"")
            self.distance_N = self.port.readline().decode('utf-8').replace('\r\n',"")
            self.distance_NE = self.port.readline().decode('utf-8').replace('\r\n',"")
            self.distance_E = self.port.readline().decode('utf-8').replace('\r\n',"")
            self.distance_SE = self.port.readline().decode('utf-8').replace('\r\n',"")
            self.distance_S = self.port.readline().decode('utf-8').replace('\r\n',"")
            self.distance_SW = self.port.readline().decode('utf-8').replace('\r\n',"")
            self.distance_W = self.port.readline().decode('utf-8').replace('\r\n',"")
            self.distance_NW = self.port.readline().decode('utf-8').replace('\r\n',"")
            self.orientation_tag = self.port.readline().decode('utf-8').replace('\r\n',"")
            self.checkSum = int(self.port.readline().decode('utf-8').replace('\r\n',""))
            break

    def checkError(self):
        self.theorySum =int(self.gloveSensor) + int(self.frontSensor) + int(self.leftSensor) + int(self.rightSensor)+ int(self.orientation_tag) + int(self.distance_N) + int(self.distance_NE) +int(self.distance_E) + int(self.distance_SE) + int(self.distance_S) + int(self.distance_SW) + int(self.distance_W) + int(self.distance_NW)
        print ('theorySum:')
        print (self.theorySum)
        print ('checkSum:')
        print (self.checkSum)
        #self.theorySum = 999
        if (self.theorySum != self.checkSum):
            print ('CheckSum Error: please poll again')
            self.check_flag = 0
            #self.port.write(bytes('N', 'UTF-8'))
        else:
            print ('Data successfully polled')
            self.check_flag = 1
            #self.port.write(bytes('A', 'UTF-8'))
###TEST
test = MegaCommunicator()
test.startup()

test.pollData()
print (test.gloveSensor)
print (test.frontSensor)
print (test.leftSensor)
print (test.rightSensor)
print (test.distance_N)
print (test.distance_NE)
print (test.distance_SE)
print (test.distance_S)
print (test.distance_SW)
print (test.distance_W)
print (test.distance_NW)
print (test.orientation_tag)
#print (test.checkSum, end='')
test.checkError()

#while True:
for i in range (20):
    print (i)
    test.pollData()
    print (test.gloveSensor)
    print (test.frontSensor)
    print (test.leftSensor)
    print (test.rightSensor)
    print (test.distance_N)
    print (test.distance_NE)
    print (test.distance_SE)
    print (test.distance_S)
    print (test.distance_SW)
    print (test.distance_W)
    print (test.distance_NW)
    print (test.orientation_tag)
    #test.checkError()
    while (test.check_flag == 0):
        print (test.gloveSensor)
        print (test.frontSensor)
        print (test.leftSensor)
        print (test.rightSensor)
        print (test.distance_N)
        print (test.distance_NE)
        print (test.distance_SE)
        print (test.distance_S)
        print (test.distance_SW)
        print (test.distance_W)
        print (test.distance_NW)
        print (test.orientation_tag)
        test.checkError()
    sleep(0.5)
