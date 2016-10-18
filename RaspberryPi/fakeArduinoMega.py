'''


@author: chen-zhuo
'''

from DataPacket import DataPacket

dataPackets = [DataPacket('1,[0,0,233,233,100,100,[1000,135],135,0];'.encode('utf_8')), # between 1211 and 1214
               DataPacket('1,[1,0,233,233,100,100,[1002,135],135,0];'.encode('utf_8')), # at 1214
               DataPacket('1,[1,0,233,233,100,100,[244,225],225,0];'.encode('utf_8')), # at 1237
               DataPacket('1,[1,0,233,233,100,100,[812,225],135,0];'.encode('utf_8')), # at 1216
              ]

def getDataPacket():
    if len(dataPackets) > 0:
        dataPacket = dataPackets[0]
        dataPacket.pop(0)
    return dataPacket

if __name__ == '__main__':
    pass
