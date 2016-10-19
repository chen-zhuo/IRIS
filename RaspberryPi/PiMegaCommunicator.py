'''
This file contains the definition of `PiMegaCommunicator` object class. This object handles the communication between
Raspberry Pi and Arduino Mega.

@author: joelle, reviewed by chen-zhuo
'''

from DataPacket import DataPacket
import hammingCode
import serial # @UnresolvedImport
import stringHelper

MSG_ACK = bytes([0b00000000])
MSG_NAK = bytes([0b00000001])
MSG_HELLO = bytes([0b00000010])
MSG_NAVI_START = bytes([0b00000011])
MSG_NAVI_END = bytes([0b00000100])
MSG_POLL_DATA = bytes([0b00000101])

class PiMegaCommunicator():
    def __init__(self):
        self.port = serial.Serial('/dev/ttyAMA0', baudrate=9600, timeout=3.0)
    
    '''
    Performs initial three-way handshake between Pi and Mega.
    '''
    def startUp(self):
        self.port.write(MSG_HELLO)
        print(stringHelper.MESSAGE + ' at PiMegaCommunicator.startUp(): Pi sent HELLO to Mega.')
        
        while True:
            msgReceived = self.port.read()
            if msgReceived == MSG_ACK:
                print(stringHelper.MESSAGE + ' Pi received ACK from Mega!')
                self.port.write(MSG_ACK)
                print(stringHelper.MESSAGE + ' Pi sent ACK to Mega. Three-way handshake is done.')
                break
    
    def pollData(self):
        self.port.write(MSG_POLL_DATA)
        print('MESSAGE: Pi sent POLL_DATA to Mega.')
        
        while True:
            bytestreamReceived = self.port.read()
            if bytestreamReceived != None:
                decodedBytestream = hammingCode.decode(bytestreamReceived)
                if decodedBytestream == None: # if the bytestream received is erroneous
                    self.port.write(MSG_NAK)
                else:
                    self.port.write(MSG_ACK)
                    dataPacket = DataPacket(decodedBytestream)
                    break
        
        return dataPacket

def testPollData():
    communicator = PiMegaCommunicator()
    communicator.startUp()
    
    totalNumStepsWalked = 0
    while True:
        dataPacket = communicator.pollData()
        print(dataPacket.packetId)
        print(dataPacket.gloveProximity)
        print(dataPacket.frontProximity)
        print(dataPacket.leftProximity)
        print(dataPacket.rightProximity)
        print(dataPacket.numSteps)
        print(dataPacket.orientation_tag)

if __name__ == '__main__':
    testPollData()
