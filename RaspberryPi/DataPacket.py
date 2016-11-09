'''
This file contains the definition of `DataPacket` object class. A `DataPacket` is instantiated from the transmitted
bytestream from Arduino Mega. The format of the bytestream should be

    <packetId>,<handProximity>,<leftLegFrontProximity>,<rightLegFrontProximity>,<leftLegLeftProximity>,
    <rightLegRightProximity>,<leftArmLeftProximity>,<rightArmRightProximity>,<initialHeading>,<numLeftTurns>,
    <numRightTurns>,<numStepsWalked>,<checksum>;

. Note that <initialHeading> is in degrees, with respect to geographical north. An example of a data packet is

    233,5,-1,-1,50,50,100,100,0,123,124,45,2333;

, which means that this packet has an ID of 233, the current hand proximity is 5cm, front proximities are out of sensor
range (i.e. no obstacles in front), left and right proximities measured from legs are 50cm, left and right proximities
measured from arms are 100cm, the user's current location is 50cm north-east from the starting location, the uers's
current heading is 45 degrees clockwise from north, and the user did not climb any stairs since the start of navigation.

@author: chen-zhuo
'''

import stringHelper

class DataPacket:
    '''
    Parses `bytestream` representing one data packet and updates the fields.
    '''
    def __init__(self, bytestream):
        self.packetId = ''
        self.handProximity = ''
#         self.leftLegFrontProximity = ''
#         self.rightLegFrontProximity = ''
#         self.leftLegLeftProximity = ''
#         self.rightLegRightProximity = ''
        self.leftArmLeftProximity = ''
        self.rightArmRightProximity = ''
        self.initialHeading = ''
        self.numLeftTurns = ''
        self.numRightTurns = ''
        self.numStepsWalked = ''
        self.checksum = ''
        
        i = 0 # for traversing through `bytestream`
        print(bytestream)
        # to parse `packetId`
        while chr(bytestream[i]) != ',':
            self.packetId += chr(bytestream[i])
            i = i + 1
        self.packetId = int(self.packetId)
        
        # to parse `handProximity`
        i = i + 1
        while chr(bytestream[i]) != ',':
            self.handProximity += chr(bytestream[i])
            i = i + 1
        self.handProximity = int(self.handProximity)
        
        # to parse `leftLegFrontProximity`
#         i = i + 1
#         while chr(bytestream[i]) != ',':
#             self.leftLegFrontProximity += chr(bytestream[i])
#             i = i + 1
#         self.leftLegFrontProximity = int(self.leftLegFrontProximity)
        
        # to parse `rightLegFrontProximity`
#         i = i + 1
#         while chr(bytestream[i]) != ',':
#             self.rightLegFrontProximity += chr(bytestream[i])
#             i = i + 1
#         self.rightLegFrontProximity = int(self.rightLegFrontProximity)
        
        # to parse `leftLegLeftProximity`
#         i = i + 1
#         while chr(bytestream[i]) != ',':
#             self.leftLegLeftProximity += chr(bytestream[i])
#             i = i + 1
#         self.leftLegLeftProximity = int(self.leftLegLeftProximity)
        
        # to parse `rightLegRightProximity`
#         i = i + 1
#         while chr(bytestream[i]) != ',':
#             self.rightLegRightProximity += chr(bytestream[i])
#             i = i + 1
#         self.rightLegRightProximity = int(self.rightLegRightProximity)
        
        # to parse `leftArmLeftProximity`
        i = i + 1
        while chr(bytestream[i]) != ',':
            self.leftArmLeftProximity += chr(bytestream[i])
            i = i + 1
        self.leftArmLeftProximity = int(self.leftArmLeftProximity)
        
        # to parse `rightArmRightProximity`
        i = i + 1
        while chr(bytestream[i]) != ',':
            self.rightArmRightProximity += chr(bytestream[i])
            i = i + 1
        self.rightArmRightProximity = int(self.rightArmRightProximity)
        
        # to parse `distancesList`
#         i = i + 2
#         while chr(bytestream[i]) != ',':
#             self.distancesList[0] += chr(bytestream[i])
#             i = i + 1
#         self.distancesList[0] = int(self.distancesList[0])
#         for j in range(1, 7):
#             i = i + 1
#             while chr(bytestream[i]) != ',':
#                 self.distancesList[j] += chr(bytestream[i])
#                 i = i + 1
#             self.distancesList[j] = int(self.distancesList[j])
#         i = i + 1
#         while chr(bytestream[i]) != ']':
#             self.distancesList[7] += chr(bytestream[i])
#             i = i + 1
#         self.distancesList[7] = int(self.distancesList[7])
        
        # to parse `initialHeading`
        i = i + 1
        while chr(bytestream[i]) != ',':
            self.initialHeading += chr(bytestream[i])
            i = i + 1
        self.initialHeading = int(self.initialHeading)
        
        # to parse `numLeftTurns`
        i = i + 1
        while chr(bytestream[i]) != ',':
            self.numLeftTurns += chr(bytestream[i])
            i = i + 1
        self.numLeftTurns = int(self.numLeftTurns)
        
        # to parse `numRightTurns`
        i = i + 1
        while chr(bytestream[i]) != ',':
            self.numRightTurns += chr(bytestream[i])
            i = i + 1
        self.numRightTurns = int(self.numRightTurns)
        
        # to parse `numStepsWalked`
        i = i + 1
        while chr(bytestream[i]) != ',':
            self.numStepsWalked += chr(bytestream[i])
            i = i + 1
        self.numStepsWalked = int(self.numStepsWalked)
        
        # to parse `checksum`
        i = i + 1
        while chr(bytestream[i]) != ';':
            self.checksum += chr(bytestream[i])
            i = i + 1
        self.checksum = int(self.checksum)
    
    def __str__(self, indent=0):
        result = ''
        result += '#' + str(self.packetId) + ' -- '
        result += str(self.handProximity) + ','
#         result += str(self.leftLegFrontProximity) + ','
#         result += str(self.rightLegFrontProximity) + ','
#         result += str(self.leftLegLeftProximity) + ','
#         result += str(self.rightLegRightProximity) + ','
        result += str(self.leftArmLeftProximity) + ','
        result += str(self.rightArmRightProximity) + ','
        result += str(self.initialHeading) + ','
        result += str(self.numLeftTurns) + ','
        result += str(self.numRightTurns) + ','
        result += str(self.numStepsWalked) + ','
        
        result += str(self.checksum) + ';'
        return result

def test():
    bytestream = '233,5,100,100,0,123,124,45,2333;'.encode('utf_8')
    dataPacket = DataPacket(bytestream)
    
    print(stringHelper.INFO + ' Input Bytestream:\n    ' + str(bytestream))
    print(stringHelper.INFO + ' String Representation:\n    ' + str(dataPacket))
    print(stringHelper.INFO + ' Parsed Data:')
    print('    packetId = #' + str(dataPacket.packetId))
    print('    handProximity = ' + str(dataPacket.handProximity) + ' cm')
#     print('    leftLegFrontProximity = ' + str(dataPacket.leftLegFrontProximity) + ' cm')
#     print('    rightLegFrontProximity = ' + str(dataPacket.rightLegFrontProximity) + ' cm')
#     print('    leftLegLeftProximity = ' + str(dataPacket.leftLegLeftProximity) + ' cm')
#     print('    rightLegRightProximity = ' + str(dataPacket.rightLegRightProximity) + ' cm')
    print('    leftArmLeftProximity = ' + str(dataPacket.leftArmLeftProximity) + ' cm')
    print('    rightArmRightProximity = ' + str(dataPacket.rightArmRightProximity) + ' cm')
    print('    initialHeading = ' + str(dataPacket.initialHeading) + ' degrees')
    print('    numLeftTurns = ' + str(dataPacket.numLeftTurns))
    print('    numRightTurns = ' + str(dataPacket.numRightTurns))
    print('    numStepsWalked = ' + str(dataPacket.numStepsWalked))
    print('    checksum = ' + str(dataPacket.checksum))

if __name__ == '__main__':
    test()
