#!/usr/bin/python3

import sys, getopt, os.path, base64 as b64, time, lzma, zstd, bz2, gzip


base16_strings = {"0": "10", "1": "110", "2": "111", "3": "010", "4": "0110", "5": "0010", \
    "6": "00110", "7": "00111", "8": "00110", "9": "00010", "A": "000110",\
    "B": "000111", "C": "000010", "D": "0000110", "E": "0000111",\
    "F": "000010"}
base16_reverse = {"F": "0", "E": "10", "D": "110", "C": "1110", "B": "11110", "A": "111110", \
    "9": "1111110", "8": "11111110", "7": "111111110", "6": "1111111110", "5": "11111111110",\
    "4": "111111111110", "3": "1111111111110", "2": "11111111111110", "1": "111111111111110",\
    "0": "1111111111111110"}

def cleanFunction(string):
    converted_one = ""
    converted_two = ""
    '''for i in range(len(string)):
        if(i % 2 == 0):
            converted_one += string[i]
        else:
            converted_two += string[i]
        pass
    converted_full = converted_two + converted_one'''
    converted_full = ""
    for i in range(len(string)):
        converted_full += base16_strings[string[i]]
        pass
    if(len(converted_full) % 8 != 0):
        for i in range (len(converted_full) % 8):
            converted_full += "0"
        pass
    return converted_full.encode()

a = "102".encode()
b = b64.b64encode(a)
print(b.decode())
data = open("/home/temmie19/codes/testing/mafiaTownIntro.mp3", "rb").read()
zstd_data = zstd.compress(data)
bz2_data = bz2.compress(data)
lzma_data = lzma.compress(data)
gzip_data = gzip.compress(data)

zstd_data_two = b64.b16encode(zstd_data).decode()
bz2_data_two = b64.b16encode(bz2_data).decode()
lzma_data_two = b64.b16encode(lzma_data).decode()
gzip_data_two = b64.b16encode(gzip_data).decode()
binary = ""
'''for i in range(len(data)):
    binary += str(bin(data[i]))[2:].zfill(8)
    pass
current_char = binary[0]
current_count = 0
count_array = []'''
compression_string = ""
'''for i in range(len(binary)):
    if(current_char != binary[i]):
        count_array.append([hex(current_count), current_char])
        compression_string += chr(current_count)
        current_char = binary[i]
        current_count = 1
    else:
        current_count += 1
    pass'''

zstd_string = zstd.compress(b64.b16decode(cleanFunction(zstd_data_two)))
bz2_string = bz2.compress(b64.b16decode(cleanFunction(bz2_data_two)))
lzma_string = bz2.compress(b64.b16decode(cleanFunction(lzma_data_two)))
gzip_string = gzip.compress(b64.b16decode(cleanFunction(gzip_data_two)))
print(len(data))
print(len(compression_string))
print(len(zstd_data))
print(len(bz2_data))
print(len(lzma_data))
print(len(gzip_data))
print()
print(len(zstd_string))
print(len(bz2_string))
print(len(lzma_string))
print(len(gzip_string))