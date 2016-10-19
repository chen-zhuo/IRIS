'''
This file contains algorithms related to keypad input. The user can enter keypad input to IRIS. A keypad command ends
with a '#' key. A keypad command is cleared with a '*' key.

@author: chen-zhuo
'''

from Keypad import Keypad
import stringHelper
from threading import Thread
from time import sleep
import audioOutput

myKeypad = Keypad()
prevKeyPressed = ''
tempUserInput = '' # stores key presses before the user confirms with a '#' key
userInputs = [] # stores a list of confirmed user inputs with the ending '#' keys
isKeypadThreadActive = False

'''
Starts `readKeypadInputThread`.
'''
def initKeypad():
    readKeypadInputThread = Thread(target = _readKeypadInput)
    readKeypadInputThread.start()

'''
Wait for the next key press, and then return it.
'''
def waitAndGetKeyPress():
    userInput = None
    while userInput == None:
        userInput = _getKeyPress()
    return userInput

def waitAndGetKeyPressesUntilHashKey():
    userInput = None
    while userInput == None:
        userInput = _getKeyPressesUntilHashKey()
    return userInput

def waitAndGetKeyPressesUntilHashKeyWithConfirmationDialog(promptAudioName):
    userInput = ''
    while True:
        print(stringHelper.AUDIO + ' ' + audioOutput.audioTextDict[promptAudioName])
        audioOutput.playAudio(promptAudioName)
        
        userInput = waitAndGetKeyPressesUntilHashKey()
        print(stringHelper.AUDIO + ' You have keyed in: ' + userInput)
        audioOutput.playAudio('youHaveKeyedIn')
        audioOutput.playNum(userInput)
        
        print(stringHelper.AUDIO + ' Press the hash key to confirm, or asterisk key to re-enter.')
        audioOutput.playAudio('pressTheHashKeyToConfirmOrAsteriskKeyToReenter')
        
        isUserInputConfirmed = None
        while isUserInputConfirmed != '*' and isUserInputConfirmed != '#':
            isUserInputConfirmed = _getKeyPress()
        if isUserInputConfirmed == '#':
            print(stringHelper.AUDIO + ' Comfirmed.')
            audioOutput.playAudio('confirmed')
            break
        else: # if isUserInputConfirmed == '*'
            continue
    return userInput

'''
Closes `readKeypadInputThread`.
'''
def closeKeypadThread():
    global isKeypadThreadActive
    isKeypadThreadActive = False

'''
Defines `readKeypadInputThread` which is started by `initKeypad()`.
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
                audioOutput.playAudioNow(keyPressed)
                tempUserInput += keyPressed
            elif keyPressed == '*':
                tempUserInput = ''
            elif keyPressed == '#':
                userInputs.append(tempUserInput)
                tempUserInput = ''
            prevKeyPressed = keyPressed
    
    print(stringHelper.MESSAGE + ' `readKeypadInputThread` closed.')

def _getKeyPress():
    global prevKeyPressed, tempUserInput, userInputs
    prevKeyPressed = None
    
    while True:
        if (prevKeyPressed != None):
            break;
    
    if prevKeyPressed == '#':
        userInputs.pop(0)
    else:
        tempUserInput = ''
    
    return prevKeyPressed

def _getKeyPressesUntilHashKey():
    global userInputs
    
    if len(userInputs) > 0:
        nextUserInput = userInputs[0]
        userInputs.pop(0)
        return nextUserInput
    else:
        return None

def _test():
    global userInputs
    
    initKeypad()
    while True:
        print('Waiting for user input...')
        userInput = None
        while userInput == None:
            userInput = _getKeyPressesUntilHashKey()
        
        print('You have keyed in: ' + userInput)
        print('Press the hash key to confirm, or asterisk key to re-enter.')
        isUserInputConfirmed = None
        while isUserInputConfirmed != '*' and isUserInputConfirmed != '#':
            isUserInputConfirmed = _getKeyPress()
        if isUserInputConfirmed == '#':
            print('Comfirmed user input: ' + userInput)
            break
        else:
            continue
    closeKeypadThread()

if __name__ == '__main__':
    _test()
