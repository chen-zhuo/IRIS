'''
This file is for use in Week 7 for the first prototype demo (software subsystem).

@author: chen-zhuo
'''

import algorithms
from Navigator import Navigator

def demo():
    printWelcomeMsg()
    
    while True:
        print('\n================= MAIN MENU =================\n')
        buildingId = int(input('Please enter building ID: '))
        buildingName = algorithms.buildingDict[buildingId]
        buildingStorey = int(input('Please enter building storey: '))
        myMap = algorithms.downloadAndParseMap(buildingId, buildingName, buildingStorey)
        print('Please enter an option:\n    1. Path Finding\n    2. Giving Direction (cumulative)\n    3. Quit Test')
        testType = input()
        
        if testType == '1':
            while True:
                print('\n=============== NEW TEST CASE ===============\n')
                srcNodeId = int(input('Please enter origin node ID (enter \'0\' to return to the main menu): '))
                if srcNodeId == 0:
                    break
                
                destNodeId = int(input('Please enter destination node ID (enter \'0\' to return to the main menu): '))
                if destNodeId == 0:
                    break
                
                result = algorithms.computeRoute(myMap, srcNodeId, destNodeId)
                for i in range(len(result) - 1):
                    print(str(result[i]) + ' -> ', end = "")
                print(result[len(result) - 1])
        elif testType == '2':
            srcNodeId = int(input('Please enter origin node ID: '))
            destNodeId = int(input('Please enter destination node ID: '))
            currentX = int(input('Please enter the x-coordinate of current location: '))
            currentY = int(input('Please enter the y-coordinate of current location: '))
            currentBearing = int(input('Please enter the bearing (w.r.t. geographical north) of current location: '))
            route = algorithms.computeRoute(myMap, srcNodeId, destNodeId)
            navigator = Navigator(myMap, route, currentX, currentY, currentBearing, 50)
            
            while True:
                print('\n=============== NEW TEST CASE ===============\n')
                currentX = int(input('Please enter the x-coordinate of current location: '))
                currentY = int(input('Please enter the y-coordinate of current location: '))
                currentBearing = int(input('Please enter the bearing (w.r.t. geographical north) of current location: '))
                
                navigator.update(currentX, currentY, currentBearing)
                if navigator.clearedRouteIdx == len(navigator.route) - 1:
                    print('You have reached the destination node.')
                    break
                naviInfo = navigator.getNaviInfo()
                print('Next node ID is ' + str(navigator.route[navigator.clearedRouteIdx + 1]) + '.')
                print('Distance from next node is ' + str(naviInfo[0]) + ' centimeters.')
                bearing = (naviInfo[1] - (currentBearing + myMap.northAt) % 360 + 360) % 360
                print('Bearing of next node from current location is ' + str(bearing) + ' degrees.')
        else:
            break
    return

'''
Prints welcome message.
'''
def printWelcomeMsg():
    print('\n================================================================================\n')
    print('Welcome to IRIS.\n')
    print('IRIS (Indoor Route Instruction System) is a wearable device to provide')
    print('in-building navigation guidance for a visually-impaired person.\n')
    print('Week 7 First Prototype Demo - Software Subsystem\n')
    print('================================================================================\n')

if __name__ == '__main__':
    demo()
