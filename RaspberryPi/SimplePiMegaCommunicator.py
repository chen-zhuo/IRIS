'''
This is a simple version of `PiMegaCommunicator`. Hamming(8,4) encoding is not used. Any erroneous data packet is simply
dropped without requesting for re-transmission.

@author joelle, reviewed by chen-zhuo
'''

from DataPacket import DataPacket
import serial # @UnresolvedImport
import stringHelper
from time import sleep

class PiMegaCommunicator():
    def __init__(self):
        self.port = serial.Serial('/dev/ttyAMA0', baudrate=9600, timeout=3.0)
    
    def startUp(self):
        print('in startUp()')
        self.port.write(bytes('H', 'utf-8'))
        print(stringHelper.MESSAGE + ' at PiMegaCommunicator.startUp(): Pi sent HELLO to Mega.')
    
    '''
    Requests for data by sending a 'P' character to Mega. Assumes data comes one by one, separated by a newline
    character. Using a simple sum as the checksum.
    
    @return a `DataPacket` object if the checksum is correct; return None if the checksum is incorrect
    '''
    def pollData(self):
        self.port.write(bytes('P', 'utf-8')) # send POLL
        
        # ============================== BEGIN DATA ==============================
        
        packetId = int(self.waitAndReadLine())
        handProximity = int(self.waitAndReadLine())
#         leftLegFrontProximity = int(self.waitAndReadLine())
#         rightLegFrontProximity = int(self.waitAndReadLine())
#         leftLegLeftProximity = int(self.waitAndReadLine())
#         rightLegRightProximity = int(self.waitAndReadLine())
        leftArmLeftProximity = int(self.waitAndReadLine())
        rightArmRightProximity = int(self.waitAndReadLine())
        
        distanceWalked_north = int(self.waitAndReadLine())
        distanceWalked_northeast = int(self.waitAndReadLine())
        distanceWalked_east = int(self.waitAndReadLine())
        distanceWalked_southeast = int(self.waitAndReadLine())
        distanceWalked_south = int(self.waitAndReadLine())
        distanceWalked_southwest = int(self.waitAndReadLine())
        distanceWalked_west = int(self.waitAndReadLine())
        distanceWalked_northwest = int(self.waitAndReadLine())
        
        heading = int(self.waitAndReadLine())
        orientationTag = int(self.waitAndReadLine())
        
        checksum = int(self.waitAndReadLine())
        
        # ============================== END DATA ==============================
        
        # to verify checksum
        expectedChecksum = packetId +\
                           handProximity +\
                           leftArmLeftProximity +\
                           rightArmRightProximity +\
                           distanceWalked_north +\
                           distanceWalked_northeast +\
                           distanceWalked_east +\
                           distanceWalked_southeast +\
                           distanceWalked_south +\
                           distanceWalked_southwest +\
                           distanceWalked_west +\
                           distanceWalked_northwest +\
                           heading +\
                           orientationTag
        if checksum != expectedChecksum:
            print(stringHelper.WARNING + ' at PiMegaCommunicator.pollData(): Checksum does not match. Dropping this \
                  erroneous data packet.')
            return None
        else:
            # to compile the data received into a single `DataPacket` object
            bytestream = str(packetId) + ',' +\
                         str(handProximity) + ',' +\
                         str(leftArmLeftProximity) + ',' +\
                         str(rightArmRightProximity) + ',[' +\
                         str(distanceWalked_north) + ',' +\
                         str(distanceWalked_northeast) + ',' +\
                         str(distanceWalked_east) + ',' +\
                         str(distanceWalked_southeast) + ',' +\
                         str(distanceWalked_south) + ',' +\
                         str(distanceWalked_southwest) + ',' +\
                         str(distanceWalked_west) + ',' +\
                         str(distanceWalked_northwest) + '],' +\
                         str(heading) + ',' +\
                         str(orientationTag) + ',' +\
                         str(checksum) + ';'
            print(bytestream)
            dataPacket = DataPacket(bytestream)
            return dataPacket
    
    def waitAndReadLine(self):
        msgReceived = ''
        while msgReceived == '':
            print('Receives nothing!')
            msgReceived = self.port.readline().decode('utf-8').replace('\r\n','')
        return msgReceived

def _test():
    piMegaCommunicator = PiMegaCommunicator()
    piMegaCommunicator.startUp()
    
    while True:
        piMegaCommunicator.pollData()
        sleep(0.5)

if __name__ == '__main__':
    _test()
