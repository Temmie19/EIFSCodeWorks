#!/usr/bin/python3

import sys, getopt, os.path, binascii

from fileConversions import convertToInt, convertFromInt, _convert_and_compress
from imageProcessing import imageWriting, imageReading

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
            data = _convert_and_compress(open(inputFile, "rb").read(), "1st")
            data = _convert_and_compress(data, "2nd")
            data = _convert_and_compress(data, "3rd")
            #imageWriting(convertToInt(inputFile), inputFile)
            pass
        elif opt in ("-d", "--decode"):
            inputFile = os.path.normpath(arg)
            checkPath(inputFile)
            convertFromInt(imageReading(inputFile), inputFile)
            pass
    pass

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

