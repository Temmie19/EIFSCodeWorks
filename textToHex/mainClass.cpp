#include "converter.hpp"
#include "mainClass.hpp"
#include "imageProcessing.hpp"
#include <iomanip>
#include <fstream>
#include <vector>

bool isEncoding;
std::string fileInput;

int main(int argc, char* argv[]){
    if(argc < 2){
        std::cout << "Please use -e or -d and a file destination or use -h for more info." << std::endl;
        return 1;
    }
    else{
        if(std::string(argv[1]) == "-e" || std::string(argv[1]) == "--encode"){
            isEncoding = true;
            fileInput = argv[2];
        }
        else if (std::string(argv[1]) == "-d" || std::string(argv[1]) == "--decode"){
            isEncoding = false;
            fileInput = argv[2];
        }
        else if(std::string(argv[1]) == "-h" || std::string(argv[1]) == "--help"){
            usage();
            return 1;
        }
        else{
           std::cout << "Please use -e or -d and a file destination or use -h for more info." << std::endl;
           return 1; 
        }
    }
    if(isEncoding == true){
        encodeFile();
    }
    else{
        decodeFile();
    }
}

void encodeFile(){
    std::vector<std::string> hexcode = convertToHex(fileInput);
    std::string fileOutput = fileInput;
    fileOutput.append(".png");
    std::vector<std::string> location = split(fileInput, '/');
    writePNG(hexcode, fileOutput);
    
}

void decodeFile(){
    std::string hexString = readImage(fileInput);
    std::string fileOutput;
    std::vector<std::string> location = split(fileInput, '/');
    for(int i = 0; i < location.size() - 1; i++){
        fileOutput += location[i];
        fileOutput += "/";
    }
    std::vector<std::string> binaryData = convertFromHex(hexString);
    fileOutput += binaryData[0];
    std::ofstream out_stream(fileOutput, std::ofstream::out|std::ios::binary);
    if (!out_stream.good()) {
        std::cout << "Output stream to file " << fileOutput << " is not valid \n";
    }
    out_stream << binaryData[1];
    out_stream.close();
}
