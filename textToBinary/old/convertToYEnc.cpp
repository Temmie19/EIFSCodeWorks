 
#include <iostream>
#include <fstream>
#include <vector>
#include <string.h>
#include <sstream>
#include <iterator>
#include <algorithm>
#include <array> 

std::string inPath = "example.ync";
std::string outPath;

bool convertToYEnc();

int main() {
    std::cout << "Please input file path:";
    std::cin >> inPath;
    outPath = inPath;
    outPath.erase(outPath.end()-11, outPath.end());
    convertToYEnc();

}

bool convertToYEnc(){
    //This will open the file
    std::ifstream in_stream(inPath, std::ifstream::in);

    if (!in_stream.good()) {
        std::cout << "Input stream to file " << inPath << " is not valid \n";
        return false;
    }

    std::ofstream out_stream(outPath ,std::ofstream::out);

    if (!out_stream.good()) {
        std::cout << "Output stream to file " << outPath << " is not valid \n";
        return false;
    }

    std::string line;
    std::string yencLine;
    std::stringstream currentHex;

    while(std::getline(in_stream, line)) {

        std::stringstream splitter(line);
        std::vector<std::string> hexVec(std::istream_iterator<std::string>{splitter}, std::istream_iterator<std::string>());

        for(int i = 0; i < hexVec.size(); i++){
            std::string currentChar;
            currentChar = hexVec[i];

            int charPos;
            int hexBuffer;
            char testChar;
            
            hexBuffer = std::stoi(currentChar, 0, 16);

            currentHex >> hexBuffer;
            charPos = hexBuffer / 130;

            yencLine.append("negative");
            currentHex.str(std::string());
            currentChar = "";
            charPos = 0;
            hexBuffer = 0;
        }
        out_stream << yencLine << std::endl;
        line = "";
        yencLine = "";
    }

    std::cout << "Conversion done! \n";

    return true;

}