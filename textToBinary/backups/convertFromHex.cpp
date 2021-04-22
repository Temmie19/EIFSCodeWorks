#include <iostream>
#include <fstream>
#include <vector>
#include <string.h>
#include <sstream>
#include <iomanip>
#include <bits/stdc++.h> 
#include <chrono> 

std::string inPath = "example.ync";
std::string outPath;

std::string convertFromHex();

std::vector<std::string> split(const std::string &string, const char delim);

int main() {
    std::cout << "Please input file path:";
    std::cin >> inPath;

    convertFromHex();

}

std::string convertFromHex() {
    std::ifstream in_stream(inPath, std::ifstream::in);
    if (!in_stream.good()) {
        std::cout << "Input stream to file " << inPath << " is not valid \n";
    }

    auto start = std::chrono::system_clock::now();
    std::cout << "In stream loaded." << std::endl;

    std::vector<std::string> location = split(inPath, '/');
    for(int i = 0; i < location.size() - 1; i++){
        outPath += location[i];
        outPath += "/";
    }

    in_stream.seekg(0, in_stream.end);
    int fileLength = in_stream.tellg();
    in_stream.seekg(0,in_stream.beg);

    std::string fileName;
    
    std::cout << "Out stream location and file size calculated." << std::endl;

    std::stringstream conversion;
    std::string fileBuffer;
    std::string fullFile;
    int lineCounter = 0;
    while(getline(in_stream, fileBuffer)){
        if(lineCounter < 1){
            fileName = fileBuffer;
            lineCounter++;
            std::cout << "File name is " << fileName;
        }
        else{
            fullFile += fileBuffer;
        }
        
    }
    outPath.append(fileName);

    conversion << fullFile;
    fullFile = "";
    std::string singleWord;
    while(!conversion.eof()){
        conversion >> singleWord;
        fullFile += singleWord;
    }
    std::cout << fullFile.substr(0, 24);

    std::cout << "In stream read." << std::endl;

    in_stream.close();

    std::cout << "In stream closed." << std::endl;

    std::basic_string<uint8_t> bytes;

    for(size_t i = 0; i < fullFile.length(); i+=2){
        uint16_t byte;
        std::string nextByte = fullFile.substr(i,2);
        std::stringstream(nextByte) >> std::hex >> byte;
        bytes.push_back(static_cast<uint8_t>(byte));
    }

    std::string fileOutput(begin(bytes), end(bytes));

    std::cout << "Data converted from hex and loaded into string." << std::endl;

    std::ofstream out_stream(outPath, std::ofstream::out|std::ios::binary);
    if (!out_stream.good()) {
        std::cout << "Output stream to file " << outPath << " is not valid \n";
    }

    std::cout << "Out stream loaded." << std::endl;

    out_stream << fileOutput;
    out_stream.close();

    std::cout << "Data written to out stream and stream closed." << std::endl;

    auto end = std::chrono::system_clock::now();
    std::chrono::duration<double> elapsed = end - start;
    std::cout << "Finished reading and writing in " << elapsed.count() << " seconds." << std::endl;

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