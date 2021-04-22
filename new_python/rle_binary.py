#!/usr/bin/python3

from base64 import decode, encodebytes
import sys, getopt, os.path, time, lzma, zstd, bz2, gzip
from burrows_wheeler import burrows_wheeler

base16_strings = {"0": "10", "1": "110", "2": "111", "3": "010", "4": "0110", "5": "0010", \
    "6": "00110", "7": "00111", "8": "00110", "9": "00010", "A": "000110",\
    "B": "000111", "C": "000010", "D": "0000110", "E": "0000111",\
    "F": "000010"}
base16_reverse = {"F": "0", "E": "10", "D": "110", "C": "1110", "B": "11110", "A": "111110", \
    "9": "1111110", "8": "11111110", "7": "111111110", "6": "1111111110", "5": "11111111110",\
    "4": "111111111110", "3": "1111111111110", "2": "11111111111110", "1": "111111111111110",\
    "0": "1111111111111110"}


data = open("/home/temmie19/codes/testing/mafiaTownIntro.mp3", "rb").read()
print(len(data))
start = time.perf_counter()
decoded = ""
for i in range(len(data)):
    decoded += chr(data[i])
print(len(decoded))
rounds = len(decoded) // 16384
print(rounds)
last_round = len(decoded) % 16384
encoded_data = ""
for i in range(rounds + 1):
    if(i < rounds):
        encoded_data += burrows_wheeler(decoded[i*16384:(i+1)*16384])
    else:
        encoded_data += burrows_wheeler(decoded[i*16384:])
    print(i)
shortened_data = ""
current_char = encoded_data[0]
current_count = 0
for i in range(len(encoded_data)):
    if(current_char == encoded_data[i]):
        if(current_count == 255):
            shortened_data += current_char + chr(current_count)
            current_count = 0
        current_count += 1
    else:
       shortened_data += current_char + chr(current_count)
       current_count = 1
       current_char = encoded_data[i] 
print(ord(shortened_data[20]))
encoded_data = b''
for i in range(len(shortened_data)):
    number = int(ord(shortened_data[i]))
    encoded_data += number.to_bytes(1, byteorder='big')



zstd_data = zstd.compress(encoded_data)
bz2_data = bz2.compress(encoded_data)
lzma_data = lzma.compress(encoded_data)
gzip_data = gzip.compress(encoded_data)
zstd_data_old = zstd.compress(data)
bz2_data_old = bz2.compress(data)
lzma_data_old = lzma.compress(data)
gzip_data_old = gzip.compress(data)


print(len(data))
print(len(zstd_data))
print(len(bz2_data))
print(len(lzma_data))
print(len(gzip_data))
print()
print(len(zstd_data_old))
print(len(bz2_data_old))
print(len(lzma_data_old))
print(len(gzip_data_old))
print("Completed in: ", (time.perf_counter() - start), " seconds.")