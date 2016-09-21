'''
This file contains the definition of 'DataPacket' object class. 'DataPacket' objects are instantiated by a
'PiMegaCommunicator' object. It contains processed sensor data for navigation algorithms.
'''

class DataPacket:
    
    packetId = -1
    frontProximity = -1
    leftProximity = -1
    rightProximity = -1
    handProximity = -1
    numStairsClimbed = -1
    numHorizontalStepsWalked = -1
    bearingsOfEachHorizontalStep = -1
    
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
        
