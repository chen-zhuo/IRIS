'''
This file contains functions for string processing.

@author: chen-zhuo
'''

MESSAGE = '\x1b[1;30;47m' + ' MESSAGE ' + '\x1b[0m'
WARNING = '\x1b[1;30;43m' + ' WARNING ' + '\x1b[0m'
ERROR   = '\x1b[1;37;41m' + '  ERROR  ' + '\x1b[0m'
AUDIO   = '\x1b[1;32;44m' + '  AUDIO  ' + '\x1b[0m'
INFO    = '\x1b[1;30;46m' + '  INFO   ' + '\x1b[0m'

def highlight(string):
    result = '\x1b[7m '
    result += str(string)
    result += ' \x1b[0m'
    return result

def test():
    print(MESSAGE)
    print(WARNING)
    print(ERROR)
    print(AUDIO)
    print(INFO)

if __name__ == '__main__':
    test()
