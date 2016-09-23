'''


@author: chen-zhuo
'''

import RPi.GPIO as GPIO # @UnresolvedImport

class Keypad():
    
    KEY_VALUES = [[1, 2, 3], [4, 5, 6], [7, 8, 9], ['*', 0, '#']]
    ROW = [7, 8, 25, 24]
    COLUMN = [11, 9, 10]
    
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
    
    def getKey(self):
        # set all columns as output low
        for j in range(len(self.COLUMN)):
            GPIO.setup(self.COLUMN[j], GPIO.OUT)
            GPIO.output(self.COLUMN[j], GPIO.LOW)
        
        # set all rows as input
        for i in range(len(self.ROW)):
            GPIO.setup(self.ROW[i], GPIO.IN, pull_up_down = GPIO.PUD_UP)
        
        # scan rows for pushed key; a valid key press should set "rowVal"  between 0 and 3
        rowVal = -1
        for i in range(len(self.ROW)):
            tmpRead = GPIO.input(self.ROW[i])
            if tmpRead == 0:
                rowVal = i
        
        # if 'rowVal' is not 0 thru 3 then no button was pressed and we can exit
        if rowVal < 0 or rowVal > 3:
            self.exit()
            return
        
        # convert columns to input
        for j in range(len(self.COLUMN)):
            GPIO.setup(self.COLUMN[j], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        
        # switch the 'i'-th row found from scan to output
        GPIO.setup(self.ROW[rowVal], GPIO.OUT)
        GPIO.output(self.ROW[rowVal], GPIO.HIGH)
        
        # scan columns for still-pushed key; a valid key press should set 'colVal' between 0 and 2
        colVal = -1
        for j in range(len(self.COLUMN)):
            tmpRead = GPIO.input(self.COLUMN[j])
            if tmpRead == 1:
                colVal = j
        
        # if 'colVal' is not 0 thru 2 then no button was pressed and we can exit
        if colVal < 0 or colVal > 2:
            self.exit()
            return
        
        # return the value of the key pressed
        self.exit()
        return self.KEY_VALUES[rowVal][colVal]
    
    def exit(self):
        # Reinitialize all rows and columns as input at exit
        for i in range(len(self.ROW)):
            GPIO.setup(self.ROW[i], GPIO.IN, pull_up_down=GPIO.PUD_UP) 
        for j in range(len(self.COLUMN)):
            GPIO.setup(self.COLUMN[j], GPIO.IN, pull_up_down=GPIO.PUD_UP)
    

def testKeypad():
    myKeypad = Keypad()
    
    digit = None
    while (digit == None):
        digit = myKeypad.getKey()
    print(digit)

if __name__ == '__main__':
    testKeypad()
