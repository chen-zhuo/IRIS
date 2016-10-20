'''
Created on 19 Oct 2016

@author: chen-zhuo
'''

from DataPacket import DataPacket
import stringHelper
from time import sleep

dataPackets = [# at #1211, facing "right"
               DataPacket('0,0,0,0,0,[0,0,0,0,0,0,0,0],135,0;'.encode('utf-8')),
               # between #1211 and #1214, facing "right" + 45 degrees (need to adjust heading back to "right")
               DataPacket('1,0,0,0,0,[0,0,0,700,0,0,0,0],180,0;'.encode('utf-8')),
               # between #1211 and #1214, facing "right"
               DataPacket('2,0,0,0,0,[0,0,0,800,0,0,0,0],135,0;'.encode('utf-8')),
               # near #1214, facing "right"
               DataPacket('2,0,0,0,0,[0,0,0,1400,0,0,0,0],135,0;'.encode('utf-8')),
               # at #1214, facing "down"
               DataPacket('2,0,0,0,0,[0,0,0,1462,0,0,0,0],225,0;'.encode('utf-8')),
               # at #1237, facing "down"
               DataPacket('3,0,0,0,0,[0,0,0,1462,0,244,0,0],135,0;'.encode('utf-8')),
               # between #1237 and #1216, facing "down", slightly deviated from graph edge
               DataPacket('3,0,0,0,0,[0,0,0,1662,0,644,0,0],135,0;'.encode('utf-8')),
               # at #1216; destination reached
               DataPacket('3,0,0,0,0,[0,0,0,1462,0,1056,0,0],135,0;'.encode('utf-8'))
              ]

class PiMegaCommunicator():
    def __init__(self):
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
    
    def startUp(self):
        # Pi sends `MSG_HELLO` to Mega.
        print(stringHelper.MESSAGE + ' at PiMegaCommunicator.startUp(): Pi sent HELLO to Mega.')
        sleep(0.3)
        
        # Pi waits for response from Mega.
        # If Pi receives ACK from Mega, then send ACK back to Mega.
        # Three-way handshake is now finished.
        print(stringHelper.MESSAGE + ' at PiMegaCommunicator.startUp(): Pi received ACK from Mega.')
        print(stringHelper.MESSAGE + ' at PiMegaCommunicator.startUp(): Pi sent ACK to Mega. Three-way handshake is done.')
    
    def pollData(self):
        global dataPackets
        
        # to get the next data packet in the list of pre-defined `dataPackets`
        dataPacket = dataPackets[0]
        dataPackets.pop(0)
        
        # to update the data fields
        self.handProximity = int(dataPacket.handProximity)
        self.frontProximity = int(dataPacket.frontProximity)
        self.leftProximity = int(dataPacket.leftProximity)
        self.rightProximity = int(dataPacket.rightProximity)
        self.distanceWalked_north = int(dataPacket.distancesList[0])
        self.distanceWalked_northeast = int(dataPacket.distancesList[1])
        self.distanceWalked_east = int(dataPacket.distancesList[2])
        self.distanceWalked_southeast = int(dataPacket.distancesList[3])
        self.distanceWalked_south = int(dataPacket.distancesList[4])
        self.distanceWalked_southwest = int(dataPacket.distancesList[5])
        self.distanceWalked_west = int(dataPacket.distancesList[6])
        self.distanceWalked_northwest = int(dataPacket.distancesList[7])
        self.heading = int(dataPacket.heading)
        
        return dataPacket

def _test():
    piMegaCommunicator = PiMegaCommunicator()
    piMegaCommunicator.startUp()
    
    print('The first data packet is:')
    print('   ' + str(piMegaCommunicator.pollData()))

if __name__ == '__main__':
    _test()
