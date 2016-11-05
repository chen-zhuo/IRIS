'''
This file contains the `main()` function, which is the starting point of the program. High-level algorithms such as task
scheduling, thread instantiations, are defined here.

@author: chen-zhuo
'''

import algorithms
import audioOutput
import keypadInput
# import math
from Navigator import Navigator
from DummyPiMegaCommunicator import PiMegaCommunicator
import stringHelper
# from threading import Thread
from time import sleep

isFastDebugMode = True
hardCodedSrcNodeId = 1211
hardCodedDestNodeId = 1216

def main():
    global isFastDebugMode, hardCodedSrcNodeId, hardCodedDestNodeId
    
    algorithms.printWelcomeMsg()
    keypadInput.initKeypad()
    audioOutput.initAudio()
    
    print(stringHelper.AUDIO + ' Welcome to IRIS.')
    audioOutput.playAudio('welcomeToIris')
    print(stringHelper.AUDIO + ' Playing arpeggio audio test...')
    audioOutput.playAudio('arpeggio_soundEffect')
    
    # to get `srcNodeId` and `destNodeId`
    if isFastDebugMode:
        srcNodeId = hardCodedSrcNodeId
        destNodeId = hardCodedDestNodeId
    else:
        srcNodeId = int(keypadInput.waitAndGetKeypadInputWithAudioPrompt(
                'plsKeyInOriginNodeIdFollowedByTheHashKey'))
        destNodeId = int(keypadInput.waitAndGetKeypadInputWithAudioPrompt(
                'plsKeyInDestinationNodeIdFollowedByTheHashKey'))
    print(stringHelper.INFO + ' srcNodeId = ' + str(srcNodeId))
    print(stringHelper.INFO + ' destNodeId = ' + str(destNodeId))
    
    # to get map info and compute route
    mapOfCom1Level2 = algorithms.downloadAndParseMap('1', '2')
    mapOfCom2Level2 = algorithms.downloadAndParseMap('2', '2')
    mapOfCom2Level3 = algorithms.downloadAndParseMap('2', '3')
    linkedMap = algorithms.linkMaps([mapOfCom1Level2, mapOfCom2Level2, mapOfCom2Level3]);
    route = algorithms.computeRoute(linkedMap, srcNodeId, destNodeId)
    algorithms.printRoute(route)
    
    # ======================================== BEGIN NAVIGATION ========================================
    
    isNavigationInProgress = True
    isNavigationPaused = False # when paused, ignore any steps that the user performs
    currLocation = [linkedMap.nodesDict[srcNodeId].x, linkedMap.nodesDict[srcNodeId].y]
    locationOffset = [0, 0]
    routeIdxOfPrevNode = 0
    routeIdxOfNextNode = 1
    
    navigator = Navigator(linkedMap, route, currLocation)
    
    piMegaCommunicator = PiMegaCommunicator()
    piMegaCommunicator.startUp()
    
    while isNavigationInProgress:
        # to poll for new data and update `navigator`
        print('\n========================= NEW DATA POLL =========================\n')
        dataPacket = piMegaCommunicator.pollData()
        print(stringHelper.INFO + ' ' + str(dataPacket))
        isNavigationInProgress = navigator.update(dataPacket)
        
        # to get and print the the previous node and the next node
        routeIdxOfNextNode = navigator.clearedRouteIdx + 1
        routeIdxOfPrevNode = navigator.clearedRouteIdx
        print(stringHelper.INFO + ' prevNode -> nextNode = #' + str(route[routeIdxOfPrevNode]) + ' -> #' +
              str(route[routeIdxOfNextNode]) + ' = (' + str(linkedMap.nodesDict[route[routeIdxOfPrevNode]].x) +
              ', ' + str(linkedMap.nodesDict[route[routeIdxOfPrevNode]].y) + ') -> (' +
              str(linkedMap.nodesDict[route[routeIdxOfNextNode]].x) + ', ' +
              str(linkedMap.nodesDict[route[routeIdxOfNextNode]].y) + ')')
        
        # to compute and print the current heading and the expected heading
        print(stringHelper.INFO + ' heading = ' + str(dataPacket.heading) + ', ', end='')
        expectedHeading = algorithms.computeBearing(
                linkedMap.nodesDict[route[routeIdxOfPrevNode]].x, linkedMap.nodesDict[route[routeIdxOfPrevNode]].y,
                linkedMap.nodesDict[route[routeIdxOfNextNode]].x, linkedMap.nodesDict[route[routeIdxOfNextNode]].y
                ) + 45 # @author chen-zhuo warning: hard-coded offset; assumes `northAt` is 315 for all maps
        print('expectedHeading = ' + str(expectedHeading))
        
        # to give beep sounds as the turning instruction; with C major scale (1 = C4),
        #     "3" means "go straight";
        #     "1" means "turn left 45 degrees";
        #     "5" means "turn right 45 degrees";
        #     "11" means "turn left 90 degrees";
        #     "55" means "turn right 90 degrees";
        #     "111" means "turn left 135 degrees";
        #     "555" means "turn right 135 degrees";
        #     "1(+8va)" means "turn 180 degrees"
        if expectedHeading - dataPacket.heading == 0:
            print(stringHelper.AUDIO + ' Adjust heading: 0 degree')
            audioOutput.playAudioNow('heading+0_soundEffect')
        elif expectedHeading - dataPacket.heading == -45 or expectedHeading - dataPacket.heading == 315:
            print(stringHelper.AUDIO + ' Adjust heading: -45 degrees')
            audioOutput.playAudioNow('heading-45_soundEffect')
        elif expectedHeading - dataPacket.heading == 45 or expectedHeading - dataPacket.heading == -315:
            print(stringHelper.AUDIO + ' Adjust heading: +45 degrees')
            audioOutput.playAudioNow('heading+45_soundEffect')
        elif expectedHeading - dataPacket.heading == -90 or expectedHeading - dataPacket.heading == 270:
            print(stringHelper.AUDIO + ' Adjust heading: -90 degrees')
            audioOutput.playAudioNow('heading-90_soundEffect')
        elif expectedHeading - dataPacket.heading == 90 or expectedHeading - dataPacket.heading == -270:
            print(stringHelper.AUDIO + ' Adjust heading: +90 degrees')
            audioOutput.playAudioNow('heading+90_soundEffect')
        elif expectedHeading - dataPacket.heading == -135 or expectedHeading - dataPacket.heading == 225:
            print(stringHelper.AUDIO + ' Adjust heading: -135 degrees')
            audioOutput.playAudioNow('heading-135_soundEffect')
        elif expectedHeading - dataPacket.heading == 135 or expectedHeading - dataPacket.heading == -225:
            print(stringHelper.AUDIO + ' Adjust heading: +135 degrees')
            audioOutput.playAudioNow('heading+135_soundEffect')
        elif expectedHeading - dataPacket.heading == 180 or expectedHeading - dataPacket.heading == -180:
            print(stringHelper.AUDIO + ' Adjust heading: 180 degrees')
            audioOutput.playAudioNow('heading+180_soundEffect')
        else:
            print(stringHelper.ERROR + ' at main(): Unhandled case of heading adjustment; expectedHeading - \
                  dataPacket.heading = ' + str(expectedHeading - dataPacket.heading))
        
        # get the user input (if any)
        userInput = keypadInput.getKeypadInput()
        
        # if the user input is '9', give detailed audio feedback
        if userInput == '9':
            straightLineDistanceToNextNode = algorithms.computeDistance(currLocation,
                                                                        linkedMap.nodesDict[route[routeIdxOfNextNode]].location)
            stepsRemainingToNextNode = int(int(straightLineDistanceToNextNode)//40)
            print(stringHelper.AUDIO + ' ' + str(stepsRemainingToNextNode) + ' steps to next node.')
            audioOutput.playInt(str(int(stepsRemainingToNextNode)))
            audioOutput.playAudio('stepsToNextNode')
        
        # if the user input is '1', snap the current location to the previous node in route
        if userInput == '1':
            keypadInput.tempUserInput = ''
            navigator.clearedRouteIdx -= 1
            print('clearedRouteIdx = ' + str(navigator.clearedRouteIdx) + ', prevNodeId = ' + str(navigator.route[navigator.clearedRouteIdx]))
            
            print(stringHelper.AUDIO + ' Reached node Id: #' + str(navigator.route[navigator.clearedRouteIdx]))
            audioOutput.playAudio('reachedNewNodeSoundEffect')
            audioOutput.playAudio('reached')
            audioOutput.playAudio('nodeId')
            audioOutput.playInt(navigator.route[navigator.clearedRouteIdx])
            
            locationOffset[0] += linkedMap.nodesDict[navigator.route[navigator.clearedRouteIdx]].location[0] - currLocation[0]
            locationOffset[1] += linkedMap.nodesDict[navigator.route[navigator.clearedRouteIdx]].location[1] - currLocation[1]
        
        # if the user input is '3', snap the current location to the next node in route
        if userInput == '3':
            keypadInput.tempUserInput = ''
            navigator.clearedRouteIdx += 1
        
            print(stringHelper.AUDIO + ' Reached node Id: #' + str(navigator.route[navigator.clearedRouteIdx]))
            audioOutput.playAudio('reachedNewNodeSoundEffect')
            audioOutput.playAudio('reached')
            audioOutput.playAudio('nodeId')
            audioOutput.playInt(navigator.route[navigator.clearedRouteIdx])
            locationOffset[0] += linkedMap.nodesDict[navigator.route[navigator.clearedRouteIdx]].location[0] - currLocation[0]
            locationOffset[1] += linkedMap.nodesDict[navigator.route[navigator.clearedRouteIdx]].location[1] - currLocation[1]
        
        # to give turning instructions; with C major scale (1 = C4),
        #     "3" means "go straight";
        #     "1" means "turn left 45 degrees";
        #     "5" means "turn right 45 degrees";
        #     "11" means "turn left 90 degrees";
        #     "55" means "turn right 90 degrees";
        #     "111" means "turn left 135 degrees";
        #     "555" means "turn right 135 degrees";
        #     "1(+8va)" means "turn 180 degrees"
        if expectedHeading - dataPacket.heading == 0:
            print(stringHelper.AUDIO + ' Adjust heading: 0 degree')
            audioOutput.playAudioNow('heading+0_soundEffect')
        elif expectedHeading - dataPacket.heading == -45 or expectedHeading - dataPacket.heading == 315:
            print(stringHelper.AUDIO + ' Adjust heading: -45 degrees')
            audioOutput.playAudioNow('heading-45_soundEffect')
        elif expectedHeading - dataPacket.heading == 45 or expectedHeading - dataPacket.heading == -315:
            print(stringHelper.AUDIO + ' Adjust heading: +45 degrees')
            audioOutput.playAudioNow('heading+45_soundEffect')
        elif expectedHeading - dataPacket.heading == -90 or expectedHeading - dataPacket.heading == 270:
            print(stringHelper.AUDIO + ' Adjust heading: -90 degrees')
            audioOutput.playAudioNow('heading-90_soundEffect')
        elif expectedHeading - dataPacket.heading == 90 or expectedHeading - dataPacket.heading == -270:
            print(stringHelper.AUDIO + ' Adjust heading: +90 degrees')
            audioOutput.playAudioNow('heading+90_soundEffect')
        elif expectedHeading - dataPacket.heading == -135 or expectedHeading - dataPacket.heading == 225:
            print(stringHelper.AUDIO + ' Adjust heading: -135 degrees')
            audioOutput.playAudioNow('heading-135_soundEffect')
        elif expectedHeading - dataPacket.heading == 135 or expectedHeading - dataPacket.heading == -225:
            print(stringHelper.AUDIO + ' Adjust heading: +135 degrees')
            audioOutput.playAudioNow('heading+135_soundEffect')
        elif expectedHeading - dataPacket.heading == 180 or expectedHeading - dataPacket.heading == -180:
            print(stringHelper.AUDIO + ' Adjust heading: 180 degrees')
            audioOutput.playAudioNow('heading+180_soundEffect')
        else:
            print(stringHelper.ERROR + ' at main(): Unhandled case of heading adjustment; expectedHeading - \
                  dataPacket.heading = ' + str(expectedHeading - dataPacket.heading))
        
        sleep(3)
        
        # ======================================== END NAVIGATION ========================================
        
        keypadInput.closeKeypadThread()
        audioOutput.closeAudioThread()

if __name__ == '__main__':
    main()
