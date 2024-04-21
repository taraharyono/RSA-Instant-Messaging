from primePy import primes
import math
import random

def generateKey(p, q):
    if primes.check(p) and primes.check(q):
        n = p * q
        phi = (p-1) * (q-1)
        e = chooseE(phi)
        d = pow(e, -1, phi)
        
        return [e, d, n]


def chooseE(phi):
    while (True):
        e = random.randrange(2, phi)

        if (math.gcd(e, phi) == 1):
            return e
        

def StringToByteIntArray(string):
    byteint_array = []
    for char in string:
        byteint_array.append(ord(char))
    
    return byteint_array


def ByteIntArrayToBlocks(byteint_array, size):
    if (size == 1):
        return byteint_array
    else:
        blocked_byteintarray = []
        i = 0
        while (i < len(byteint_array)):
            block = ""

            for j in range(size):
                if ((i+j) < len(byteint_array)):
                    if (byteint_array[i+j]<10):
                        block += "00" + str(byteint_array[i+j])
                    elif (byteint_array[i+j] < 100):
                        block += "0" + str(byteint_array[i+j])
                    else:
                        block += str(byteint_array[i+j])
                else:
                    block += str(ord('\0'))
        
            i += size
            blocked_byteintarray.append(int(block))
        return blocked_byteintarray


def CiphertextToBlock(ciphertext, n):
    ciphertext_string = str(ciphertext)
    block_size = math.ceil(math.log(n, 16))

    ciphertext_block = []

    i = 0
    while (i < len(ciphertext_string)):
        block = ""
        for j in range(block_size):
            if ((i+j) < len(ciphertext_string)):
                block += ciphertext_string[i+j]
            else:
                block += "0"
        
        i += block_size
        ciphertext_block.append(int(block, 16))
    
    return ciphertext_block


def CiphertextBlockSize(n):
    size = math.log(n, 16)
    return (int(size)+1)


def encrypt(plaintext, e, n, block_size, is_file):
    if not is_file:
        plaintext_byteintarray = StringToByteIntArray(plaintext)
        plaintext_blocks = ByteIntArrayToBlocks(plaintext_byteintarray, block_size)
    else:
        plaintext_blocks = ByteIntArrayToBlocks(plaintext, block_size)

    ciphertext_blocksize = CiphertextBlockSize(n)
    print(ciphertext_blocksize)

    ciphertext_hexstr = ""

    for block in plaintext_blocks:
        cipher_block = (block**e)%n

        cipher_hex = str(hex(cipher_block))[2:].upper()

        if (len(cipher_hex) < ciphertext_blocksize):
            leading_zero = "0" * (ciphertext_blocksize - len(cipher_hex))
            cipher_hex = leading_zero + cipher_hex

        ciphertext_hexstr += cipher_hex
    return ciphertext_hexstr


def decrypt(ciphertext, d, n):
    """Ciphertext in hexstring"""
    ciphertext_blocks = CiphertextToBlock(ciphertext, n)

    plaintext_byteintarray = []
    for block in ciphertext_blocks:
        plaintext_block = (block**d)%n

        plaintext_blockstr = str(plaintext_block)

        if (len(plaintext_blockstr) % 3 != 0):
            leading_zero = "0" * (3 - len(plaintext_blockstr) % 3)
            plaintext_blockstr = leading_zero + plaintext_blockstr

        i = 0
        while (i < len(plaintext_blockstr)):
            num = plaintext_blockstr[i:i+3]
            plaintext_byteintarray.append(int(num))
            i += 3
    result = bytes(plaintext_byteintarray)
    return result

