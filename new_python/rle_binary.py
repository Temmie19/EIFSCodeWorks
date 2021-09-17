#!/usr/bin/python3

import sys, getopt, os.path, time, lzma, zstd, bz2, gzip, huffman, collections, h5py, hdf5plugin, numpy
from typing import Collection
from burrows_wheeler import burrows_wheeler
from alternate_encoding import escape_encoding, escape_decoding
from base64_converter import base64_converter

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
decoded = data.decode("iso-8859-15")
escapeless = escape_encoding(decoded)
#unescaped = escape_decoding(escapeless)
#print(len(unescaped), " vs ", len(decoded))
#print(unescaped == decoded)
print(len(decoded))
rounds = len(escapeless) // 16384
print(rounds)
last_round = len(decoded) % 16384
encoded_data = b""
lzc = lzma.LZMACompressor(preset=9)
for i in range(rounds + 1):
    pre_compressed = b''
    if(i < rounds):
        pre_compressed = burrows_wheeler(escapeless[i*16384:(i+1)*16384]).encode("iso-8859-15")
    else:
        pre_compressed = burrows_wheeler(escapeless[i*16384:]).encode("iso-8859-15")
    encoded_data += lzc.compress(pre_compressed)
test_data = encoded_data.decode("iso-8859-15")
escapeless = escape_encoding(test_data)
rounds = len(escapeless) // 16384
encoded_data_two = b""
for i in range(rounds + 1):
    pre_compressed = b''
    if(i < rounds):
        pre_compressed = burrows_wheeler(escapeless[i*16384:(i+1)*16384]).encode("iso-8859-15")
    else:
        pre_compressed = burrows_wheeler(escapeless[i*16384:]).encode("iso-8859-15")
    encoded_data_two += lzc.compress(pre_compressed)
test_data = encoded_data_two.decode("iso-8859-15")
escapeless = escape_encoding(test_data)
rounds = len(escapeless) // 16384
encoded_data_three = b""
for i in range(rounds + 1):
    pre_compressed = b''
    if(i < rounds):
        pre_compressed = burrows_wheeler(escapeless[i*16384:(i+1)*16384]).encode("iso-8859-15")
    else:
        pre_compressed = burrows_wheeler(escapeless[i*16384:]).encode("iso-8859-15")
    encoded_data_three += lzc.compress(pre_compressed)
test_data = encoded_data_three.decode("iso-8859-15")
escapeless = escape_encoding(test_data)
rounds = len(escapeless) // 16384
encoded_data_four = b""
for i in range(rounds + 1):
    pre_compressed = b''
    if(i < rounds):
        pre_compressed = burrows_wheeler(escapeless[i*16384:(i+1)*16384]).encode("iso-8859-15")
    else:
        pre_compressed = burrows_wheeler(escapeless[i*16384:]).encode("iso-8859-15")
    encoded_data_four += lzc.compress(pre_compressed)


#encoded_data = encoded_data.encode("iso-8859-15")
"""shortened_data = ""
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
    encoded_data += number.to_bytes(1, byteorder='big')"""

f = h5py.File("mytestfile.hdf5", "rw")
dset = f.create_dataset("autochunk", (1000, 1000), chunks=True 
    **hdf5plugin.Blosc(cname='zstd', clevel=9, shuffle=hdf5plugin.Blosc.SHUFFLE))

dset.attrs["autochunk"] = numpy.void(encoded_data)


zstd_data = zstd.compress(encoded_data)
bz2_data = bz2.compress(encoded_data)
lzma_data = lzma.compress(encoded_data)
gzip_data = gzip.compress(encoded_data)
zstd_data_old = zstd.compress(data)
bz2_data_old = bz2.compress(data)
lzma_data_old = lzma.compress(data)
gzip_data_old = gzip.compress(data)


print("Original size: ", len(data))
print("Encoded size: ", len(encoded_data))
print("Double encoded size: ", len(encoded_data_two))
print("Triple encoded size: ", len(encoded_data_three))
print("Quad encoded size: ", len(encoded_data_four))
print("ZTSD + BWT + MTF: ", len(zstd_data))
print("BZip + BWT + MTF: ", len(bz2_data))
print("LZMA + BWT + MTF: ", len(lzma_data))
print("GZip + BWT + MTF: ", len(gzip_data))
print()
print("ZTSD: ", len(zstd_data_old))
print("BZip: ", len(bz2_data_old))
print("LZMA: ", len(lzma_data_old))
print("GZip: ", len(gzip_data_old))
print()
print("HDF5 size", len(dset))
print("Completed in: ", (time.perf_counter() - start), " seconds.")