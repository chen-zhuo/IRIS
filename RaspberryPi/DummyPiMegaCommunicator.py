'''
Created on 19 Oct 2016

@author: chen-zhuo
'''

from DataPacket import DataPacket
import stringHelper
from time import sleep

dataPackets = [DataPacket('0,233,233,100,100,[1000,135],135,0;'.encode('utf_8')), # between 1211 and 1214
               DataPacket('1,233,233,100,100,[1002,135],135,0;'.encode('utf_8')), # at 1214
               DataPacket('2,233,233,100,100,[244,225],225,0;'.encode('utf_8')), # at 1237
               DataPacket('3,233,233,100,100,[812,225],135,0;'.encode('utf_8')), # at 1216
              ]

class PiMegaCommunicator():
    def __init__(self):
        # initialize serial
        pass
    
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
        
        # to process the data packet
        processedDataDict = {}
        processedDataDict['packetId'] = int(dataPacket.packetId)
        processedDataDict['handProximity'] = int(dataPacket.handProximity)
        processedDataDict['frontProximity'] = int(dataPacket.frontProximity)
        processedDataDict['leftProximity'] = int(dataPacket.leftProximity)
        processedDataDict['rightProximity'] = int(dataPacket.rightProximity)
        processedDataDict['distance'] = int(dataPacket.displacement[0])
        processedDataDict['direction'] = int(dataPacket.displacement[1])
        processedDataDict['heading'] = int(dataPacket.heading)
        processedDataDict['numStairsClimbed'] = int(dataPacket.numStairsClimbed)
        
        return processedDataDict

def _test():
    piMegaCommunicator = PiMegaCommunicator()
    piMegaCommunicator.startUp()
    
    print('The first data packet is:')
    print('   ' + str(piMegaCommunicator.pollData()))

if __name__ == '__main__':
    _test()
