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
    

def ByteIntArrayToBlocks2(byteint_array, size):
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
    
array = [7, 97, 103, 3337, 5467]

print(ByteIntArrayToBlocks(array, 2))
print(ByteIntArrayToBlocks2(array, 2))