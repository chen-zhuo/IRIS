'''
This file contains the definition of 'PiMegaCommunicator' object class. This object handles the communication between
Raspberry Pi and Arduino Mega.

@author: joelle
'''

#MSG_ACK = 0b0000;
#MSG_NAK = 0b0001;
#MSG_HELLO = 0b0010;
#MSG_START_NAVI = 0b0011
#MSG_END_NAVI = 0b0100
#MSG_POLL_DATA = 0b0101;

import serial

class PiMegaCommunicator:
    
    device1 = 0
    port = None
    
    def __init__(self):
        self.port = serial.Serial("/dev/ttyAMA0", baudrate = 9600, timeout = 3.0)
    
    def startup(self):
        print('Saying hello')
        self.port.write('H')
        print('Sent H')
        print('Arduino is reading')
    
        while True:
            ch = self.port.read()
            if (ch == 'A'):
                print('read')
                print(ch)
                print('Sending ACK')
                self.port.write('A')
                print('Mega is ready')
                break
    
    def piSendsMsgToMega(self, msg):
        self.port.write(msg)
    
    def piGetsDataPacket(self):
        self.device1 = 127
    

def test():
    packet = PiMegaCommunicator()
    packet.startup()

if __name__ == '__main__':
    test()
