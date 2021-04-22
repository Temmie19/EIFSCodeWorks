#!/usr/bin/python3

import sys, binascii as ba, math, time, os, base64 as b64, base58 as b58, lzma, zstd, bz2, gzip, base62 as b62
from pathlib import Path
from burrowsWheeler import burrowsWheeler

base64_arrays = {"A": [0, 0, 0, 0, 0, 0], "B": [0, 0, 0, 0, 0, 1], \
    "C": [0, 0, 0, 0, 1, 0], "D": [0, 0, 0, 0, 1, 1], "E": [0, 0, 0, 1, 0, 0],\
    "F": [0, 0, 0, 1, 0, 1], "G": [0, 0, 0, 1, 1, 0], "H": [0, 0, 0, 1, 1, 1],\
    "I": [0, 0, 1, 0, 0, 0], "J": [0, 0, 1, 0, 0, 1], "K": [0, 0, 1, 0, 1, 0],\
    "L": [0, 0, 1, 0, 1, 1], "M": [0, 0, 1, 1, 0, 0], "N": [0, 0, 1, 1, 0, 1],\
    "O": [0, 0, 1, 1, 1, 0], "P": [0, 0, 1, 1, 1, 1], "Q": [0, 1, 0, 0, 0, 0],\
    "R": [0, 1, 0, 0, 0, 1], "S": [0, 1, 0, 0, 1, 0], "T": [0, 1, 0, 0, 1, 1],\
    "U": [0, 1, 0, 1, 0, 0], "V": [0, 1, 0, 1, 0, 1], "W": [0, 1, 0, 1, 1, 0],\
    "X": [0, 1, 0, 1, 1, 1], "Y": [0, 1, 1, 0, 0, 0], "Z": [0, 1, 1, 0, 0, 1],\
    "a": [0, 1, 1, 0, 1, 0], "b": [0, 1, 1, 0, 1, 1], "c": [0, 1, 1, 1, 0, 0],\
    "d": [0, 1, 1, 1, 0, 1], "e": [0, 1, 1, 1, 1, 0], "f": [0, 1, 1, 1, 1, 1],\
    "g": [1, 0, 0, 0, 0, 0], "h": [1, 0, 0, 0, 0, 1], "i": [1, 0, 0, 0, 1, 0],\
    "j": [1, 0, 0, 0, 1, 1], "k": [1, 0, 0, 1, 0, 0], "l": [1, 0, 0, 1, 0, 1],\
    "m": [1, 0, 0, 1, 1, 0], "n": [1, 0, 0, 1, 1, 1], "o": [1, 0, 1, 0, 0, 0],\
    "p": [1, 0, 1, 0, 0, 1], "q": [1, 0, 1, 0, 1, 0], "r": [1, 0, 1, 0, 1, 1],\
    "s": [1, 0, 1, 1, 0, 0], "t": [1, 0, 1, 1, 0, 1], "u": [1, 0, 1, 1, 1, 0],\
    "v": [1, 0, 1, 1, 1, 1], "w": [1, 1, 0, 0, 0, 0], "x": [1, 1, 0, 0, 0, 1],\
    "y": [1, 1, 0, 0, 1, 0], "z": [1, 1, 0, 0, 1, 1], "0": [1, 1, 0, 1, 0, 0],\
    "1": [1, 1, 0, 1, 0, 1], "2": [1, 1, 0, 1, 1, 0], "3": [1, 1, 0, 1, 1, 1],\
    "4": [1, 1, 1, 0, 0, 0], "5": [1, 1, 1, 0, 0, 1], "6": [1, 1, 1, 0, 1, 0],\
    "7": [1, 1, 1, 0, 1, 1], "8": [1, 1, 1, 1, 0, 0], "9": [1, 1, 1, 1, 0, 1],\
    "+": [1, 1, 1, 1, 1, 0], "/": [1, 1, 1, 1, 1, 1]}

base64_strings = {"A": "000000", "B": "000001", "C": "000010", "D": "000011", \
    "E": "000100", "F": "000101", "G": "000110", "H": "000111", "I": "001000",\
    "J": "001001", "K": "001010", "L": "001011", "M": "001100", "N": "001101",\
    "O": "001110", "P": "001111", "Q": "010000", "R": "010001", "S": "010010",\
    "T": "010011", "U": "010100", "V": "010101", "W": "010110", "X": "010111",\
    "Y": "011000", "Z": "011001", "a": "011010", "b": "011011", "c": "011100",\
    "d": "011101", "e": "011110", "f": "011111", "g": "100000", "h": "100001",\
    "i": "100010", "j": "100011", "k": "100100", "l": "100101", "m": "100110",\
    "n": "100111", "o": "101000", "p": "101001", "q": "101010", "r": "101011",\
    "s": "101100", "t": "101101", "u": "101110", "v": "101111", "w": "110000",\
    "x": "110001", "y": "110010", "z": "110011", "0": "110100", "1": "110101",\
    "2": "110110", "3": "110111", "4": "111000", "5": "111001", "6": "111010",\
    "7": "111011", "8": "111100", "9": "111101", "+": "111110", "/": "111111"}

base64_reversion = {'000000': 'A', '000001': 'B', '000010': 'C', '000011': 'D',\
    '000100': 'E', '000101': 'F', '000110': 'G', '000111': 'H', '001000': 'I', \
    '001001': 'J', '001010': 'K', '001011': 'L', '001100': 'M', '001101': 'N', \
    '001110': 'O', '001111': 'P', '010000': 'Q', '010001': 'R', '010010': 'S', \
    '010011': 'T', '010100': 'U', '010101': 'V', '010110': 'W', '010111': 'X', \
    '011000': 'Y', '011001': 'Z', '011010': 'a', '011011': 'b', '011100': 'c', \
    '011101': 'd', '011110': 'e', '011111': 'f', '100000': 'g', '100001': 'h', \
    '100010': 'i', '100011': 'j', '100100': 'k', '100101': 'l', '100110': 'm', \
    '100111': 'n', '101000': 'o', '101001': 'p', '101010': 'q', '101011': 'r', \
    '101100': 's', '101101': 't', '101110': 'u', '101111': 'v', '110000': 'w', \
    '110001': 'x', '110010': 'y', '110011': 'z', '110100': '0', '110101': '1', \
    '110110': '2', '110111': '3', '111000': '4', '111001': '5', '111010': '6', \
    '111011': '7', '111100': '8', '111101': '9', '111110': '+', '111111': '/'}

def convertToInt(fileInput):
    inStream = open(fileInput, "rb")
    print("File opened as binary.")
    data = ba.b2a_qp(inStream.read()).decode("utf-8")
    print("Data read to string.")
    inStream.close()
    print("In stream closed.")

    start = time.perf_counter()

    split = fileInput.split(os.path.sep)
    print("File name is", split[-1],". ")
    stringBuffer = split[-1]
    stringBuffer += "\n"
    stringBuffer += data
    stringBuffer += "TemmieBigBrainEndOfFileString"
    stringBytes = stringBuffer.encode("utf-8")
    stringBytes = bz2.compress(stringBytes)
    print("Data compressed.")
    #stringBytes = lzma.open(stringBytes, format=lzma.FORMAT_XZ)
    #stringBytes = b64.b64encode(stringBytes)
    #print("String converted to base 58.")
    stringBytes = zstd.compress(stringBytes)
    #print("Data compressed again.")
    transformation = str(stringBytes)#.decode("utf-8")
    #print("String converted to base 58.")
    bufferLoc = stringBuffer.find("=")
    print("First character of stringBytes is ", stringBytes[0], " while the first",\
        " character of transformation is ", transformation[0], ".")

    for x in range(len(stringBytes)):
        if(stringBytes[x] > 255):
            print("Higher than 255! ", stringBytes[x])
            pass
        pass
    
    if(bufferLoc != -1):
        stringBuffer = stringBuffer[:bufferLoc]
        print("Padding found.")
        pass

    
    print("Tranformation length is ", len(transformation), " while", \
        "original length is ", len(data))
    intArray = []

    for x in range(len(stringBytes)):
        #hexBytes.append(base64[transformation[x]])
        intArray.append(stringBytes[x])
        pass
    print("First item in intArray is ", intArray[0])
    end = time.perf_counter()
    print("IntArray length is ", len(transformation))
    print("Data converted to byte ints and loaded to string in ", \
        end - start, " seconds.")
    
    return intArray


def _convert_and_compress(input_data, try_count):
    global base64_strings
    global base64_arrays
    data = input_data
    data_two = ""
    print()
    start = time.perf_counter()
    encoded = b64.b64encode(data)
    decoded = encoded.decode("utf-8")
    print("Does input_data equal decoded: ", input_data == b64.b64decode(decoded))
    full_length = len(decoded)
    decoded = decoded[:decoded.find("=")]
    new_length = len(decoded)
    amount_of_equal_signs = full_length - new_length
    print("Number of equal signs: ", amount_of_equal_signs)
    encoded_and_shortened = ""
    print("Generating matrix")
    string_one = ""
    string_two = ""
    string_three = ""
    for x in range(len(decoded)):
        current_set = base64_strings[decoded[x]]
        string_one += current_set[0] + current_set[1]
        string_two += current_set[2] + current_set[3]
        string_three += current_set[4] + current_set[5]
        pass
    full_string_one = ""
    full_string_two = ""
    full_string_three = ""
    full_string_four = ""
    for x in range(len(data_two)):
        current_set = str(format(ord(data_two[x]), '08b'))
        full_string_one += current_set[0] + current_set[1]
        full_string_two += current_set[2] + current_set[3]
        full_string_three += current_set[4] + current_set[5]
        full_string_four += current_set[6] + current_set[7]
        pass
    full_matrix_string = full_string_one + full_string_two + full_string_three + full_string_four
    full_binary = ""
    for x in range(int(len(full_matrix_string) / 8)):
        start_pos = x * 8
        end_pos = ((x + 1) * 8)
        current_set = full_matrix_string[start_pos:end_pos]
        full_binary += chr(int(current_set, 2))
        pass
    full_binary.encode("utf-8")
    matrix_string = string_one + string_two + string_three
    print(len(matrix_string))
    print("Completed matrix")
    brand_new_data = ""
    for x in range(int(len(matrix_string) / 6)):
        start_pos = x * 6
        end_pos = ((x + 1) * 6)
        current_set = matrix_string[start_pos:end_pos]
        brand_new_data += base64_reversion[current_set]
        pass
    print(len(brand_new_data), len(decoded))
    for x in range(amount_of_equal_signs):
        brand_new_data += "="
        pass
    brand_new_data = b64.b64decode(brand_new_data.encode("utf-8"))
    redo = b64.b64encode(brand_new_data).decode("utf-8")
    redo_equal_signs = len(redo) - len(redo[:redo.find("=")])
    redo = redo[:redo.find("=")]
    print("First bytes of redo: ", redo[:50])
    print("Number of redo equal signs:", redo_equal_signs)
    string_four = ""
    string_five = ""
    string_six = ""
    new_binary = ""
    for x in range(len(redo)):
        new_binary += base64_strings[redo[x]]
        pass
    print(new_binary == matrix_string)
    print("New binary length: ", len(new_binary), " Old binary length: ", len(matrix_string))
    one_third = len(new_binary) // 3
    string_four = new_binary[:(one_third)]
    string_five = new_binary[one_third:(one_third * 2)]
    string_six = new_binary[(one_third * 2):]
    undone = ""
    print(string_three == string_six)
    for x in range(int(len(new_binary) / 3)):
        if(x % 2 == 0):
            current_string = ""
            current_string += string_four[x] + string_four[x+1]
            current_string += string_five[x] + string_five[x+1]
            current_string += string_six[x] + string_six[x+1]
            undone += base64_reversion[current_string]
            pass
        pass
    print("Does undone equal decoded: ", undone == decoded)
    for x in range(redo_equal_signs):
        undone += "="
        pass
    for x in range(amount_of_equal_signs):
        decoded += "="
        pass
    print("Does input_data equal decoded: ", input_data == b64.b64decode(decoded))
    decoded = decoded[:decoded.find("=")]
    print("Does undone equal encoded: ", undone.encode("utf-8") == encoded)
    undone = undone.encode("utf-8")
    print("Does undone equal input_data: ", undone == input_data)
    undone = b64.b64decode(undone)
    for x in range(len(decoded)):
        encoded_and_shortened += base64_strings[decoded[x]]
        pass
    print(undone == data)
    remainder = len(encoded_and_shortened) % 8
    if(remainder != 0):
        for i in range(8 - remainder):
            encoded_and_shortened += "0"
        pass
    #binary = int(encoded_and_shortened, 2).to_bytes(len(encoded_and_shortened) // 8, \
        #byteorder="big").decode("utf-8", "surrogatepass")
    converted_binary = ""
    #for x in range(int(len(encoded_and_shortened)/8)):
     #   start_of_string = x * 8
      #  end_of_string = (x + 1) * 8
       # binary_string = encoded_and_shortened[start_of_string:end_of_string]
        #converted_binary += int(binary_string, 2).to_bytes((len(binary_string) + 7) // 8, byteorder='big')
        #converted_binary += chr(int(binary_string, 2))
        #pass
    converted_binary = int(encoded_and_shortened, 2).to_bytes((len(encoded_and_shortened) + 7) // 8, byteorder='big')
    print("Base length is: ", len(data), "Encoded length is:", len(encoded), \
        "New length is: ", int(len(encoded_and_shortened))/6, )
    #converted_binary = converted_binary.encode("utf-8")
    compressed_bytes = zstd.compress(data)
    encoded_and_compressed = zstd.compress(encoded)
    #converted_binary = bz2.compress(converted_binary)
    converted_binary = zstd.compress(converted_binary)
    brand_new_data = zstd.compress(brand_new_data)
    full_binary = bz2.compress(full_binary.encode("utf-8"))
    print("Data compressed.")
    full_length = sys.getsizeof(compressed_bytes)
    original_length = sys.getsizeof(data)
    encoded_length = sys.getsizeof(encoded_and_compressed)
    binary_length = sys.getsizeof(converted_binary)
    recoded_length = sys.getsizeof(brand_new_data)
    new_bin_length = sys.getsizeof(full_binary)
    print("This is the ", try_count, " try.")
    print("Original length was: ", original_length, " Compressed length is: ", full_length, \
        " Encoded length is: ", encoded_length, " Binary length is: ", binary_length, \
        " Recoded length is: ", recoded_length, " New binary length is : ", new_bin_length)
    end = time.perf_counter()
    print("Time taken to complete: ", end - start, " seconds.")
    return compressed_bytes

def convertFromInt(intArray, fileName):
    start = time.perf_counter()
    byteString = b''
    for x in range(len(intArray)):
        byteString += intArray[x].to_bytes(1, byteorder="big")
        pass
    print("Ints converted to bytes.")
    print("First item in byteString is ", byteString[0])

    split = fileName.split(os.path.sep)
    filePath = ""
    for x in range(len(split) - 1):
        filePath += split[x]
        pass
    byteString = bz2.decompress(byteString)
    dataBuffer = byteString.decode("utf-8")
    eofLocation = dataBuffer.find("TemmieBigBrainEndOfFileString")
    data = dataBuffer[:eofLocation]
    firstLineEnd = data.find("\n")
    filePath += data[:firstLineEnd]
    print("Entire file path is ", filePath)
    data = data[firstLineEnd+1:]
    outStream = open(filePath, "wb")
    print("File opened as binary.")
    outStream.write(data)
    
    #print("Tranformation length is ", len(transformation), " while", \
        #"original length is ", len(data))


    #print("First item in hex bytes is ", hexBytes[0])
    end = time.perf_counter()
    print("Ints converted to bytes and written to file in ", \
        end - start, " seconds.")
    
    pass