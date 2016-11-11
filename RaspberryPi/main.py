'''
This file contains the `main()` function, which is the starting point of the program. High-level algorithms such as task
scheduling, thread instantiations, are defined here.

@author: chen-zhuo
'''

import algorithms
import audioOutput
import keypadInput
# import math
from Navigator import Navigator, STEP_LENGTH
# from DummyPiMegaCommunicator import PiMegaCommunicator # <---------- use this when debugging on Pi only
from SimplePiMegaCommunicator import PiMegaCommunicator # <---------- use this when communicating with Mega
import stringHelper
# from threading import Thread
from time import sleep

IS_FAST_DEBUG_MODE = True
HARDCODED_SRC_NODE_ID = 1211
HARDCODED_DEST_NODE_ID = 1216

def main():
    global IS_FAST_DEBUG_MODE, HARDCODED_SRC_NODE_ID, HARDCODED_DEST_NODE_ID
    
    algorithms.printWelcomeMsg()
    keypadInput.initKeypad()
    audioOutput.initAudio()
    
    # to get `srcNodeId` and `destNodeId` from user
    if IS_FAST_DEBUG_MODE:
        srcNodeId = HARDCODED_SRC_NODE_ID
        destNodeId = HARDCODED_DEST_NODE_ID
    else:
        print(stringHelper.AUDIO + ' Welcome to IRIS.')
        audioOutput.playAudio('welcomeToIris')
#         print(stringHelper.AUDIO + ' Playing arpeggio audio test...')
#         audioOutput.playAudio('arpeggio_soundEffect')
        sleep(2)
        
        srcNodeId = int(keypadInput.waitAndGetKeypadInputWithAudioPrompt(
                'plsKeyInOriginNodeIdFollowedByTheHashKey'))
        destNodeId = int(keypadInput.waitAndGetKeypadInputWithAudioPrompt(
                'plsKeyInDestinationNodeIdFollowedByTheHashKey'))
    print(stringHelper.INFO + ' srcNodeId = ' + str(srcNodeId))
    print(stringHelper.INFO + ' destNodeId = ' + str(destNodeId))
    
    # to get map info and compute route
    mapOfCom1Level2 = algorithms.downloadAndParseMap(1, 2)
    mapOfCom2Level2 = algorithms.downloadAndParseMap(2, 2)
    mapOfCom2Level3 = algorithms.downloadAndParseMap(2, 3)
    linkedMap = algorithms.linkMaps([mapOfCom1Level2, mapOfCom2Level2, mapOfCom2Level3]);
    route = algorithms.computeRoute(linkedMap, srcNodeId, destNodeId)
    algorithms.printRoute(route)
    
    # ======================================== BEGIN NAVIGATION ========================================
    
    print(stringHelper.AUDIO + ' Navigation started.')
    audioOutput.playAudio('navigationStarted')
    
    isNavigationInProgress = True
    isNavigationPaused = False # when paused, ignore any steps that the user performs
    currLocation = linkedMap.nodesDict[srcNodeId].location
    routeIdxOfPrevNode = 0
    routeIdxOfNextNode = 1
    
    navigator = Navigator(linkedMap, route)
    
    piMegaCommunicator = PiMegaCommunicator()
    piMegaCommunicator.startUp()
    
    while isNavigationInProgress:
        # to poll for new data and update `navigator`
        print('\n========================= NEW DATA POLL =========================\n')
        dataPacket = piMegaCommunicator.pollData()
        
        if dataPacket == None:
            sleep(1.5)
            continue
        
        print(stringHelper.INFO + ' ' + stringHelper.highlight('    Data Packet:    ') + ' ' + str(dataPacket))
        isNavigationInProgress = navigator.update(dataPacket, isNavigationPaused)
        if not isNavigationInProgress:
            break
        
        # to get and print the the previous node and the next node
        routeIdxOfNextNode = navigator.clearedRouteIdx + 1
        routeIdxOfPrevNode = navigator.clearedRouteIdx
        print(stringHelper.INFO + ' ' + stringHelper.highlight('Prev/Next Node Info:') + ' ', end='')
        print('#' + str(route[routeIdxOfPrevNode]) + ' -> #' +
              str(route[routeIdxOfNextNode]) + ' === (' +
              str(linkedMap.nodesDict[route[routeIdxOfPrevNode]].location[0]) + ', ' +
              str(linkedMap.nodesDict[route[routeIdxOfPrevNode]].location[1]) + ') -> (' +
              str(linkedMap.nodesDict[route[routeIdxOfNextNode]].location[0]) + ', ' +
              str(linkedMap.nodesDict[route[routeIdxOfNextNode]].location[1]) + ')')
        
        # to print the current heading and the expected heading
        print(stringHelper.INFO + ' ' + stringHelper.highlight('   Heading Info:    ') + ' ', end='')
        print(str(navigator.currHeading) + ' ', end='')
        print('(expected: ' + str(navigator.expectedHeading) + '), ', end='')
        
        # to give beep sounds as the turning instruction; with C major scale (1 = C4),
        #     "3" means "go straight";
        #     "1" means "turn left 45 degrees";
        #     "5" means "turn right 45 degrees";
        #     "11" means "turn left 90 degrees";
        #     "55" means "turn right 90 degrees";
        #     "111" means "turn left 135 degrees";
        #     "555" means "turn right 135 degrees";
        #     "1(+8va)" means "turn 180 degrees"
        if (navigator.expectedHeading - navigator.currHeading) % 360 <= 22.5 or \
                (navigator.expectedHeading - navigator.currHeading) % 360 > 337.5:
            print(stringHelper.AUDIO + ' Adjust heading: 0 degree')
            audioOutput.playAudioNow('heading+0_soundEffect')
        elif (navigator.expectedHeading - navigator.currHeading) % 360 > 292.5 and \
                (navigator.expectedHeading - navigator.currHeading) % 360 <= 337.5:
            print(stringHelper.AUDIO + ' Adjust heading: -45 degrees')
            audioOutput.playAudioNow('heading-45_soundEffect')
        elif (navigator.expectedHeading - navigator.currHeading) % 360 > 22.5 and \
                (navigator.expectedHeading - navigator.currHeading) % 360 <= 67.5:
            print(stringHelper.AUDIO + ' Adjust heading: +45 degrees')
            audioOutput.playAudioNow('heading+45_soundEffect')
        elif (navigator.expectedHeading - navigator.currHeading) % 360 > 247.5 and \
                (navigator.expectedHeading - navigator.currHeading) % 360 <= 292.5:
            print(stringHelper.AUDIO + ' Adjust heading: -90 degrees')
            audioOutput.playAudioNow('heading-90_soundEffect')
        elif (navigator.expectedHeading - navigator.currHeading) % 360 > 67.5 and \
                (navigator.expectedHeading - navigator.currHeading) % 360 <= 112.5:
            print(stringHelper.AUDIO + ' Adjust heading: +90 degrees')
            audioOutput.playAudioNow('heading+90_soundEffect')
        elif (navigator.expectedHeading - navigator.currHeading) % 360 > 202.5 and \
                (navigator.expectedHeading - navigator.currHeading) % 360 <= 247.5:
            print(stringHelper.AUDIO + ' Adjust heading: -135 degrees')
            audioOutput.playAudioNow('heading-135_soundEffect')
        elif (navigator.expectedHeading - navigator.currHeading) % 360 > 112.5 and \
                (navigator.expectedHeading - navigator.currHeading) % 360 <= 157.5:
            print(stringHelper.AUDIO + ' Adjust heading: +135 degrees')
            audioOutput.playAudioNow('heading+135_soundEffect')
        elif (navigator.expectedHeading - navigator.currHeading) % 360 > 157.5 and \
                (navigator.expectedHeading - navigator.currHeading) % 360 <= 202.5:
            print(stringHelper.AUDIO + ' Adjust heading: 180 degrees')
            audioOutput.playAudioNow('heading+180_soundEffect')
        else:
            print(stringHelper.ERROR + ' at main(): Unhandled case of heading adjustment; expectedHeading - \
                  navigator.currHeading = ' + str(navigator.expectedHeading - navigator.currHeading))
        
        # get the user input (if any)
        userInput = keypadInput.getKeypadInput()
        
        # if the user input is '1', snap the current location to the previous node in route
        if userInput == '1':
            navigator.clearedRouteIdx -= 1
            print('clearedRouteIdx = ' + str(navigator.clearedRouteIdx) +
                  ', prevNodeId = ' + str(navigator.route[navigator.clearedRouteIdx]))
            
            print(stringHelper.AUDIO + ' Reached node Id: #' + str(navigator.route[navigator.clearedRouteIdx]))
            audioOutput.playAudio('reachedNewNode_soundEffect')
            audioOutput.playAudio('reached')
            audioOutput.playInt(navigator.route[navigator.clearedRouteIdx])
            audioOutput.playAudio('node' + str(navigator.route[navigator.clearedRouteIdx]) + '_description')
        
        # if the user input is '3', snap the current location to the next node in route
        if userInput == '3':
            navigator.clearedRouteIdx += 1
        
            print(stringHelper.AUDIO + ' Reached node Id: #' + str(navigator.route[navigator.clearedRouteIdx]))
            audioOutput.playAudio('reachedNewNode_soundEffect')
            audioOutput.playAudio('reached')
            audioOutput.playInt(navigator.route[navigator.clearedRouteIdx])
            audioOutput.playAudio('node' + str(navigator.route[navigator.clearedRouteIdx]) + '_description')
        
        # if the user input is '5', assume current heading is the expected heading (update heading offset)
        if userInput == '5':
            navigator.currHeading = navigator.expectedHeading
        
        # if the user input is '9', give detailed audio feedback
        if userInput == '9':
            audioOutput.playAudio('from')
            audioOutput.playInt(route[routeIdxOfPrevNode])
            audioOutput.playAudio('towards')
            audioOutput.playInt(route[routeIdxOfNextNode])
            
            straightLineDistanceToNextNode = algorithms.computeDistance(currLocation,
                                                                        linkedMap.nodesDict[route[routeIdxOfNextNode]].location)
            stepsRemainingToNextNode = int(int(straightLineDistanceToNextNode) // STEP_LENGTH)
            
            audioOutput.playAudio('stepsRemaining')
            audioOutput.playInt(str(int(stepsRemainingToNextNode)))
            
            # give the number of stairs expected, if any
            if navigator.route[navigator.clearedRouteIdx] == 2214:
                print(stringHelper.AUDIO + ' Number of stairs expected: 12')
                audioOutput.playAudio('numberOfStairsExpected')
                audioOutput.playInt(12)
            elif navigator.route[navigator.clearedRouteIdx] == 2311:
                print(stringHelper.AUDIO + ' Number of stairs expected: 12')
                audioOutput.playAudio('numberOfStairsExpected')
                audioOutput.playInt(12)
            elif navigator.route[navigator.clearedRouteIdx] == 1230:
                print(stringHelper.AUDIO + ' Number of stairs expected: 10, 5, 9')
                audioOutput.playAudio('numberOfStairsExpected')
                audioOutput.playInt(10)
                audioOutput.playAudio('then')
                audioOutput.playInt(5)
                audioOutput.playAudio('then')
                audioOutput.playInt(9)
        
        # if the user input is '0', toggle on/off steps counting
        if userInput == '0':
            isNavigationPaused = not isNavigationPaused
        
        sleep(1.5)
        
        # ======================================== END NAVIGATION ========================================
        
    keypadInput.closeKeypadThread()
    audioOutput.closeAudioThread()

if __name__ == '__main__':
    main()
