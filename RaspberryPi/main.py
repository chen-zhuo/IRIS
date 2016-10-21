'''
This file contains the `main()` function, which is the starting point of the program. High-level algorithms such as task
scheduling, thread instantiations, are defined here.

@author: chen-zhuo
'''

import algorithms
import audioOutput
# import json
import keypadInput
import math
from Navigator import Navigator
from SimplePiMegaCommunicator import PiMegaCommunicator # <-----------------------------
import stringHelper
# from threading import Thread
from time import sleep

def main():
    algorithms.printWelcomeMsg()
    
    keypadInput.initKeypad()
    audioOutput.initAudio()
    
    print(stringHelper.AUDIO + ' Welcome to IRIS.')
    audioOutput.playAudio('welcomeToIris')
    
    srcNodeId = int(keypadInput.waitAndGetKeyPressesUntilHashKeyWithConfirmationDialog(
            'plsKeyInOriginNodeIdFollowedByTheHashKey'))
    destNodeId = int(keypadInput.waitAndGetKeyPressesUntilHashKeyWithConfirmationDialog(
            'plsKeyInDestinationNodeIdFollowedByTheHashKey'))
    print(stringHelper.INFO + ' srcNodeId = ' + str(srcNodeId))
    print(stringHelper.INFO + ' destNodeId = ' + str(destNodeId))
    
    mapOfCom1Level1 = algorithms.downloadAndParseMap('COM1', 1)
    mapOfCom1Level2 = algorithms.downloadAndParseMap('COM1', 2)
    mapOfCom2Level2 = algorithms.downloadAndParseMap('COM2', 2)
    mapOfCom2Level3 = algorithms.downloadAndParseMap('COM2', 3)
    linkedMap = algorithms.linkMaps([mapOfCom1Level1, mapOfCom1Level2, mapOfCom2Level2, mapOfCom2Level3]);
    
    route = algorithms.computeRoute(linkedMap, srcNodeId, destNodeId)
    print(stringHelper.INFO + ' Route: ', end='')
    for i in range(len(route) - 1):
        print(str(route[i]) + ' -> ', end = "")
    print(route[len(route) - 1])
    
    # =========================== NAVIGATION START ===========================================
    
    piMegaCommunicator = PiMegaCommunicator() # <-----------------------------
    piMegaCommunicator.startUp() # <-----------------------------
    
    isNavigationInProgress = True
    currBuildingId = int(str(srcNodeId)[0])
    currLocation = [linkedMap.nodesDict[srcNodeId].x, linkedMap.nodesDict[srcNodeId].y]
    routeIdxOfPrevNode = 0
    routeIdxOfNextNode = 1
    
    navigator = Navigator(linkedMap, route, currLocation[0], currLocation[1])
    
    while isNavigationInProgress:
        piMegaCommunicator.pollData() # <-----------------------------
        
        packetId = piMegaCommunicator.packetId
        distanceWalked_north = piMegaCommunicator.distanceWalked_north
        distanceWalked_northeast = piMegaCommunicator.distanceWalked_northeast
        distanceWalked_east = piMegaCommunicator.distanceWalked_east
        distanceWalked_southeast = piMegaCommunicator.distanceWalked_southeast
        distanceWalked_south = piMegaCommunicator.distanceWalked_south
        distanceWalked_southwest = piMegaCommunicator.distanceWalked_southwest
        distanceWalked_west = piMegaCommunicator.distanceWalked_west
        distanceWalked_northwest = piMegaCommunicator.distanceWalked_northwest
        heading = piMegaCommunicator.heading
        
        currLocation = [linkedMap.nodesDict[srcNodeId].x, linkedMap.nodesDict[srcNodeId].y]
        currLocation[0] -= distanceWalked_north/math.sqrt(2)
        currLocation[1] += distanceWalked_north/math.sqrt(2)
        currLocation[1] += distanceWalked_northeast
        currLocation[0] += distanceWalked_east/math.sqrt(2)
        currLocation[1] += distanceWalked_east/math.sqrt(2)
        currLocation[0] += distanceWalked_southeast
        currLocation[0] += distanceWalked_south/math.sqrt(2)
        currLocation[1] -= distanceWalked_south/math.sqrt(2)
        currLocation[1] -= distanceWalked_southwest
        currLocation[0] -= distanceWalked_west/math.sqrt(2)
        currLocation[1] -= distanceWalked_west/math.sqrt(2)
        currLocation[0] -= distanceWalked_northwest
        print('\n==================================================\n')
        print(stringHelper.INFO + ' packetId = ' + str(packetId) + ', ', end='')
        print('currLocation = ' + str(currLocation))
        
        navigator.updateLocation(currLocation[0], currLocation[1], heading)
        
        if navigator.clearedRouteIdx + 1 == len(navigator.route):
            print(stringHelper.AUDIO + ' Navigation completed.')
            audioOutput.playAudio('navigationCompleted')
            break
        
        naviInfo = navigator.getNaviInfo()
        
        routeIdxOfNextNode = navigator.clearedRouteIdx + 1
        routeIdxOfPrevNode = routeIdxOfNextNode - 1
        print(stringHelper.INFO + ' nextNodeId = ' + str(navigator.route[navigator.clearedRouteIdx + 1]))
        
        print(stringHelper.INFO + ' heading = ' + str(heading) + ', ', end='')
        expectedHeading = algorithms.computeBearing(linkedMap.nodesDict[route[routeIdxOfPrevNode]].x,
                                                    linkedMap.nodesDict[route[routeIdxOfPrevNode]].y,
                                                    linkedMap.nodesDict[route[routeIdxOfNextNode]].x,
                                                    linkedMap.nodesDict[route[routeIdxOfNextNode]].y,
                                                    ) + 45
        print('expectedHeading = ' + str(expectedHeading))
        print(stringHelper.INFO + ' prevNode -> nextNode = (' + str(linkedMap.nodesDict[route[routeIdxOfPrevNode]].x) +
              ', ' + str(linkedMap.nodesDict[route[routeIdxOfPrevNode]].y) + ') -> (' +
              str(linkedMap.nodesDict[route[routeIdxOfNextNode]].x) + ', ' +
              str(linkedMap.nodesDict[route[routeIdxOfNextNode]].y) + ')')
        
        # to give steps remaining instructions
        straightLineDistanceToNextNode = algorithms.computeDistance(currLocation[0],
                                                                    currLocation[1],
                                                                    linkedMap.nodesDict[route[routeIdxOfNextNode]].x,
                                                                    linkedMap.nodesDict[route[routeIdxOfNextNode]].y)
        stepsRemainingToNextNode = int(straightLineDistanceToNextNode//40)
        print(stringHelper.AUDIO + ' ' + str(stepsRemainingToNextNode) + ' steps to next node.')
        audioOutput.playInt(str(stepsRemainingToNextNode))
        audioOutput.playAudio('stepsToNextNode')
        
        
        # to give turning instructions
        if packetId != 0:
            if heading - expectedHeading > 22.5 and heading - expectedHeading < 67.5:
                print(stringHelper.AUDIO + ' Adjust heading: left')
                audioOutput.playAudio('adjustHeading')
                audioOutput.playAudio('left')
            elif heading - expectedHeading > 67.5 and heading - expectedHeading < 180:
                print(stringHelper.AUDIO + ' Turn left.')
                audioOutput.playAudio('turnLeft')
            elif heading - expectedHeading < -67.5 and heading - expectedHeading > -180:
                print(stringHelper.AUDIO + ' Turn right.')
                audioOutput.playAudio('turnRight')
            elif heading - expectedHeading > -67.5 and heading - expectedHeading < -22.5:
                print(stringHelper.AUDIO + ' Adjust heading: right')
                audioOutput.playAudio('adjustHeading')
                audioOutput.playAudio('right')
        else:
            print(stringHelper.AUDIO + ' Adjust heading: ' + str(expectedHeading - heading) + ' degrees.')
            audioOutput.playAudio('adjustHeading')
            audioOutput.playInt(expectedHeading - heading)
            audioOutput.playAudio('degrees')
        
        sleep(5)
    
    # =========================== NAVIGATION END ===========================================
    
    keypadInput.closeKeypadThread()
    audioOutput.closeAudioThread()

if __name__ == '__main__':
    main()
