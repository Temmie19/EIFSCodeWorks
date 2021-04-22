#include "converter.hpp"
#include "compressor.hpp"
#include <vector>
#include <sstream>
#include <iomanip>
#include <bits/stdc++.h>
#include <chrono> 
#include <string>
#include <math.h>


std::vector<std::string> convertToHex(std::string fileLocation) {

    std::ifstream in_stream(fileLocation, std::ifstream::in|std::ios::binary);
    if (!in_stream.good()) {
        std::cout << "Input stream to file " << fileLocation << " is not valid \n";
    }
    
    auto start = std::chrono::system_clock::now();

    std::cout << "In stream loaded." << std::endl;

    std::string fileBuffer;
    std::string fullFile;
    while(getline(in_stream, fileBuffer)){
        fullFile += fileBuffer;
        fullFile += '\n';
    }

    std::cout << "In stream read." << std::endl;

    in_stream.close();

    std::cout << "In stream closed." << std::endl;
    int divider = floor(fullFile.size()/65536);
    std::cout << "There will be " << divider + 1 << " transformation(s) made." << std::endl;

    std::string transformed;
    std::string buffer;
    int checker = 0;
    for(int i = 0; i < divider + 1; i++){
        if(i < (divider)){
            buffer = burrowsWheeler(fullFile.substr(i * (65536 - 1), 65536));
            //std::cout << "Rotation " << i+1 << " made." << std::endl;
        }
        else{
            buffer = burrowsWheeler(fullFile.substr(i * (65536 - 1), fullFile.size() % 65536));
            std::cout << "Final transformation. ";

        }
        std::cout << "Buffer length is " << buffer.size() << std::endl;
        if(checker < 2){
            checker++;
        }
        transformed += buffer;
    }

    transformed += "TemmieBigBrainEndOfFileMarker123";

    std::vector<std::string> location = split(fileLocation, '/');

    std::string fileName = location.back();
    fileName += '\n';

    std::cout << "File name calculated." << std::endl;

    transformed.insert(0, fileName);

    std::cout << "File name added." << std::endl;

    std::stringstream conversion;

    conversion << std::hex;
    std::vector<std::string> storedHex;
    int counter = 0;
    for(int i = 0; i < transformed.size(); i++){
        int z = transformed[i]&0xff;
        conversion << std::setw(2) << std::setfill('0') << z;
        if(counter < 3){
            counter++;
        }
        else{
            counter = 0;
            storedHex.push_back(conversion.str());
            conversion.str(std::string());
        }
    }

    /*for(int32_t i = 0; i < transformed.size(); i++){
        int32_t z = transformed[i]&0xff;
        conversion << std::setw(2) << std::setfill('0') << z;
    }

    std::ofstream out_stream(fileLocation+".txt", std::ofstream::out);
    if (!out_stream.good()) {
        std::cout << "Input stream to file " << fileLocation << " is not valid \n";
    }

    std::stringstream eof;
    std::string eofMarker = "TemmieBigBrainEndOfFileMarker123";
    for(int32_t i = 0; i < eofMarker.size(); i++){
        int32_t z = eofMarker[i]&0xff;
        eof << std::setw(2) << std::setfill('0') << std::hex << z;
    }
    //transformed += eof.str();
    conversion << eof.str();*/

    if(storedHex.back().size() % 8 != 0){
        std::cout << "Not a 0 remainder!" << std::endl;
        for(int i = 0; i < storedHex.back().size() % 8; i++){
           //transformed.insert(transformed.end(), 'F');
           storedHex.back() += 'F'; 
        }
    }

    //out_stream.close();

    std::cout << "Data converted to hex." << std::endl;

    auto end = std::chrono::system_clock::now();
    std::chrono::duration<double> elapsed = end - start;
    std::cout << "Finished read and conversion in " << elapsed.count() << " seconds." << std::endl;

    std::vector<std::string> test;

    return storedHex;

}

std::vector<std::string> convertFromHex(std::string hexString) {
    auto start = std::chrono::system_clock::now();

    int eofMarker = hexString.find("TemmieBigBrainEndOfFileMarker");
    std::cout << "End of file marker found at position: " << eofMarker << "." << std::endl;
    hexString.erase(hexString.begin() + eofMarker, hexString.end());
    std::cout << "Extranious data erased." << std::endl;

    std::string fileName; 
    getline(std::stringstream(hexString), fileName);
    hexString.erase(hexString.begin(), hexString.begin() + fileName.size());
    std::cout << "File name is " << fileName << "." << std::endl;



    std::vector<std::string> chunkSizes;
    int lastPosition = 0;
    std::ofstream out_stream("/home/temmie19/codes/testing/output.txt", std::ofstream::out);
    out_stream << hexString;
    
    for(int i = 0; i < hexString.size(); i++){
        if(hexString.substr(i,16) == "TemmieEndOfChunk"){
            chunkSizes.push_back(hexString.substr(lastPosition, i));
            lastPosition = i + 16;
            //chunkSizes.back().erase(chunkSizes.back().end() - 16, chunkSizes.back().end());
        }
    }
    chunkSizes[0].erase(0, 1);

    std::string transformed;
    std::string buffer;
    std::cout << "There will be " << chunkSizes.size() << " transformation(s) made." << std::endl;
    for(int i = 0; i < chunkSizes.size(); i++){
        std::cout << "chunkSizes[" << i << "] is " << chunkSizes[i].size() << "." << std::endl;
        out_stream << chunkSizes[i] << '\n';
        buffer = reverter(chunkSizes[i]);
        std::cout << "Chunk read. ";
        transformed += buffer;
        std::cout << "Buffer length is " << buffer.size() << std::endl;
    }


    std::cout << "Data converted from hex and loaded into string." << std::endl;

    std::stringstream hexStream(transformed);
    std::string fileBuffer;
    std::string fullFile;
    std::stringstream intBuffer;
    int lineCounter = 0;
    while(getline(hexStream, fileBuffer)){
        fullFile += fileBuffer + '\n';
    }

    std::cout << "Full file put into string." << std::endl;

    std::vector<std::string> bothStrings = {fileName, fullFile};

    auto end = std::chrono::system_clock::now();
    std::chrono::duration<double> elapsed = end - start;
    std::cout << "Finished conversion to string in " << elapsed.count() << " seconds." << std::endl;

    return bothStrings;

}

std::string getFilename(std::string hexNameStream){
    std::ifstream in_stream(hexNameStream, std::ifstream::in);
    if (!in_stream.good()) {
        std::cout << "Input stream to file " << hexNameStream << " is not valid \n";
    }
    std::string nameBuffer;
    getline(in_stream, nameBuffer);
    in_stream.close();
    return nameBuffer;
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