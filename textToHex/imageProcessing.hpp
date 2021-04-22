#include <iomanip>
#include <vector>

void writePNG(std::vector<std::string> hexValues, std::string fileName);
void encodeWithState(const char* filename, std::vector<unsigned char>& image, unsigned width, unsigned height);
std::vector<unsigned char> decodeTwoSteps(const char* filename);
std::string readImage(std::string filePath);