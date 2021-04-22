#!/usr/bin/python3

import sys, getopt, os.path, base64 as b64, time

def main(argv):
    inputFile = ""
    if(len(argv) == 0):
        print("Please use -e or -d and a file destination or use -h for more info.")
        sys.exit(2)
        pass
    try:
        opts, args = getopt.getopt(argv, "he:d:", ["help", "encode=", "decode="])
        pass
    except getopt.GetoptError:
        print("Please use -e or -d and a file destination or use -h for more info.")
        sys.exit(2)
        pass
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print("Usage for conversion: \n" \
            "-e or --encode      Encode a file into an image\n" \
            "-d or --decode      Decode an image to get the original file\n" \
            "-h or --help        Show this dialog")
            sys.exit(2)
            pass
        elif opt in ("-e", "--encode"):
            inputFile = os.path.normpath(arg)
            checkPath(inputFile)
            #data = _convert_and_compress(open(inputFile, "rb").read(), "1st", inputFile)
            data = _convert_to_b64(inputFile)
            #imageWriting(convertToInt(inputFile), inputFile)
            pass
        elif opt in ("-d", "--decode"):
            inputFile = os.path.normpath(arg)
            checkPath(inputFile)
            #convertFromInt(imageReading(inputFile), inputFile)
            pass
    pass



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


def _convert_to_b64(input_data):
    
    global base64_strings
    global base64_reversion
    data = open(input_data, "rb").read()
    data_two = ""
    start = time.perf_counter()
    encoded = b64.b64encode(data)
    decoded = encoded.decode("utf-8")
    print("Does input_data equal decoded: ", input_data == b64.b64decode(decoded))
    full_length = len(decoded)
    decoded = decoded[:decoded.find("=")]
    new_length = len(decoded)
    amount_of_equal_signs = full_length - new_length
    print("Number of equal signs: ", amount_of_equal_signs)
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
    matrix_string = string_one + string_two + string_three
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
    output_data = input_data + "-test"
    out_stream = open(output_data, "wb")
    out_stream.write(brand_new_data)
    end = time.perf_counter()
    print("Time taken to complete: ", end - start, " seconds.")
    


def checkPath(filePath):
    try:
        file = open(filePath)
        pass
    except IOError:
        print("Error: File not found. Please use a valid file.")
        sys.exit(2)
        pass
    print("Real file!")
    pass

if __name__ == "__main__":
    main(sys.argv[1:])
    pass