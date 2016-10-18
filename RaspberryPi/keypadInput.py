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
tempUserInput = '' # stores key presses before the user confirms with a '#' key
userInputs = [] # stores a list of confirmed user inputs with the ending '#' keys
isKeypadThreadActive = False

'''
Starts `readKeypadInputThread`.
'''
def initKeypadThread():
    global isKeypadThreadActive, tempUserInput
    
    tempUserInput = ''
    readKeypadInputThread = Thread(target = _readKeypadInput)
    readKeypadInputThread.start()

'''
Defines `readKeypadInputThread` which is started by `initKeypadThread()`.
'''
def _readKeypadInput():
    print(stringHelper.MESSAGE + ' `readKeypadInputThread` started.')
    
    global isKeypadThreadActive, tempUserInput, userInputs
    isKeypadThreadActive = True
    
    while isKeypadThreadActive:
        keyPressed = myKeypad.getKey()
        if keyPressed != None and keyPressed != '*' and keyPressed != '#':
            tempUserInput += keyPressed
        elif keyPressed == '*':
            tempUserInput = []
        elif keyPressed == '#':
            userInputs.append(tempUserInput)
            tempUserInput = []
    
    print(stringHelper.MESSAGE + ' `readKeypadInputThread` is closed.')

'''
Closes `readKeypadInputThread`.
'''
def closeKeypadThread():
    global isKeypadThreadActive
    isKeypadThreadActive = False

def getUserInput():
    global userInputs
    
    if len(userInputs) > 0:
        nextUserInput = userInputs[0]
        userInputs.pop(0)
        return nextUserInput
    else:
        return None

def _test():
    global tempUserInput, userInputs
    
    initKeypadThread()
    while True:
        userInput = None
        while userInput == None:
            userInput = getUserInput()
            print('tempUserInput = ' + tempUserInput)
            print('userInputs = ' + userInputs)
            sleep(3)
        
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
