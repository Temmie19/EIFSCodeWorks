 
#include <iostream>
#include <fstream>
#include <vector>
#include <string.h>
#include <sstream>
#include <algorithm>
#include <iomanip>

std::string inPath = "example.ync";
std::string outPath;


bool listChars();

int main() {
    std::cout << "Please input file path:";
    std::cin >> inPath;
    outPath = inPath;
    outPath.append("-output.txt");
    listChars();

}

bool listChars(){
    //This will open the file
    std::ifstream in_stream(inPath, std::ifstream::in);

    //Check if the input file is valid
    if (!in_stream.good()) {
        std::cout << "Input stream to file " << inPath << " is not valid \n";
        return false;
    }

    std::ofstream out_stream(outPath ,std::ofstream::out);

    //Check if the output file is valid
    if (!out_stream.good()) {
        std::cout << "Output stream to file " << outPath << " is not valid \n";
        return false;
    }
    
    std::string line;
    std::stringstream currentChar;
    std::vector<std::string> charList = {};
    std::vector<int>::iterator it;

    //While there are still lines to be read, convert each character
    //of a line to its hexidecimal
    while(std::getline(in_stream, line)) {
        for(int i = 0; i < line.length(); i++){
            currentChar << line[i];
            auto it = std::find(charList.begin(), charList.end(), currentChar.str());
            if(it == charList.end()){
                charList.push_back(currentChar.str());
                std::cout << "Unique char " << currentChar.str() << " found!" << std::endl;
            }
            currentChar.str(std::string());
        }
        line = "";
    }
    
    std::cout << "Now compiling to file!" << std::endl;
    
    for(int i = 0; i < charList.size(); i++){
        out_stream << charList[i] << " = " << i + 1 << std::endl;
    }

    std::cout << "Now compiling to vector!" << std::endl;
    out_stream << "std::array<std::string, 254> charList = {";
    for(int i = 0; i < charList.size(); i++){
        out_stream << "\"" << charList[i] << "\", ";
    }
    out_stream << "};" << std::endl;

    std::cout << "Operations complete! \n";

    return true;

}