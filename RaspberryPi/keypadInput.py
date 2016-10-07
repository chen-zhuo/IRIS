'''
This file contains algorithms related to keypad input. The user can enter keypad input to IRIS. A keypad command ends
with a '#' key. A keypad command is cleared with a '*' key.

@author: chen-zhuo
'''

from threading import Thread

import Keypad

tempUserInput = [] # stores key presses before the user confirms with a '#' key
userInputs = [] # stores a list of confirmed user inputs with the ending '#' keys
isKeypadThreadActive = False

'''
Starts 'readKeypadInputThread'.
'''
def initKeypadThread():
    tempUserInput = []
    readKeypadInputThread = Thread(target = readKeypadInput)
    readKeypadInputThread.start()

'''
Defines 'readKeypadInputThread' which is started by 'initKeypadThread()'.
'''
def readKeypadInput():
    print('\'readKeypadInputThread\' is starting...')
    
    global isKeypadThreadActive, tempUserInput
    
    myKeypad = Keypad()
    while isKeypadThreadActive:
        keyPressed = myKeypad.getKey()
        if keyPressed != '*' and keyPressed != '#':
            tempUserInput.append(keyPressed)
        elif keyPressed == '*':
            tempUserInput = []
        else:
            userInputs.append(tempUserInput)
            tempUserInput = []
    
    print('\'readKeypadInputThread\' is closing...')

'''
Closes 'readKeypadInputThread'.
'''
def closeKeypadThread():
    global isKeypadThreadActive
    isKeypadThreadActive = False

def getUserInput():
    if len(userInputs) > 0:
        nextUserInput = userInputs[0]
        userInputs.pop(0)
        return nextUserInput

def testKeypadInput():
    initKeypadThread()
    while True:
        input = readKeypadInput()
    closeKeypadThread()

if __name__ == '__main__':
    testKeypadInput()
