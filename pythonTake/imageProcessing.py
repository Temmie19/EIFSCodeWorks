#!/usr/bin/python3

import os, math, time, bz2, lzma
from PIL import Image, ImageColor, ImageDraw2

def imageWriting(colours, fileName):
    print("Array length is ", len(colours))
    start = time.perf_counter()
    fileName += ".png"
    width = math.ceil(math.sqrt(len(colours))) * 2
    height = math.ceil(math.sqrt(len(colours))) * 4
    print("Image size calculated. Width is ", width, " and height", \
        "is ", height, ".")
    vecPos = 0
    im = Image.new("1", (width, height), 1)
    pixels = im.load()

    for y in range(height):
        for x in range (width):
            if(vecPos < len(colours) - 1):
                if(x % 2 == 0):
                    if(y % 4 == 0):
                        currentSet = bin(colours[vecPos])
                        while(len(currentSet) < 10):
                            currentSet = currentSet[:2] + "0" + currentSet[2:]
                            pass
                        im.putpixel((x, y), (int(currentSet[2]),))
                        im.putpixel((x + 1, y), (int(currentSet[3]),))
                        im.putpixel((x, y + 1), (int(currentSet[4]),))
                        im.putpixel((x + 1, y + 1), (int(currentSet[5]),))
                        im.putpixel((x, y + 2), (int(currentSet[6]),))
                        im.putpixel((x + 1, y + 2), (int(currentSet[7]),))
                        im.putpixel((x, y + 3), (int(currentSet[7]),))
                        im.putpixel((x + 1, y + 3), (int(currentSet[8]),))
                        vecPos += 1
                        lastRow = y
                        pass
                    pass
                pass
            else:
                if(y != lastRow):
                    pixels[x,y] = (1,)
                    pass
                else:
                    pixels[x,y] = (1,)
                    pixels[x,y+1] = (1,)
                    pixels[x,y+2] = (1,)
                    pixels[x,y+3] = (1,)
                pass
            pass
        pass

    #im.show()
    im.save(fileName, format="WebP", lossless = True)
    imageReadingHorizontal(fileName)
    
    end = time.perf_counter()
    print("Bytes converted to image in ", end - start, " seconds.")
    pass

def imageReadingHorizontal(fileName):
    im = Image.open(fileName)
    print("Image loaded.")
    start = time.perf_counter()
    width = im.size[0]
    height = im.size[1]
    print("Image size calculated. Width is ", width, " and height", \
        "is ", height, ".")
    intArray = []
    for y in range(height):
        for x in range (width):
            if(x % 2 == 0):
                if(y % 4 == 0):
                    if(y + 3 > height):
                        break
                    xPlus = 0
                    yPlus = 0
                    nextLine = False
                    currentSet = ""
                    for i in range(8):
                        currentNumber = str(im.getpixel((x + xPlus, y + yPlus)))
                        if(currentNumber == "255"):
                            currentNumber = "1"
                            pass
                        currentSet += currentNumber
                        xPlus += 1
                        if(nextLine == False):
                            nextLine = True
                            pass
                        else:
                            xPlus = 0
                            yPlus += 1
                            nextLine = False
                            pass
                        pass
                    intArray.append(int(currentSet, base=2))
                    pass
                pass
            pass
        pass
    for x in range(len(intArray)):
        byteString += intArray[x].to_bytes(1, byteorder="big")
        pass
    end = time.perf_counter()
    print("Last item in intArray is ", intArray[len(intArray)-1])
    print("Bytes read from image image in ",\
            "and loaded into string in ", end - \
            start, " seconds.")
    return intArray
    

def imageReading(fileName):
    im = Image.open(fileName)
    print("Image loaded.")
    start = time.perf_counter()
    width = im.size[0]
    height = im.size[1]
    print("Image size calculated. Width is ", width, " and height", \
        "is ", height, ".")
    intArray = []
    for y in range(height):
        for x in range (width):
            if(x % 2 == 0):
                if(y % 4 == 0):
                    if(y + 3 > height):
                        break
                    xPlus = 0
                    yPlus = 0
                    nextLine = False
                    currentSet = ""
                    for i in range(8):
                        currentNumber = str(im.getpixel((x + xPlus, y + yPlus)))
                        if(currentNumber == "255"):
                            currentNumber = "1"
                            pass
                        currentSet += currentNumber
                        xPlus += 1
                        if(nextLine == False):
                            nextLine = True
                            pass
                        else:
                            xPlus = 0
                            yPlus += 1
                            nextLine = False
                            pass
                        pass
                    location = 0
                    intArray.append(int(currentSet, base=2))
                    pass
                pass
            pass
        pass
    end = time.perf_counter()
    print("Last item in intArray is ", intArray[len(intArray)-1])
    print("Bytes read from image image in ",\
            "and loaded into string in ", end - \
            start, " seconds.")
    return intArray
    