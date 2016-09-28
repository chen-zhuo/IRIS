'''
This file contains the definition of 'DataPacket' object class. 'DataPacket' objects are instantiated by a
'PiMegaCommunicator' object. It contains processed sensor data for navigation algorithms.

@author: chen-zhuo
'''

'''
@todo
'''
class DataPacket:
    def __init__(self, packetId, frontProximity, leftProximity, rightProximity, handProximity, numStairsClimbed,
                 numHorizontalStepsWalked, bearingsOfEachHorizontalStep):
        self.packetId = packetId
        self.frontProximity = frontProximity
        self.leftProximity = leftProximity
        self.rightProximity = rightProximity
        self.handProximity = handProximity
        self.numStairsClimbed = numStairsClimbed
        self.numHorizontalStepsWalked = numHorizontalStepsWalked
        self.bearingsOfEachHorizontalStep = bearingsOfEachHorizontalStep
    

def test():
    test = DataPacket()
    print(test.packetId)

if __name__ == '__main__':
    test()
