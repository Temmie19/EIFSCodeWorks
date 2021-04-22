#include <iomanip>
#include <iostream>
static void usage(){
    std::cout << "Usage for conversion: " << std::endl <<
    "-e or --encode      Encode a file into an image" << std::endl <<
    "-d or --decode      Decode an image to get the original file" << std::endl <<
    "-h or --help        Show this dialog" << std::endl;
};

void encodeFile();
void decodeFile();