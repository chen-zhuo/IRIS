'''
This file contains the `main()` function, which is the starting point of the program. High-level algorithms such as task
scheduling, thread instantiations, are defined here.

@author: chen-zhuo
'''

from algorithms import computeRoute, downloadAndParseMap, linkMaps, printWelcomeMsg
import audioOutput
import json
import keypadInput
from threading import Thread
from time import sleep
import stringHelper

def main():
    keypadInput.initKeypad()
    audioOutput.initAudio()
    
    printWelcomeMsg()
    
    print(stringHelper.AUDIO + ' Welcome to IRIS.')
    audioOutput.playAudio('welcomeToIris')
    sleep(3)
    
    print(stringHelper.AUDIO + ' Please key in origin building ID, followed by the hash key.')
    audioOutput.playAudio('plsKeyInOriginBuildingIdFollowedByTheHashKey')
    srcBuildingId = keypadInput.waitAndGetKeyPressesUntilHashKey()
    
    print(stringHelper.AUDIO + ' Please key in origin building storey, followed by the hash key.')
    audioOutput.playAudio('plsKeyInOriginBuildingStoreyFollowedByTheHashKey')
    srcBuildingStorey = keypadInput.waitAndGetKeyPressesUntilHashKey()
    
    print(stringHelper.AUDIO + ' Please key in origin node ID, followed by the hash key.')
    audioOutput.playAudio('plsKeyInOriginNodeIdFollowedByTheHashKey')
    srcNodeId = keypadInput.waitAndGetKeyPressesUntilHashKey()
    
    print(stringHelper.AUDIO + ' Please key in destination building ID, followed by the hash key.')
    audioOutput.playAudio('plsKeyInDestinationBuildingIdFollowedByTheHashKey')
    destBuildingId = keypadInput.waitAndGetKeyPressesUntilHashKey()
    
    print(stringHelper.AUDIO + ' Please key in destination building storey, followed by the hash key.')
    audioOutput.playAudio('plsKeyInDestinationBuildingStoreyFollowedByTheHashKey')
    destBuildingStorey = keypadInput.waitAndGetKeyPressesUntilHashKey()
    
    print(stringHelper.AUDIO + ' Please key in destination node ID, followed by the hash key.')
    audioOutput.playAudio('plsKeyInDestinationNodeIdFollowedByTheHashKey')
    destNodeId = keypadInput.waitAndGetKeyPressesUntilHashKey()
    
    srcNodeId += srcBuildingId*1000 + srcBuildingStorey*100
    destNodeId += destBuildingId*1000 + destBuildingStorey*100
    
    mapOfCom1Level1 = downloadAndParseMap('COM1', 1)
    mapOfCom1Level2 = downloadAndParseMap('COM1', 2)
    mapOfCom2Level2 = downloadAndParseMap('COM2', 2)
    mapOfCom2Level3 = downloadAndParseMap('COM2', 3)
    linkedMap = linkMaps([mapOfCom1Level1, mapOfCom1Level2, mapOfCom2Level2, mapOfCom2Level3]);
    
    route = computeRoute(linkedMap, srcNodeId, destNodeId)
    print('Route: ', end='')
    for i in range(len(route) - 1):
        print(str(route[i]) + ' -> ', end = "")
    print(route[len(route) - 1])
    
    

if __name__ == '__main__':
    main()
