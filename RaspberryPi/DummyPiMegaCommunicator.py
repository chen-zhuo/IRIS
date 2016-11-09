'''
Created on 19 Oct 2016

@author: chen-zhuo
'''

from DataPacket import DataPacket
import stringHelper
from time import sleep

dataPackets = [DataPacket('0,0,0,0,45,0,0,0,45;'.encode('utf-8')),
               # at #1211, facing "up" (feedback: turn right 90 degrees)
               
               DataPacket('1,0,0,0,45,0,2,0,48;'.encode('utf-8')),
               # at #1211, facing "right" (feedback: go straight)
               
               DataPacket('2,0,0,0,45,0,2,0,2333;'.encode('utf-8')),
               # erronous data packet; drop this (feedback: go straight)
               
               DataPacket('3,0,0,0,45,0,2,5,58;'.encode('utf-8')),
               # between #1211 and #1214, facing "right" (feedback: go straight)
               
               DataPacket('4,0,0,0,45,0,2,24,75;'.encode('utf-8')),
               # near #1214, facing "right" (feedback: turn right 90 degrees)
               
               DataPacket('5,0,0,0,45,0,4,24,78;'.encode('utf-8')),
               # at #1214, facing "down" (feedback: go straight)
               
               DataPacket('6,0,0,0,45,0,4,28,83;'.encode('utf-8')),
               # at #1237, facing "down" (feedback: go straight)
               
               DataPacket('7,0,0,0,45,0,4,41,182;'.encode('utf-8')),
               # at #1216; destination reached
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
