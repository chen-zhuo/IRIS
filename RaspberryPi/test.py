from PiMegaCommunicator import PiMegaCommunicator

commumicator = PiMegaCommunicator()

encodedByte = commumicator.encode(bytes([0b11000011]))

print('Encoded byte:')
for i in range(0, len(encodedByte)):
    print('    ' + bin(encodedByte[i]))

decodedByte = commumicator.decode([0b00001001, 0b00110111])

for i in range(0, len(decodedByte)):
    print('Decoded byte: ' + bin(decodedByte[i]))






# encodedBytestream = bytes([251, 0])
# print(int.from_bytes(encodedBytestream, byteorder='big', signed=False))