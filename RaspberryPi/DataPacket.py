'''
This file contains the definition of `DataPacket` object class. A `DataPacket` is instantiated from the transmitted
bytestream from Arduino Mega. The format of the bytestream should be

    <packetId>,<handProximity>,<leftLegFrontProximity>,<rightLegFrontProximity>,<leftLegLeftProximity>,
    <rightLegRightProximity>,<leftArmLeftProximity>,<rightArmRightProximity>,<distancesList>,<heading>;

. In particular, <distancesList> indicates the user's displacement from the starting location to the current location
in the format of

    [<distanceWalked_north>,<distanceWalked_northeast>,<distanceWalked_east>,<distanceWalked_southeast>,
    <distanceWalked_south>,<distanceWalked_southwest>,<distanceWalked_west>,<distanceWalked_northwest>]

. Note that <heading> is in degrees, with respect to geographical north. An example of a data packet is

    233,5,-1,-1,50,50,100,100,[0,50,0,0,0,0,0,0],45,0;

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
        self.distancesList = ['', '', '', '', '', '', '', '']
        self.heading = ''
        self.checksum = ''
        
        i = 0 # for traversing through `bytestream`
        
        print(bytestream[i])
        # to parse `packetId`
        while bytestream[i] != ',':
            self.packetId += bytestream[i]
            i = i + 1
        self.packetId = int(self.packetId)
        
        # to parse `handProximity`
        i = i + 1
        while bytestream[i] != ',':
            self.handProximity += bytestream[i]
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
        while bytestream[i] != ',':
            self.leftArmLeftProximity += bytestream[i]
            i = i + 1
        self.leftArmLeftProximity = int(self.leftArmLeftProximity)
        
        # to parse `rightArmRightProximity`
        i = i + 1
        while bytestream[i] != ',':
            self.rightArmRightProximity += bytestream[i]
            i = i + 1
        self.rightArmRightProximity = int(self.rightArmRightProximity)
        
        # to parse `distancesList`
        i = i + 2
        while bytestream[i] != ',':
            self.distancesList[0] += bytestream[i]
            i = i + 1
        self.distancesList[0] = int(self.distancesList[0])
        for j in range(1, 7):
            i = i + 1
            while bytestream[i] != ',':
                self.distancesList[j] += bytestream[i]
                i = i + 1
            self.distancesList[j] = int(self.distancesList[j])
        i = i + 1
        while bytestream[i] != ']':
            self.distancesList[7] += bytestream[i]
            i = i + 1
        self.distancesList[7] = int(self.distancesList[7])
        
        # to parse `heading`
        i = i + 2
        while bytestream[i] != ',':
            self.heading += bytestream[i]
            i = i + 1
        self.heading = int(self.heading)
        
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
        result += str(self.distancesList).replace(' ', '') + ','
        result += str(self.heading) + ','
        result += str(self.checksum) + ';'
        return result

def test():
    bytestream = '233,5,100,100,[0,50,0,0,0,0,0,0],45,233;'
    dataPacket = DataPacket(bytestream.encode('utf-8'))
    
    print(stringHelper.INFO + ' Input Bytestream:\n    ' + bytestream)
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
    print('    distancesList = ' + str(dataPacket.distancesList) + ' cm')
    print('    heading = ' + str(dataPacket.heading) + ' degrees from north')
    print('    checksum = ' + str(dataPacket.checksum))

if __name__ == '__main__':
    test()
