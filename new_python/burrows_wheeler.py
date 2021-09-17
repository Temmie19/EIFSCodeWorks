#!/usr/bin/python3
import yenc, huffman, array, lzma
from test_bwt import burroughs_wheeler_custom

char_list = ['\x00', '\x01', '\x02', '\x03', '\x04', '\x05', '\x06', '\x07', '\x08', \
    '\t', '\n', '\x0b', '\x0c', '\r', '\x0e', '\x0f', '\x10', '\x11', '\x12', '\x13',\
     '\x14', '\x15', '\x16', '\x17', '\x18', '\x19', '\x1a', '\x1b', '\x1c', '\x1d', \
     '\x1e', '\x1f', ' ', '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',',\
     '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';', '<', \
     '=', '>', '?', '@', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', \
     'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '[', '\\',\
     ']', '^', '_', '`', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', \
     'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', \
     '}', '~', '\x7f', '\xa0', '¡', '¢', '£', '€', '¥', 'Š', '§', 'š', '©', 'ª', '«',\
     '\x80', '\x81', '\x82', '\x83', '\x84', '\x85', '\x86', '\x87', '\x88', '\x89', \
     '\x8a', '\x8b', '\x8c', '\x8d', '\x8e', '\x8f', '\x90', '\x91', '\x92', '\x93', \
     '\x94', '\x95', '\x96', '\x97', '\x98', '\x99', '\x9a', '\x9b', '\x9c', '\x9d', \
     '\x9e', '\x9f', '¬', '\xad', '®', '¯', '°', '±', '²', '³', 'Ž', 'µ', '¶', '·',  \
     'ž', '¹', 'º', '»', 'Œ', 'œ', 'Ÿ', '¿', 'À', 'Á', 'Â', 'Ã', 'Ä', 'Å', 'Æ', 'Ç', \
     'È', 'É', 'Ê', 'Ë', 'Ì', 'Í', 'Î', 'Ï', 'Ð', 'Ñ', 'Ò', 'Ó', 'Ô', 'Õ', 'Ö', '×', \
     'Ø', 'Ù', 'Ú', 'Û', 'Ü', 'Ý', 'Þ', 'ß', 'à', 'á', 'â', 'ã', 'ä', 'å', 'æ', 'ç', \
     'è', 'é', 'ê', 'ë', 'ì', 'í', 'î', 'ï', 'ð', 'ñ', 'ò', 'ó', 'ô', 'õ', 'ö', '÷', \
     'ø', 'ù', 'ú', 'û', 'ü', 'ý', 'þ', 'ÿ']

def burrows_wheeler(input:str):
    #test = encode(input, str(chr(10)+chr(13)+chr(61)+chr(0)))
    #yenc_string = test[2].decode("iso-8859-15")
    #print(len(yenc_string))
    """array = []
    string = ""
    not_found = []
    for i in range(len(test[2])):
        array.append(test[2][i])
    array = sorted(array)
    print(array[-1])
    for i in range(256):
        try:
            location = array.index(i)
        except:
            not_found.append(i)

    #print(not_found)"""
    global char_list
    #transformation = ''.join([i[-1] for i in sorted([input[i:] + input[:i] for i in range(len(input))])])
    buckets = [list() for i in range(256)]
    sorted_positions = []
    for i in range(len(input)):
        buckets[char_list.index(input[(i+1) % len(input)])].append(i)   
    for i in range(len(buckets)):
            sorted_positions.extend(buckets[i])
            buckets[i].clear()
    for i in range(len(sorted_positions)):
        buckets[char_list.index(input[i])].append(sorted_positions[i])
    """for i in range(8):
        sorted_positions = []
        for j in range(len(buckets)):
            sorted_positions += buckets[j]
            buckets[j].clear()
        for x in range(len(sorted_positions)):
            position = (sorted_positions[x] + (7 - i)) % len(input)
            if(position < 0):
                position = (len(input) - 1) - position
            buckets[char_list.index(input[position])].append(position)"""
    transformation_list = []
    for i in range(len(buckets)):
        buckets[i] = [k[-1] for k in sorted([input[j:] + input[:j] for j in range(len(buckets[i]))])]
        transformation_list += buckets[i]
        buckets[i].clear()
    transformation = "".join(transformation_list)
    """rotations = []
    one_rotation = input + chr(10)
    for x in range(len(one_rotation)-1):
        one_rotation = one_rotation[-1] + one_rotation [:-1]
        rotations.append(one_rotation)
        pass
    sorted_array = sorted(rotations)

    #print("Data sorted lexicographically.")
    transformation = ""
    for x in range(len(sorted_array)):
        sorted_array[x] = sorted_array[x][-1]
        transformation += sorted_array[x]
        pass"""
    ascii = char_list
    for i in range(len(transformation)):
        index = ascii.index(transformation[i])
        if(index == 0):
            transformation = transformation[:i] + chr(12) + transformation[i+1:]
        else:
            ascii.pop(index)
            ascii.insert(0, transformation[i])
            transformation = transformation[:i] + ascii[0] + transformation[i+1:]
    #transformation = burroughs_wheeler_custom(input + chr(10))
    if(len(transformation) == 16384):
        transformation += chr(11)
        #print("Equal to 16384")
    else:
        transformation += chr(11)
        #print("Not equal to 16384. ", len(transformation), " vs ", len(input))
    #rotations.clear()
    """previous_char = ""
    for i in range(len(transformation)):
        if(transformation[i] == previous_char):
            transformation = transformation[:i] + chr(12) + transformation[i+1:]
        else:
            previous_char = transformation[i]
    print(transformation[:251])"""
    return transformation

def reverse_bwt(input):
    reverse = input[:-1]
    previous_char = ""
    transformation = ""
    for i in range(len(reverse)):
        if(reverse[i] == chr(12)):
            reverse = reverse[:i] + previous_char + reverse[i+1:]
        else:
            previous_char = reverse[i]
    pass

