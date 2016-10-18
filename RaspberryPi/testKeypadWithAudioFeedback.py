'''
This is a unit-test file for keypad with audio feedback.

@author: chen-zhuo
'''

import algorithms
import audioOutput
import keypadInput
from time import sleep

def _test():
    keypadInput.initKeypad()
    audioOutput.initAudio()
    
    audioOutput.playAudio('welcomeToIris')
    sleep(1)
    
    while True:
        audioOutput.playAudio('plsKeyInDestinationNodeIdFollowedByTheHashKey')
        
        userInput = None
        while userInput == None:
            userInput = keypadInput.getKeyPressesUntilHashKey()
        
        print('You have keyed in: ' + userInput)
        audioOutput.playAudio('youHaveKeyedIn')
        audioOutput.playNum(userInput)
        
        print('Press the hash key to confirm, or the asterisk key to re-enter.')
        audioOutput.playAudio('pressTheHashKeyToConfirmOrAsteriskKeyToReenter')
        
        isUserInputConfirmed = None
        while isUserInputConfirmed != '*' and isUserInputConfirmed != '#':
            isUserInputConfirmed = keypadInput.getKeyPress()
        if isUserInputConfirmed == '#':
            print('Comfirmed.')
            audioOutput.playAudio('confirmed')
            break
        else: # if isUserInputConfirmed == '*'
            continue
    
    keypadInput.closeKeypadThread()
    audioOutput.closeAudioThread()

if __name__ == '__main__':
    _test()
