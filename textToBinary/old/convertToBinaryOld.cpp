 
#include <iostream>
#include <fstream>
#include <vector>
#include <string.h>
#include <sstream>
#include <algorithm>
#include <limits>
#include <bits/stdc++.h> 
#include <ctype.h>
#include <iterator>

std::string inPath = "example.ync";
std::string outPath;

std::vector<std::string> split(const std::string &string, const char delim);


bool convertToHex();

char* readBitsTwo();

std::string allBits;

std::stringstream readBuffer;


int main() {
    std::cout << "Please input file path:";
    std::cin >> inPath;

    outPath = inPath;
    outPath.append("-output.txt");

    readBitsTwo();

}

char* readBitsTwo() {
    std::ifstream in_stream(inPath, std::ifstream::in|std::ios::binary);
    if (!in_stream.good()) {
        std::cout << "Input stream to file " << inPath << " is not valid \n";
    }

    std::ofstream out_stream(outPath, std::ofstream::out);
    if (!out_stream.good()) {
        std::cout << "Output stream to file " << outPath << " is not valid \n";
    }

    std::vector<std::string> location = split(inPath, '/');
    out_stream << location.back() << std::endl;

    in_stream.seekg(0, in_stream.end);
    int fileLength = in_stream.tellg();
    in_stream.seekg(0,in_stream.beg);

    char fileBufferChar[fileLength];

    in_stream.read(fileBufferChar, fileLength);

    std::stringstream conversion;

    conversion << std::hex;
    int counter = 0;
    for(int i = 0; i < fileLength; i++){
        conversion << std::setw(2) << std::setfill('0') << (int)fileBufferChar[i];
    }

    char fileOutput[conversion.str().length()];

    std::strcpy(fileOutput, conversion.str().c_str());

    out_stream << fileOutput;

}


bool convertToHex(){

    //This will open the file
    std::ifstream in_stream;
    in_stream.open(inPath, std::ifstream::in);

    //Check if the input file is valid
    if (!in_stream.good()) {
        std::cout << "Input stream to file " << inPath << " is not valid \n";
        return false;
    }

    /*std::vector<std::string> location = split(inPath, '/');
    for(int i = 0; i < location.size() - 1; i++){
        outPath += location[i];
        outPath += "/";
    }*/

    in_stream.seekg(0, in_stream.end);
    int fileLength = in_stream.tellg();

    char fileBufferChar[fileLength];

    in_stream.read(fileBufferChar, fileLength);

    std::string line;
    std::string hexLine;
    std::stringstream currentHex;
    std::vector<int> hexVec;

    //While there are still lines to be read, convert each character
    //of a line to its hexidecimal
    int bitCount = 0;
    int byteBuffer;
    std::string oneByte;
    int lineCount = 0;
    while(std::getline(in_stream, line)) {
        if(lineCount < 1){
            outPath.append(line);
            lineCount++;
            std::cout << "Line one complete" << std::endl;
        }
        else {
            std::vector<std::string> vecBuffer = split(line, ' ');
            for(int i = 0; i < vecBuffer.size(); i++){
                vecBuffer[i].insert(0,"0x");
                std::cout << "vecBuffer[i] is " << vecBuffer[i] << std::endl;
                currentHex.str() = hexVec[i];
                currentHex >> byteBuffer;
                hexVec.push_back(byteBuffer);
                byteBuffer = 0;
            }
            std::cout << "Converted into " << hexLine << std::endl;
            oneByte = "0x";

            for(int i = 0; i < hexLine.size(); i++){
                if (bitCount < 2){
                    oneByte += hexLine[i];
                    bitCount++;
                }
                else{
                    currentHex.str() = oneByte;
                    //std::cout << "CurrentHex string is " << currentHex.str() << std::endl;
                    currentHex >> byteBuffer;
                    hexVec.push_back(byteBuffer);
                    byteBuffer = 0;
                    bitCount = 1;
                    oneByte = "0x";
                    oneByte += hexLine[i];
                    currentHex.str(std::string());
                }
            }
            hexLine = "";
            std::cout << "Line two complete" << std::endl;
        }
    }

    while(!in_stream.eof()){
        in_stream >> std::noskipws >> fileBufferChar;
    }
    std::cout << fileBufferChar[fileLength];

    std::ofstream out_stream(outPath, std::ofstream::out);

    //Check if the output file is valid
    if (!out_stream.good()) {
        std::cout << "Output stream to file " << outPath << " is not valid \n";
        return false;
    }

    char fileOutput[hexVec.size()];
    for(int i = 0; i < hexVec.size(); i++){
        fileOutput[i+1] = hexVec[i];
    }
    //out_stream.write(fileOutput,sizeof(fileOutput));
    return true;

}

std::vector<std::string> split(const std::string &string, const char delim){
    std::vector<std::string> result;

    std::stringstream splitStream(string);
    std::string item;

    while(std::getline(splitStream, item, delim)){
        result.push_back(item);
    }
    return result;
}