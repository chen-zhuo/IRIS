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
    
#     srcBuildingId = keypadInput.waitAndGetKeyPressesUntilHashKeyWithConfirmationDialog(
#             'plsKeyInOriginBuildingIdFollowedByTheHashKey')
#     srcBuildingStorey = keypadInput.waitAndGetKeyPressesUntilHashKeyWithConfirmationDialog(
#             'plsKeyInOriginBuildingStoreyFollowedByTheHashKey')
#     srcNodeId = keypadInput.waitAndGetKeyPressesUntilHashKeyWithConfirmationDialog(
#             'plsKeyInOriginNodeIdFollowedByTheHashKey')
#     destBuildingId = keypadInput.waitAndGetKeyPressesUntilHashKeyWithConfirmationDialog(
#             'plsKeyInDestinationBuildingIdFollowedByTheHashKey')
#     destBuildingStorey = keypadInput.waitAndGetKeyPressesUntilHashKeyWithConfirmationDialog(
#         'plsKeyInDestinationBuildingStoreyFollowedByTheHashKey')
#     destNodeId = keypadInput.waitAndGetKeyPressesUntilHashKeyWithConfirmationDialog(
#         'plsKeyInDestinationNodeIdFollowedByTheHashKey')
#     
#     srcNodeId += srcBuildingId*1000 + srcBuildingStorey*100
#     destNodeId += destBuildingId*1000 + destBuildingStorey*100
    srcNodeId = 1211
    destNodeId = 1216
    print('srcNodeId = ' + srcNodeId)
    print('destNodeId = ' + destNodeId)
    
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
