'''
This file contains algorithms related to keypad input. The user can enter keypad input to IRIS. A keypad command ends
with a '#' key. A keypad command is cleared with a '*' key.

@author: chen-zhuo
'''

import audioOutput
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
def initKeypad():
    readKeypadInputThread = Thread(target = _readKeypadInput)
    readKeypadInputThread.start()

'''
Wait for the next key press, and then return it.
'''
# def waitAndGetKeyPress():
#     userInput = None
#     while userInput == None:
#         userInput = _getKeyPress()
#     return userInput

'''
Wait for the next keypad input, and then return it. A keypad input is a sequence of key presses, ending with '#'. '*' is
treated as "clear".
'''
def waitAndGetKeypadInput():
    userInput = None
    while userInput == None:
        userInput = _getKeyPressesUntilHashKey()
    return userInput

def waitAndGetKeypadInputWithAudioPrompt(promptAudioName):
    userInput = ''
    while True:
        print(stringHelper.AUDIO + ' ' + audioOutput.audioTextDict[promptAudioName])
        audioOutput.playAudio(promptAudioName)
        
        userInput = waitAndGetKeypadInput()
        print(stringHelper.AUDIO + ' You have keyed in: ' + userInput)
        audioOutput.playAudio('youHaveKeyedIn')
        audioOutput.playInt(userInput)
        
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

def getKeypadInput():
    global userInputs
    
    if len(userInputs) > 0:
        userInput = userInputs[0]
        userInputs.pop(0)
        return userInput
    else:
        return None

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
    initKeypad()
    audioOutput.initAudio()
    
    print(stringHelper.AUDIO + ' Welcome to IRIS.')
    audioOutput.playAudio('welcomeToIris')
    sleep(1)
    
    destNodeId = waitAndGetKeypadInputWithAudioPrompt(
        'plsKeyInDestinationNodeIdFollowedByTheHashKey')
    print(stringHelper.INFO + ' destNodeId = ' + destNodeId)
    
    closeKeypadThread()
    audioOutput.closeAudioThread()

if __name__ == '__main__':
    _test()
