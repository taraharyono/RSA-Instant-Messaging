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
        for i in range(0, len(byteint_array), size):
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

            blocked_byteintarray.append(int(block))
        return blocked_byteintarray
    

def HexStringToByteIntArray(hexstring):
    byteint_array = []
    
    i = 0
    while (i<len(hexstring)):
        if (i==len(hexstring)-1):
            byteint_array.append(int(hexstring[i]+"0",16))
            i = i + 1
        else:
            byteint_array.append(int(hexstring[i:i+2],16))
            i = i + 2
        
    return byteint_array


def ByteIntArrayToHexString(byteint_array):
    hexstring = ""
    for byte in byteint_array:
        cipher_hex = str(hex(byte))[2:].upper()
        if (len(cipher_hex)==1):
            cipher_hex = '0'+cipher_hex
        hexstring = hexstring + cipher_hex

    return hexstring


def CiphertextBlockSize(n):
    size = math.log(n, 16)
    return (int(size)+1)


def CiphertextToBlock(ciphertext, n):
    ciphertext_string = str(ciphertext)
    block_size = CiphertextBlockSize(n)

    ciphertext_block = []

    for i in range(0, len(ciphertext_string), block_size):
        block = ""
        for j in range(block_size):
            if ((i+j) < len(ciphertext_string)):
                block += ciphertext_string[i+j]
            else:
                block += "0"
        
        ciphertext_block.append(int(block, 16))
    
    return ciphertext_block


def read_file_bytes(filename):
    byte_array = []
    try:
        with open(filename, 'rb') as file:
            byte = file.read(1)
            while byte:
                byte_array.append(int.from_bytes(byte, byteorder='little'))
                byte = file.read(1)
    except FileNotFoundError:
        print("File not found!")
    return byte_array


def encrypt(plaintext, e, n, block_size, is_file):
    """File fed should be in the form of array of integer (byte)"""
    if not is_file:
        plaintext_byteintarray = StringToByteIntArray(plaintext)
        plaintext_blocks = ByteIntArrayToBlocks(plaintext_byteintarray, block_size)
    else:
        plaintext_blocks = ByteIntArrayToBlocks(plaintext, block_size)

    ciphertext_blocksize = CiphertextBlockSize(n)

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
    return plaintext_byteintarray

# Testing

# file_array = read_file_bytes('UMKM.png')
# print(file_array)
# print("\noke")

# enc = encrypt(file_array, 79, 3337, 1, True)
# print(enc)
# enc_byteintarray = HexStringToByteIntArray(enc)

# output = open('Hasil.png', "wb")
# for byteint in enc_byteintarray:
#     output.write(byteint.to_bytes(1, byteorder='little'))

# output.close()

# dec_byteintarray = read_file_bytes('Hasil.png')
# dec_hex = ByteIntArrayToHexString(dec_byteintarray)

# dec = decrypt(dec_hex, 1019, 3337)

# output_dec = open('Hasil Dec.png', "wb")
# for byteint in dec:
#     output_dec.write(byteint.to_bytes(1,byteorder='little'))
# output_dec.close()
