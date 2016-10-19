'''
This file contains the `main()` function, which is the starting point of the program. High-level algorithms such as task
scheduling, thread instantiations, are defined here.

@author: chen-zhuo
'''

import algorithms
import audioOutput
# import json
import keypadInput
from DummyPiMegaCommunicator import PiMegaCommunicator
import stringHelper
# from threading import Thread
# from time import sleep

def main():
    algorithms.printWelcomeMsg()
    
    keypadInput.initKeypad()
    audioOutput.initAudio()
    piMegaCommunicator = PiMegaCommunicator()
    piMegaCommunicator.startUp()
    
    print(piMegaCommunicator.pollData())
    print(piMegaCommunicator.pollData())
    print(piMegaCommunicator.pollData())
    
    print(stringHelper.AUDIO + ' Welcome to IRIS.')
    audioOutput.playAudio('welcomeToIris')
    
    srcBuildingId = keypadInput.waitAndGetKeyPressesUntilHashKeyWithConfirmationDialog(
            'plsKeyInOriginBuildingIdFollowedByTheHashKey')
    srcBuildingStorey = keypadInput.waitAndGetKeyPressesUntilHashKeyWithConfirmationDialog(
            'plsKeyInOriginBuildingStoreyFollowedByTheHashKey')
    srcNodeId = keypadInput.waitAndGetKeyPressesUntilHashKeyWithConfirmationDialog(
            'plsKeyInOriginNodeIdFollowedByTheHashKey')
    destBuildingId = keypadInput.waitAndGetKeyPressesUntilHashKeyWithConfirmationDialog(
            'plsKeyInDestinationBuildingIdFollowedByTheHashKey')
    destBuildingStorey = keypadInput.waitAndGetKeyPressesUntilHashKeyWithConfirmationDialog(
        'plsKeyInDestinationBuildingStoreyFollowedByTheHashKey')
    destNodeId = keypadInput.waitAndGetKeyPressesUntilHashKeyWithConfirmationDialog(
        'plsKeyInDestinationNodeIdFollowedByTheHashKey')
    
    print('srcBuildingId = ' + srcBuildingId)
    print('srcBuildingStorey = ' + srcBuildingStorey)
    print('srcNodeId = ' + srcNodeId)
    
    srcBuildingId = int(srcBuildingId)
    srcBuildingStorey = int(srcBuildingStorey)
    srcNodeId = int(srcNodeId)
    destBuildingId = int(destBuildingId)
    destBuildingStorey = int(destBuildingStorey)
    destNodeId = int(destNodeId)
    
    srcNodeId += srcBuildingId*1000 + srcBuildingStorey*100
    destNodeId += destBuildingId*1000 + destBuildingStorey*100
    print('srcNodeId = ' + str(srcNodeId))
    print('destNodeId = ' + str(destNodeId))
    
    mapOfCom1Level1 = algorithms.downloadAndParseMap('COM1', 1)
    mapOfCom1Level2 = algorithms.downloadAndParseMap('COM1', 2)
    mapOfCom2Level2 = algorithms.downloadAndParseMap('COM2', 2)
    mapOfCom2Level3 = algorithms.downloadAndParseMap('COM2', 3)
    linkedMap = algorithms.linkMaps([mapOfCom1Level1, mapOfCom1Level2, mapOfCom2Level2, mapOfCom2Level3]);
    
    route = algorithms.computeRoute(linkedMap, srcNodeId, destNodeId)
    print('Route: ', end='')
    for i in range(len(route) - 1):
        print(str(route[i]) + ' -> ', end = "")
    print(route[len(route) - 1])
    
    keypadInput.closeKeypadThread()
    audioOutput.closeAudioThread()

if __name__ == '__main__':
    main()
