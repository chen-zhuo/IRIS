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
from DummyPiMegaCommunicator import PiMegaCommunicator # <-----------------------------
import stringHelper
# from threading import Thread
from time import sleep

def main():
    algorithms.printWelcomeMsg()
    
    keypadInput.initKeypad()
    audioOutput.initAudio()
    piMegaCommunicator = PiMegaCommunicator() # <-----------------------------
    piMegaCommunicator.startUp() # <-----------------------------
    
    print(piMegaCommunicator.pollData())
    print(piMegaCommunicator.pollData())
    print(piMegaCommunicator.pollData())
    
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
    print('Route: ', end='')
    for i in range(len(route) - 1):
        print(str(route[i]) + ' -> ', end = "")
    print(route[len(route) - 1])
    
    # =========================== NAVIGATION START ===========================================
    
    isNavigationInProgress = True
    currBuildingId = int(str(srcNodeId)[0])
    currLocation = [linkedMap.nodesDict[srcNodeId].x, linkedMap.nodesDict[srcNodeId].y]
    routeIdxOfPrevNode = 0
    routeIdxOfNextNode = 1
    
    navigator = Navigator(linkedMap, route, currLocation[0], currLocation[1])
    
    while isNavigationInProgress:
        piMegaCommunicator.pollData() # <-----------------------------
        
        distanceWalked_north = piMegaCommunicator.distanceWalked_north
        distanceWalked_northeast = piMegaCommunicator.distanceWalked_northeast
        distanceWalked_east = piMegaCommunicator.distanceWalked_east
        distanceWalked_southeast = piMegaCommunicator.distanceWalked_southeast
        distanceWalked_south = piMegaCommunicator.distanceWalked_south
        distanceWalked_southwest = piMegaCommunicator.distanceWalked_southwest
        distanceWalked_west = piMegaCommunicator.distanceWalked_west
        distanceWalked_northwest = piMegaCommunicator.distanceWalked_northwest
        heading = piMegaCommunicator.heading
        
        currLocation = [0, 0]
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
        print(stringHelper.INFO + ' currLocation = ' + currLocation)
        
        navigator.updateLocation(currLocation[0], currLocation[1], heading)
        naviInfo = navigator.getNaviInfo()
        
        if naviInfo[1] > 67.5 and naviInfo[1] < 180:
            print(stringHelper.AUDIO + ' Turn right.')
            audioOutput.playAudio('turnRight')
        elif naviInfo[1] > 180 and naviInfo[1] < 292.5:
            print(stringHelper.AUDIO + ' Turn left.')
            audioOutput.playAudio('turnLeft')
        
        print(stringHelper.INFO + ' heading = ' + heading)
        expectedHeading = algorithms.computeBearing(linkedMap[route[routeIdxOfNextNode]].x,
                                                    linkedMap[route[routeIdxOfNextNode]].y,
                                                    linkedMap[route[routeIdxOfPrevNode]].x,
                                                    linkedMap[route[routeIdxOfPrevNode]].y)
        print(stringHelper.INFO + ' expectedHeading = ' + expectedHeading)
        
        if heading - expectedHeading > 25:
            print(stringHelper.AUDIO + ' Adjust your bearing slightly to the left.')
            audioOutput.playAudio('adjustYourBearingSlightlyToTheLeft')
        elif heading - expectedHeading < -25:
            print(stringHelper.AUDIO + ' Adjust your bearing slightly to the right.')
            audioOutput.playAudio('adjustYourBearingSlightlyToTheRight')
        
        
        
        sleep(5)
    
    # =========================== NAVIGATION END ===========================================
    
    keypadInput.closeKeypadThread()
    audioOutput.closeAudioThread()

if __name__ == '__main__':
    main()
