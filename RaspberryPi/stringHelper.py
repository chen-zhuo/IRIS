'''
This file contains functions for string processing.

@author: chen-zhuo
'''

MESSAGE = '\x1b[1;30;47m' + ' MESSAGE ' + '\x1b[0m';
WARNING = '\x1b[1;30;43m' + ' WARNING ' + '\x1b[0m'
ERROR   = '\x1b[1;37;41m' + '  ERROR  ' + '\x1b[0m'

def test():
    print(MESSAGE)
    print(WARNING)
    print(ERROR)

if __name__ == '__main__':
    test()
