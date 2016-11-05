'''
Created on 19 Oct 2016

@author: chen-zhuo
'''

from DataPacket import DataPacket
import stringHelper
from time import sleep

dataPackets = [DataPacket('0,0,0,0,[0,0,0,0,0,0,0,0],45;'.encode('utf-8')),
               # at #1211, facing "right"
               DataPacket('1,0,0,0,[0,0,0,0,0,0,0,0],135;'.encode('utf-8')),
               # between #1211 and #1214, facing "right" + 45 degrees (audio "adjust left 45 degrees")
               DataPacket('2,0,0,0,[0,0,0,700,0,0,0,0],180;'.encode('utf-8')),
               # between #1211 and #1214, facing "right"
               DataPacket('3,0,0,0,[0,0,0,800,0,0,0,0],135;'.encode('utf-8')),
               # near #1214, facing "right" (audio "turn right")
               DataPacket('4,0,0,0,[0,0,0,1400,0,0,0,0],135;'.encode('utf-8')),
               # at #1214, facing "down"
               DataPacket('5,0,0,0,[0,0,0,1462,0,0,0,0],225;'.encode('utf-8')),
               # at #1237, facing "down"
               DataPacket('6,0,0,0,[0,0,0,1462,0,244,0,0],225;'.encode('utf-8')),
               # between #1237 and #1216, facing "down", slightly deviated from graph edge
               DataPacket('7,0,0,0,[0,0,0,1662,0,644,0,0],225;'.encode('utf-8')),
               # at #1216; destination reached
               DataPacket('8,0,0,0,[0,0,0,1462,0,1056,0,0],225;'.encode('utf-8'))
              ]

class PiMegaCommunicator():
    def __init__(self):
        pass
    
    def startUp(self):
        # Pi sends `MSG_HELLO` to Mega.
        print(stringHelper.MESSAGE + ' at PiMegaCommunicator.startUp(): Pi sent HELLO to Mega.')
        sleep(0.5)
    
    def pollData(self):
        global dataPackets
        
        # to get the next data packet in the list of pre-defined `dataPackets`
        dataPacket = dataPackets[0]
        dataPackets.pop(0)
        return dataPacket

def _test():
    piMegaCommunicator = PiMegaCommunicator()
    piMegaCommunicator.startUp()
    
    print('The first data packet is:')
    print('    ' + str(piMegaCommunicator.pollData()))

if __name__ == '__main__':
    _test()
