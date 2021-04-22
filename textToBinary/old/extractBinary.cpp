 
#include <iostream>
#include <fstream>
#include <vector>
#include <string.h>
#include <sstream>
#include <algorithm>
#include <array> 
#include <limits>
#include <bitset>

std::string inPath = "example.ync";
std::string outPath;

using byte = unsigned char;
constexpr std::size_t bitsPerByte = std::numeric_limits<byte>::digits ;


bool convertToHex();

char readBits();
std::string allBits;

std::vector<std::string> split(const std::string &string, const char delim);

std::stringstream readBuffer;


int main() {
    std::cout << "Please input file path:";
    std::cin >> inPath;
    outPath = inPath;
    outPath.append("-binary.txt");
    readBits();

}

char readBits(){

    using bits = std::bitset<bitsPerByte>;

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
    std::cout << "fileLength is " << fileLength << std::endl;
    char fileBuffer[fileLength];
    std::cout << "Char fileBuffer made. First 8 characters are" << fileBuffer[1] << 
    fileBuffer[2] << fileBuffer[3] << fileBuffer[4] << fileBuffer[5] << fileBuffer[6] <<
    fileBuffer[7] << fileBuffer[8] <<std::endl;
    in_stream.read(fileBuffer, fileLength);
    std::cout << "File read" << std::endl;
    out_stream << fileBuffer;
    
}

bool convertToHex(){

    readBits();



    std::ofstream out_stream(outPath, std::ofstream::out);

    //Check if the output file is valid
    if (!out_stream.good()) {
        std::cout << "Output stream to file " << outPath << " is not valid \n";
        return false;
    }

    const char delim = '/';
    std::vector<std::string> location = split(inPath, '/');
    out_stream << location.back() << std::endl;



    std::string line;
    std::string hexLine;
    std::stringstream currentHex;
    std::vector<int>::iterator it;

    //While there are still lines to be read, convert each character
    //of a line to its hexidecimal
    int bitCount = 0;
    int byteBuffer;
    std::string oneByte;
    while(std::getline(readBuffer, line)) {
        for(int i = 0; i < allBits.length(); i++){
                if(bitCount < 7){
                    oneByte += line[i];
                    bitCount++;
                }
                else{
                    oneByte += line[i];
                    byteBuffer = std::stoi(oneByte);
                    currentHex << std::hex << std::uppercase << byteBuffer;
                    oneByte = currentHex.str();
                    if(oneByte.length() < 6){
                        while(oneByte.length() < 6){
                            oneByte.insert(0,"0");
                        }
                    }
                    bitCount = 0;
                    hexLine.append(oneByte);
                    hexLine.append(" ");
                    currentHex.str(std::string());
                    oneByte = "";
                }
                out_stream << hexLine;
            line = "";
            hexLine = "";    
        }
    }

    std::cout << "Conversion done! \n";

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