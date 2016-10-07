'''
This file contains the definition of 'DataPacket' object class. 'DataPacket' objects are instantiated by a
'PiMegaCommunicator' object. It contains processed sensor data for navigation algorithms.

id; handProximity; frontProximity; leftProximity; rightProximity; distance; direction; heading; numStairsClimbed;

'0;50;inf;50;50;100;182;0;'

@author: chen-zhuo
'''

'''
@todo
'''
class DataPacket:
    def __init__(self, bytestream):
        
        self.packetId = bytestream[0]
        self.frontProximity = bytestream[0]
        self.leftProximity = bytestream[0]
        self.rightProximity = bytestream[0]
        self.handProximity = bytestream[0]
        self.numStairsClimbed = bytestream[0]
        self.numHorizontalStepsWalked = bytestream[0]
        self.bearingsOfEachHorizontalStep = bytestream[0]
    

def test():
    test = DataPacket()
    print(test.packetId)

if __name__ == '__main__':
    test()
