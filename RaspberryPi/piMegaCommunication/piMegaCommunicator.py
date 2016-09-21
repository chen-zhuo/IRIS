'''
This file contains the definition of 'PiMegaCommunicator' object class. This object handles the communication between
Raspberry Pi and Arduino Mega.
'''

MSG_ACK = 0b0000;
MSG_NAK = 0b0001;
MSG_HELLO = 0b0010;
MSG_START_NAVI = 0b0011
MSG_END_NAVI = 0b0100
MSG_POLL_DATA = 0b0101;

class PiMegaCommunicator:
    
    def __init__(self):
        return
    
    def piSendsMsgToMega(self, msg):
        # TODO
        return
    
    def piGetsDataPacket(self):
        # TODO
        
        
        
        return
    
