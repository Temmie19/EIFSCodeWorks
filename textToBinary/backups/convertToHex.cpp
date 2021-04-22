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

std::string convertToHex();

std::vector<std::string> split(const std::string &string, const char delim);

int main() {
    std::cout << "Please input file path:";
    std::cin >> inPath;
    outPath = inPath;
    outPath.append("-output.txt");
    convertToHex();

}

std::string convertToHex() {
    std::ifstream in_stream(inPath, std::ifstream::in|std::ios::binary);
    if (!in_stream.good()) {
        std::cout << "Input stream to file " << inPath << " is not valid." << std::endl;
    }

    std::ofstream out_stream(outPath, std::ofstream::out);
    if (!out_stream.good()) {
        std::cout << "Output stream to file " << outPath << " is not valid." << std::endl;
    }
    
    auto start = std::chrono::system_clock::now();

    std::cout << "In and out streams loaded." << std::endl;

    std::vector<std::string> location = split(inPath, '/');
    out_stream << location.back() << std::endl;

    in_stream.seekg(0, in_stream.end);
    int16_t fileLength = in_stream.tellg();
    in_stream.seekg(0,in_stream.beg);

    std::cout << "In stream location and file size calculated." << std::endl;

    std::string fileBuffer;
    std::string fullFile;
    while(getline(in_stream, fileBuffer)){
        fullFile += fileBuffer;
        fullFile += '\n';
    }

    std::cout << "In stream read." << std::endl;

    in_stream.close();

    std::cout << "In stream closed." << std::endl;

    std::stringstream conversion;

    conversion << std::hex;
    int counter = 0;
    for(int32_t i = 0; i < fullFile.length(); i++){
        int32_t z = fullFile[i]&0xff;
        conversion << std::setw(2) << std::setfill('0') << z;
        if(counter < 3){
            counter++;
        }
        else{
            counter = 0;
            conversion << " ";
        }
    }

    std::cout << "Data converted to hex." << std::endl;

    std::string fileOutput = conversion.str();

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