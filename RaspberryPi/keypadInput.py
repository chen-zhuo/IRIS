'''
This file contains algorithms related to keypad input. The user can enter keypad input to IRIS. A keypad command ends
with a '#' key. A keypad command is cleared with a '*' key.

@author: chen-zhuo
'''

import Keypad
import stringHelper
from threading import Thread

tempUserInput = [] # stores key presses before the user confirms with a '#' key
userInputs = [] # stores a list of confirmed user inputs with the ending '#' keys
isKeypadThreadActive = False

'''
Starts `readKeypadInputThread`.
'''
def initKeypadThread():
    tempUserInput = []
    readKeypadInputThread = Thread(target = _readKeypadInput)
    readKeypadInputThread.start()

'''
Defines `readKeypadInputThread` which is started by `initKeypadThread()`.
'''
def _readKeypadInput():
    print(stringHelper.MESSAGE + ' `readKeypadInputThread` started.')
    
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

'''
Closes `readKeypadInputThread`.
'''
def closeKeypadThread():
    global isKeypadThreadActive
    isKeypadThreadActive = False
    print(stringHelper.MESSAGE + ' `readKeypadInputThread` is closed.')

def getUserInput():
    if len(userInputs) > 0:
        nextUserInput = userInputs[0]
        userInputs.pop(0)
        return nextUserInput

def _test():
    initKeypadThread()
    while True:
        userInput = None
        while userInput == None:
            userInput = getUserInput()
        
        print('You have keyed in: ' + userInput)
        print('Press the hash key to confirm, or asterisk key to re-enter.')
        isUserInputConfirmed = None
        while isUserInputConfirmed == None:
            isUserInputConfirmed = getUserInput()
        
        if isUserInputConfirmed == '#':
            print('Comfirmed user input: ' + userInput)
        else:
            continue
    closeKeypadThread()

if __name__ == '__main__':
    _test()
