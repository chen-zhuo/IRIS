'''
This file contains algorithms related to keypad input. The user can enter keypad input to IRIS. A keypad command ends
with a '#' key. A keypad command is cleared with a '*' key.

@author: chen-zhuo
'''

from Keypad import Keypad
import stringHelper
from threading import Thread
from time import sleep

myKeypad = Keypad()
prevKeyPressed = ''
tempUserInput = '' # stores key presses before the user confirms with a '#' key
userInputs = [] # stores a list of confirmed user inputs with the ending '#' keys
isKeypadThreadActive = False

'''
Starts `readKeypadInputThread`.
'''
def initKeypadThread():
    readKeypadInputThread = Thread(target = _readKeypadInput)
    readKeypadInputThread.start()

'''
Defines `readKeypadInputThread` which is started by `initKeypadThread()`.
'''
def _readKeypadInput():
    print(stringHelper.MESSAGE + ' `readKeypadInputThread` started.')
    
    global isKeypadThreadActive, prevKeyPressed, tempUserInput, userInputs
    isKeypadThreadActive = True
    
    tempUserInput = ''
    while isKeypadThreadActive:
        keyPressed = myKeypad.getKey()
        if keyPressed != None:
            if keyPressed != None and keyPressed != '*' and keyPressed != '#':
                tempUserInput += keyPressed
            elif keyPressed == '*':
                tempUserInput = ''
            elif keyPressed == '#':
                userInputs.append(tempUserInput)
                tempUserInput = ''
            prevKeyPressed = keyPressed
    
    print(stringHelper.MESSAGE + ' `readKeypadInputThread` is closed.')

'''
Closes `readKeypadInputThread`.
'''
def closeKeypadThread():
    global isKeypadThreadActive
    isKeypadThreadActive = False

'''
Wait for the next key press, and then return it.
'''
def getKeyPress():
    global prevKeyPressed
    prevKeyPressed = None
    
    while True:
        if (prevKeyPressed != None):
            break;
    return prevKeyPressed

def getKeyPressesUntilHashKey():
    global userInputs
    
    if len(userInputs) > 0:
        nextUserInput = userInputs[0]
        userInputs.pop(0)
        return nextUserInput
    else:
        return None

def _test():
    global userInputs
    
    initKeypadThread()
    while True:
        print('Waiting for user input...')
        userInput = None
        while userInput == None:
            userInput = getKeyPressesUntilHashKey()
        
        print('You have keyed in: ' + userInput)
        print('Press the hash key to confirm, or asterisk key to re-enter.')
        isUserInputConfirmed = None
        while isUserInputConfirmed != '*' and isUserInputConfirmed != '#':
            isUserInputConfirmed = getKeyPress()
        if isUserInputConfirmed == '#':
            print('Comfirmed user input: ' + userInput)
            break
        else:
            continue
    closeKeypadThread()

if __name__ == '__main__':
    _test()
