 
CC = g++

CFLAGS = -Wall -O3 -std=c++11

filePath= build/hexConverter

WinCC = x86_64-w64-mingw32-g++

default: converter.cpp mainClass.cpp imageProcessing.cpp compressor.cpp 
	$(CC) $(CFLAGS) -o $(filePath) mainClass.cpp converter.cpp imageProcessing.cpp lodepng.cpp compressor.cpp 

windows: converter.cpp mainClass.cpp
	$(WinCC) $(CFLAGS) -static-libstdc++ -static-libgcc -o $(filePath) mainClass.cpp converter.cpp imageProcessing.cpp lodepng.cpp

clean:
	$(RM) $(filePath) $(filePath).exe
