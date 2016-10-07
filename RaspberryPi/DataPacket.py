'''
This file contains the definition of 'DataPacket' object class. A 'DataPacket' is instantiated from the transmitted
bytestream from Arduino Mega. The format of the bytestream should be

    <numPackets>,[<packetId>,<handProximity>,<frontProximity>,<leftProximity>,<rightProximity>,<displacement>,<heading>,
    <numStairsClimbed>],[ ... ], ... ,[ ... ];
                        ^~~~~~~       ^~~~~~~
                        2nd packet    last packet

. In particular, <displacement> is the displacement of the user from the previous location (i.e. user location when
previous data packet was polled) to the current location in the format of

    [<distance>,<direction>]

. Note that <direction> and <heading> are in degrees, with respect to geographical north. Also, <numPackets> should
always be 1, unless packet loss occured. The lost packet will be appended behind the next packet, and be transmitted
during the next data poll. Hence, the format of the bytestream representing one data packet is

    <packetId>,<handProximity>,<frontProximity>,<leftProximity>,<rightProximity>,<displacement>,<heading>,
    <numStairsClimbed>;

, for example,

    233,5,-1,100,100,[50,45],47,0;

, which means that this packet has an ID of 233,,the current hand proximity is 5cm, front proximity is out of sensor
range (i.e. no obstacles in front), left and right proximities are 100cm, the user has walked 50cm north-east since
previous data packet was polled, the uers's current heading is 47 degrees clockwise from north, and the user did not
climb any stairs since the previous data packet was polled.

@author: chen-zhuo
'''

class DataPacket:
    '''
    Parses 'bytestream' and updates the fields.
    '''
    def __init__(self, bytestream):
        self.packetId = ''
        self.handProximity = ''
        self.frontProximity = ''
        self.leftProximity = ''
        self.rightProximity = ''
        self.displacement = ['', '']
        self.heading = ''
        self.numStairsClimbed = ''
        
        i = 0 # for traversing through 'bytestream'
        
        # to parse 'packetId'
        while chr(bytestream[i]) != ',':
            self.packetId += chr(bytestream[i])
            i = i + 1
        self.packetId = int(self.packetId)
        
        # to parse 'handProximity'
        i = i + 1
        while chr(bytestream[i]) != ',':
            self.handProximity += chr(bytestream[i])
            i = i + 1
        self.handProximity = int(self.handProximity)
        
        # to parse 'frontProximity'
        i = i + 1
        while chr(bytestream[i]) != ',':
            self.frontProximity += chr(bytestream[i])
            i = i + 1
        self.frontProximity = int(self.frontProximity)
        
        # to parse 'leftProximity'
        i = i + 1
        while chr(bytestream[i]) != ',':
            self.leftProximity += chr(bytestream[i])
            i = i + 1
        self.leftProximity = int(self.leftProximity)
        
        # to parse 'rightProximity'
        i = i + 1
        while chr(bytestream[i]) != ',':
            self.rightProximity += chr(bytestream[i])
            i = i + 1
        self.rightProximity = int(self.rightProximity)
        
        # to parse 'displacement'
        i = i + 2
        while chr(bytestream[i]) != ',':
            self.displacement[0] += chr(bytestream[i])
            i = i + 1
        self.displacement[0] = int(self.displacement[0])
        i = i + 1
        while chr(bytestream[i]) != ']':
            self.displacement[1] += chr(bytestream[i])
            i = i + 1
        self.displacement[1] = int(self.displacement[1])
        
        # to parse 'heading'
        i = i + 2
        while chr(bytestream[i]) != ',':
            self.heading += chr(bytestream[i])
            i = i + 1
        self.heading = int(self.heading)
        
        # to parse 'numStairsClimbed'
        i = i + 1
        while chr(bytestream[i]) != ';':
            self.numStairsClimbed += chr(bytestream[i])
            i = i + 1
        self.numStairsClimbed = int(self.numStairsClimbed)

def test():
    dataPacket = DataPacket('233,5,-1,100,100,[50,45],47,0;'.encode('utf_8'))
    print(dataPacket.packetId)
    print(dataPacket.handProximity)
    print(dataPacket.frontProximity)
    print(dataPacket.leftProximity)
    print(dataPacket.rightProximity)
    print(dataPacket.displacement)
    print(dataPacket.heading)
    print(dataPacket.numStairsClimbed)

if __name__ == '__main__':
    test()
