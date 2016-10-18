'''
This file contains algorithms related to Hamming(8,4) encoding.

@author: chen-zhuo
'''

import stringHelper

'''
Encodes a bytestream using Hamming(8,4) encoding. The length of resultant bytestream will be doubled after encoding.

@param bytestream
           a `bytes` object representing the bytestream
@return a `bytes` object representing the encoded bytestream
'''
def encode(bytestream):
    encodedBytestream = ''.encode('utf_8')
    for i in range(0, len(bytestream)):
        # data bits in original byte
        d1 = (bytestream[i] >> 7) & 1 # most significant bit
        d2 = (bytestream[i] >> 6) & 1
        d3 = (bytestream[i] >> 5) & 1
        d4 = (bytestream[i] >> 4) & 1
        d5 = (bytestream[i] >> 3) & 1
        d6 = (bytestream[i] >> 2) & 1
        d7 = (bytestream[i] >> 1) & 1
        d8 = (bytestream[i] >> 0) & 1 # least significant bit
        
        # parity bits to be appended
        p1 = (d1 + d3 + d4) % 2
        p2 = (d1 + d2 + d4) % 2
        p3 = (d1 + d2 + d3) % 2
        p4 = (d1 + d2 + d3 + d4 + p1 + p2 + p3) % 2
        p5 = (d5 + d7 + d8) % 2
        p6 = (d5 + d6 + d8) % 2
        p7 = (d5 + d6 + d7) % 2
        p8 = (d5 + d6 + d7 + d8 + p5 + p6 + p7) % 2
        
        # original data byte is divided into two bytes with appended parity bits
        byte1 = bytes([
                    d1*(2**7) + d2*(2**6) + d3*(2**5) + d4*(2**4) + p1*(2**3) + p2*(2**2) + p3*(2**1) + p4*(2**0)
                ])
        byte2 = bytes([
                    d5*(2**7) + d6*(2**6) + d7*(2**5) + d8*(2**4) + p5*(2**3) + p6*(2**2) + p7*(2**1) + p8*(2**0)
                ])
        
        encodedBytestream += byte1
        encodedBytestream += byte2
    return encodedBytestream

'''
Decodes a bytestream using Hamming(8,4) encoding. Assumes that there are at most 2 errors per byte. Attempts to
correct 1-bit errors (in each byte). Returns None if a 2-bit error (in one byte) is detected. The decoding may be
wrong if there are 3-bit errors (or higher).

@param bytestream
           a `bytes` object representing the encoded bytestream
@return a `bytes` object representing the decoded bytestream; return None if error
'''
def decode(bytestream):
    if len(bytestream) % 2 != 0:
        print(stringHelper.ERROR + ' at hammingCode.decode(): The length of bytestream is odd.')
        return None
    
    decodedBytestream = ''.encode('utf_8')
    
    for i in range(0, len(bytestream), 2):
        # data bits
        d1 = (bytestream[i] >> 7) & 1 # most significant bit
        d2 = (bytestream[i] >> 6) & 1
        d3 = (bytestream[i] >> 5) & 1
        d4 = (bytestream[i] >> 4) & 1
        d5 = (bytestream[i + 1] >> 7) & 1
        d6 = (bytestream[i + 1] >> 6) & 1
        d7 = (bytestream[i + 1] >> 5) & 1
        d8 = (bytestream[i + 1] >> 4) & 1 # least significant bit
        
        # parity bits
        p1 = (bytestream[i] >> 3) & 1
        p2 = (bytestream[i] >> 2) & 1
        p3 = (bytestream[i] >> 1) & 1
        p4 = (bytestream[i] >> 0) & 1
        p5 = (bytestream[i + 1] >> 3) & 1
        p6 = (bytestream[i + 1] >> 2) & 1
        p7 = (bytestream[i + 1] >> 1) & 1
        p8 = (bytestream[i + 1] >> 0) & 1
        
        # to verify parity bits
        circle1 = p1 == (d1 + d3 + d4) % 2
        circle2 = p2 == (d1 + d2 + d4) % 2
        circle3 = p3 == (d1 + d2 + d3) % 2
        circle4 = p4 == (d1 + d2 + d3 + d4 + p1 + p2 + p3) % 2
        circle5 = p5 == (d5 + d7 + d8) % 2
        circle6 = p6 == (d5 + d6 + d8) % 2
        circle7 = p7 == (d5 + d6 + d7) % 2
        circle8 = p8 == (d5 + d6 + d7 + d8 + p5 + p6 + p7) % 2
        
        decodedByte = 0b00000000
        
        if circle1 and circle2 and circle3 and circle4:
            decodedByte += d1*(2**7) + d2*(2**6) + d3*(2**5) + d4*(2**4) # no error
        elif not circle1 and not circle2 and not circle3 and not circle4:
            decodedByte += ((d1 + 1) % 2)*(2**7) + d2*(2**6) + d3*(2**5) + d4*(2**4) # error correction on `d1`
        elif circle1 and not circle2 and not circle3 and not circle4:
            decodedByte += d1*(2**7) + ((d2 + 1) % 2)*(2**6) + d3*(2**5) + d4*(2**4) # error correction on `d2`
        elif not circle1 and circle2 and not circle3 and not circle4:
            decodedByte += d1*(2**7) + d2*(2**6) + ((d3 + 1) % 2)*(2**5) + d4*(2**4) # error correction on `d3`
        elif not circle1 and not circle2 and circle3 and not circle4:
            decodedByte += d1*(2**7) + d2*(2**6) + d3*(2**5) + ((d4 + 1) % 2)*(2**4) # error correction on `d4`
        elif not circle1 and circle2 and circle3 and not circle4:
            decodedByte += d1*(2**7) + d2*(2**6) + d3*(2**5) + d4*(2**4) # error on `p1`
        elif circle1 and not circle2 and circle3 and not circle4:
            decodedByte += d1*(2**7) + d2*(2**6) + d3*(2**5) + d4*(2**4) # error on `p2`
        elif circle1 and circle2 and not circle3 and not circle4:
            decodedByte += d1*(2**7) + d2*(2**6) + d3*(2**5) + d4*(2**4) # error on `p3`
        elif circle1 and circle2 and circle3 and not circle4:
            decodedByte += d1*(2**7) + d2*(2**6) + d3*(2**5) + d4*(2**4) # error on `p4`
        else:
            print(stringHelper.WARNING + ' at hammingCode.decode(): The encoded bytestream is erroneous.')
            return None
        
        if circle5 and circle6 and circle7 and circle8:
            decodedByte += d5*(2**3) + d6*(2**2) + d7*(2**1) + d8*(2**0) # no error
        elif not circle5 and not circle6 and not circle7 and not circle8:
            decodedByte += ((d5 + 1) % 2)*(2**3) + d6*(2**2) + d7*(2**1) + d8*(2**0) # error correction on `d5`
        elif circle5 and not circle6 and not circle7 and not circle8:
            decodedByte += d5*(2**3) + ((d6 + 1) % 2)*(2**2) + d7*(2**1) + d8*(2**0) # error correction on `d6`
        elif not circle5 and circle6 and not circle7 and not circle8:
            decodedByte += d5*(2**3) + d6*(2**2) + ((d7 + 1) % 2)*(2**1) + d8*(2**0) # error correction on `d7`
        elif not circle5 and not circle6 and circle7 and not circle8:
            decodedByte += d5*(2**3) + d6*(2**2) + d7*(2**1) + ((d8 + 1) % 2)*(2**0) # error correction on `d8`
        elif not circle5 and circle6 and circle7 and not circle8:
            decodedByte += d5*(2**3) + d6*(2**2) + d7*(2**1) + d8*(2**0) # error on `p5`
        elif circle5 and not circle6 and circle7 and not circle8:
            decodedByte += d5*(2**3) + d6*(2**2) + d7*(2**1) + d8*(2**0) # error on `p6`
        elif circle5 and circle6 and not circle7 and not circle8:
            decodedByte += d5*(2**3) + d6*(2**2) + d7*(2**1) + d8*(2**0) # error on `p7`
        elif circle5 and circle6 and circle7 and not circle8:
            decodedByte += d5*(2**3) + d6*(2**2) + d7*(2**1) + d8*(2**0) # error on `p8`
        else:
            print(stringHelper.WARNING + ' at hammingCode.decode(): The encoded bytestream is erroneous.')
            return None
        decodedBytestream += bytes([decodedByte])
    return decodedBytestream

def test():
    originalByte = 0b11000011
    print('Original byte:         ' + format(originalByte, '08b'))
    expectedEncodedByte = encode(bytes([originalByte]))
    print('Expected encoded byte:', end='')
    for i in range(0, len(expectedEncodedByte)):
        print(' ' + format(expectedEncodedByte[i], '08b'), end='')
    print('')
    
    print('\n================== TEST CASE 1: NO ERROR ==================\n')
    
    actualEncodedByte = bytes([0b11001001, 0b00110110])
    print('Actual encoded byte:  ', end='')
    for i in range(0, len(actualEncodedByte)):
        print(' ' + format(actualEncodedByte[i], '08b'), end='')
    print('')
    
    testDecode(actualEncodedByte)
    
    print('\n============ TEST CASE 2: 1-BIT ERROR PER BYTE =============\n')
    
    actualEncodedByte = bytes([0b01001001, 0b10110110])
    print('Actual encoded byte:  ', end='')
    for i in range(0, len(actualEncodedByte)):
        print(' ' + format(actualEncodedByte[i], '08b'), end='')
    print('')
    
    testDecode(actualEncodedByte)
    
    print('\n============ TEST CASE 3: 2-BIT ERROR PER BYTE =============\n')
    
    actualEncodedByte = bytes([0b00001001, 0b11110110])
    print('Actual encoded byte:  ', end='')
    for i in range(0, len(actualEncodedByte)):
        print(' ' + format(actualEncodedByte[i], '08b'), end='')
    print('')
    
    testDecode(actualEncodedByte)

def testDecode(encodedByte):
    decodedByte = decode(encodedByte)
    if decodedByte == None:
        print('Decoded byte:          ERROR')
    else:
        for i in range(0, len(decodedByte)):
            print('Decoded byte:          ' + format(decodedByte[i], '08b'))

if __name__ == '__main__':
    test()
