'''
This file contains the definition of `DataPacket` object class. A `DataPacket` is instantiated from the transmitted
bytestream from Arduino Mega. The format of the bytestream should be

    <numPackets>,[<packetId>,<handProximity>,<frontProximity>,<leftProximity>,<rightProximity>,<distancesList>,
    <heading>,<numStairsClimbed>],[ ... ], ... ,[ ... ];
                                  ^~~~~~~       ^~~~~~~
                                  2nd packet    last packet

. Note that <numPackets> should always be 1, unless packet loss occured. The lost packet will be appended behind the
next packet, and be transmitted during the next data poll. Hence, the format of the bytestream representing one data
packet is

    <packetId>,<handProximity>,<frontProximity>,<leftProximity>,<rightProximity>,<distancesList>,<heading>,
    <numStairsClimbed>;

. In particular, <distancesList> indicates the user's displacement from the starting location to the current location
in the format of

    [<distanceWalked_north>,<distanceWalked_northeast>,<distanceWalked_east>,<distanceWalked_southeast>,
    <distanceWalked_south>,<distanceWalked_southwest>,<distanceWalked_west>,<distanceWalked_northwest>]

. Note that <heading> is in degrees, with respect to geographical north. An example of a data packet is

    233,5,-1,100,100,[0,50,0,0,0,0,0,0],45,0;

, which means that this packet has an ID of 233, the current hand proximity is 5cm, front proximity is out of sensor
range (i.e. no obstacles in front), left and right proximities are 100cm, the user's current location is 50cm north-east
from the starting location, the uers's current heading is 47 degrees clockwise from north, and the user did not climb
any stairs since the start of navigation.

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
        self.frontProximity = ''
        self.leftProximity = ''
        self.rightProximity = ''
        self.distancesList = ['', '', '', '', '', '', '', '']
        self.heading = ''
        self.numStairsClimbed = ''
        
        i = 0 # for traversing through `bytestream`
        
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
        
        # to parse `frontProximity`
        i = i + 1
        while chr(bytestream[i]) != ',':
            self.frontProximity += chr(bytestream[i])
            i = i + 1
        self.frontProximity = int(self.frontProximity)
        
        # to parse `leftProximity`
        i = i + 1
        while chr(bytestream[i]) != ',':
            self.leftProximity += chr(bytestream[i])
            i = i + 1
        self.leftProximity = int(self.leftProximity)
        
        # to parse `rightProximity`
        i = i + 1
        while chr(bytestream[i]) != ',':
            self.rightProximity += chr(bytestream[i])
            i = i + 1
        self.rightProximity = int(self.rightProximity)
        
        # to parse `distancesList`
        i = i + 2
        while chr(bytestream[i]) != ',':
            self.distancesList[0] += chr(bytestream[i])
            i = i + 1
        self.distancesList[0] = int(self.distancesList[0])
        for j in range(1, 7):
            i = i + 1
            while chr(bytestream[i]) != ',':
                self.distancesList[j] += chr(bytestream[i])
                i = i + 1
            self.distancesList[j] = int(self.distancesList[j])
        i = i + 1
        while chr(bytestream[i]) != ']':
            self.distancesList[7] += chr(bytestream[i])
            i = i + 1
        self.distancesList[7] = int(self.distancesList[7])
        
        # to parse `heading`
        i = i + 2
        while chr(bytestream[i]) != ',':
            self.heading += chr(bytestream[i])
            i = i + 1
        self.heading = int(self.heading)
        
        # to parse `numStairsClimbed`
        i = i + 1
        while chr(bytestream[i]) != ';':
            self.numStairsClimbed += chr(bytestream[i])
            i = i + 1
        self.numStairsClimbed = int(self.numStairsClimbed)
    
    def __str__(self, indent=0):
        result = ''
        result += 'packetId = #' + str(self.packetId) + '\n'
        result += 'handProximity = ' + str(self.handProximity) + ' cm\n'
        result += 'frontProximity = ' + str(self.frontProximity) + ' cm\n'
        result += 'leftProximity = ' + str(self.leftProximity) + ' cm\n'
        result += 'rightProximity = ' + str(self.rightProximity) + ' cm\n'
        result += 'distancesList = ' + str(self.distancesList) + ' cm\n'
        result += 'heading = ' + str(self.heading) + ' degrees from north\n'
        result += 'numStairsClimbed = ' + str(self.numStairsClimbed)
        return result

def test():
    bytestream = '233,5,-1,100,100,[0,50,0,0,0,0,0,0],45,0;'
    dataPacket = str(DataPacket(bytestream.encode('utf-8')))
    dataPacket = dataPacket.replace('\n', '\n    ') # add indentation
    
    print(stringHelper.INFO + ' Input Bytestream:\n    ' + bytestream)
    print(stringHelper.INFO + ' Parsed Data:\n    ' + dataPacket)

if __name__ == '__main__':
    test()
