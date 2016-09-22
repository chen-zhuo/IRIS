'''
This file contains the definition of 'PiMegaCommunicator' object class. This object handles the communication between
Raspberry Pi and Arduino Mega.
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

    
    def startup(self):       
        print('Saying hello')
        port.write('H')
        print('Sent H')
        print('Arduino is reading')

        while True:
            ch=port.read()
            if(ch=='A'):
                print('read')
                print(ch)
                print('Sending ACK')
                port.write('A')
                print('Mega is ready')
                break
    
    def __init__(self):
        port = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=3.0)

        return    
          
    
    def piSendsMsgToMega(self, msg):
        port.write(msg)

    
    def piGetsDataPacket(self):
        # TODO
        self.device1 = 127
        
        return
    
    
   
# TEST        
packet = PiMegaCommunicator()
packet.startup()

