'''
This is a unit-test file for keypad with audio feedback.

@author: chen-zhuo
'''

import algorithms
import audioOutput
import keypadInput
import stringHelper
from time import sleep

def _test():
    keypadInput.initKeypad()
    audioOutput.initAudio()
    
    print(stringHelper.AUDIO + ' Welcome to IRIS.')
    audioOutput.playAudio('welcomeToIris')
    sleep(1)
    
    while True:
        print(stringHelper.AUDIO + ' Please key in destination node ID, followed by the hash key.')
        audioOutput.playAudio('plsKeyInDestinationNodeIdFollowedByTheHashKey')
        
        userInput = None
        while userInput == None:
            userInput = keypadInput._getKeyPressesUntilHashKey()
        
        print(stringHelper.AUDIO + ' You have keyed in: ' + userInput)
        audioOutput.playAudio('youHaveKeyedIn')
        audioOutput.playNum(userInput)
        
        print(stringHelper.AUDIO + ' Press the hash key to confirm, or asterisk key to re-enter.')
        audioOutput.playAudio('pressTheHashKeyToConfirmOrAsteriskKeyToReenter')
        
        isUserInputConfirmed = None
        while isUserInputConfirmed != '*' and isUserInputConfirmed != '#':
            isUserInputConfirmed = keypadInput._getKeyPress()
        if isUserInputConfirmed == '#':
            print(stringHelper.AUDIO + ' Comfirmed.')
            audioOutput.playAudio('confirmed')
            break
        else: # if isUserInputConfirmed == '*'
            continue
    
    keypadInput.closeKeypadThread()
    audioOutput.closeAudioThread()

if __name__ == '__main__':
    _test()
