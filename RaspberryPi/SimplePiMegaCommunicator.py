'''
This is a simple version of `PiMegaCommunicator`. Hamming(8,4) encoding is not used. Any erroneous data packet is simply
dropped without requesting for re-transmission.

@author joelle, reviewed by chen-zhuo
'''

import serial # @UnresolvedImport
import stringHelper
from time import sleep

class PiMegaCommunicator():
    def __init__(self):
        self.port = serial.Serial('/dev/ttyAMA0',baudrate=9600,timeout=3.0)
        
        self.handProximity = 0
        self.frontProximity = 0
        self.leftProximity = 0
        self.rightProximity = 0
        self.distanceWalked_north = 0
        self.distanceWalked_northeast = 0
        self.distanceWalked_east = 0
        self.distanceWalked_southeast = 0
        self.distanceWalked_south = 0
        self.distanceWalked_southwest = 0
        self.distanceWalked_west = 0
        self.distanceWalked_northwest = 0
        self.heading = 0
        
        self.checksum = 0 # sum of all values above (from `handProximity` to `heading`)
    
    # three-way handshake
    def startUp(self):
        self.port.write(bytes('H', 'utf-8')) # send HELLO
        print(stringHelper.MESSAGE + ' at PiMegaCommunicator.startUp(): Pi sent HELLO to Mega.')
        
#         msgReceived = ''
#         while msgReceived == '':
#             print(stringHelper.MESSAGE + ' Reading...')
#             msgReceived = self.port.read().decode('utf-8')
#         if msgReceived == 'A': # if ACK is received
#             print(stringHelper.MESSAGE + ' at PiMegaCommunicator.startUp(): Pi received ACK from Mega.')
#             self.port.write(bytes('A', 'utf-8')) # send ACK
#             print(stringHelper.MESSAGE + ' at PiMegaCommunicator.startUp(): Pi sent ACK to Mega. Three-way handshake is done.')
#         else: # if ACK is not received
#             print(stringHelper.ERROR + ' at PiMegaCommunicator.startUp(): Pi did not receive ACK from Mega.')
        
        
        
        
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
        self.port.write(bytes('P', 'utf-8')) # send POLL
        # @author chen-zhuo: possible logic error here; data might not be ready yet right after sending POLL 
        self.handProximity = int(self.port.readline().decode('utf-8').replace('\r\n',''))
        self.frontProximity = int(self.port.readline().decode('utf-8').replace('\r\n',''))
        self.leftProximity = int(self.port.readline().decode('utf-8').replace('\r\n',''))
        self.rightProximity = int(self.port.readline().decode('utf-8').replace('\r\n',''))
        self.distanceWalked_north = int(self.port.readline().decode('utf-8').replace('\r\n',''))
        self.distanceWalked_northeast = int(self.port.readline().decode('utf-8').replace('\r\n',''))
        self.distanceWalked_east = int(self.port.readline().decode('utf-8').replace('\r\n',''))
        self.distanceWalked_southeast = int(self.port.readline().decode('utf-8').replace('\r\n',''))
        self.distanceWalked_south = int(self.port.readline().decode('utf-8').replace('\r\n',''))
        self.distanceWalked_southwest = int(self.port.readline().decode('utf-8').replace('\r\n',''))
        self.distanceWalked_west = int(self.port.readline().decode('utf-8').replace('\r\n',''))
        self.distanceWalked_northwest = int(self.port.readline().decode('utf-8').replace('\r\n',''))
        self.heading = int(self.port.readline().decode('utf-8').replace('\r\n',''))
        self.checksum = int(self.port.readline().decode('utf-8').replace('\r\n',''))
        
        print(stringHelper.INFO + ' ' + str(self.handProximity) + ', ' + str(self.frontProximity) + ', ' +
              str(self.leftProximity) + ', ' + str(self.rightProximity) + ', [' + str(self.distanceWalked_north) +
              ', ' + str(self.distanceWalked_northeast) + ', ' + str(self.distanceWalked_east) + ', ' +
              str(self.distanceWalked_southeast) + ', ' + str(self.distanceWalked_south) + ', ' +
              str(self.distanceWalked_southwest) + ', ' + str(self.distanceWalked_west) + ', ' +
              str(self.distanceWalked_northwest) + '], ' + str(self.heading))
        
        expectedChecksum = self.handProximity + self.frontProximity + self.leftProximity + self.rightProximity +\
                self.distanceWalked_north + self.distanceWalked_northeast + self.distanceWalked_east +\
                self.distanceWalked_southeast + self.distanceWalked_south + self.distanceWalked_southwest +\
                self.distanceWalked_west + self.distanceWalked_northwest + self.heading
        if self.checkum != expectedChecksum:
            print(stringHelper.WARNING + ' at PiMegaCommunicator.pollData(): Checksum does not match. Dropping this' +
                  'erroneous data packet.')
            self.handProximity = 0
            self.frontProximity = 0
            self.leftProximity = 0
            self.rightProximity = 0
            self.distanceWalked_north = 0
            self.distanceWalked_northeast = 0
            self.distanceWalked_east = 0
            self.distanceWalked_southeast = 0
            self.distanceWalked_south = 0
            self.distanceWalked_southwest = 0
            self.distanceWalked_west = 0
            self.distanceWalked_northwest = 0
            self.heading = 0
            self.checksum = 0

def _test():
    piMegaCommunicator = PiMegaCommunicator()
    piMegaCommunicator.startUp()
    
    while True:
        piMegaCommunicator.pollData()
        sleep(0.5)

if __name__ == '__main__':
    _test()
