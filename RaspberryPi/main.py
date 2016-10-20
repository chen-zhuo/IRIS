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
    
    srcNodeId = keypadInput.waitAndGetKeyPressesUntilHashKeyWithConfirmationDialog(
            'plsKeyInOriginNodeIdFollowedByTheHashKey')
    destNodeId = keypadInput.waitAndGetKeyPressesUntilHashKeyWithConfirmationDialog(
            'plsKeyInDestinationNodeIdFollowedByTheHashKey')
    
    print(stringHelper.INFO + ' srcNodeId = ' + srcNodeId)
    print(stringHelper.INFO + ' destNodeId = ' + destNodeId)
    
    mapOfCom1Level1 = algorithms.downloadAndParseMap('COM1', 1)
    mapOfCom1Level2 = algorithms.downloadAndParseMap('COM1', 2)
    mapOfCom2Level2 = algorithms.downloadAndParseMap('COM2', 2)
    mapOfCom2Level3 = algorithms.downloadAndParseMap('COM2', 3)
#     linkedMap = algorithms.linkMaps([mapOfCom1Level1, mapOfCom1Level2, mapOfCom2Level2, mapOfCom2Level3]);
    
    print('\n=============== Adjacency List for Linked Map ===============\n')
    linkedMap = algorithms.linkMaps([mapOfCom1Level1, mapOfCom1Level2, mapOfCom2Level2, mapOfCom2Level3]);
    for node in linkedMap.nodesDict.values():
        print(str(node.nodeId) + ': ' + str(sorted(list(node.adjacentNodes.keys()))))
    print('\n==================================================\n')
    
    route = algorithms.computeRoute(linkedMap, srcNodeId, destNodeId)
    print('Route: ', end='')
    for i in range(len(route) - 1):
        print(str(route[i]) + ' -> ', end = "")
    print(route[len(route) - 1])
    
    keypadInput.closeKeypadThread()
    audioOutput.closeAudioThread()

if __name__ == '__main__':
    main()
