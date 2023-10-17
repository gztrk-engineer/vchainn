from backend.util.hex2bin import hexToBinary

def testHexToBinary():
    originalNumber = 789
    hexNumber = hex(originalNumber)[2:]
    binaryNumber = hexToBinary(hexNumber)

    assert int(binaryNumber, 2) == originalNumber