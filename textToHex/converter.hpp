#include <vector>
#include <iomanip>

std::vector<std::string> convertToHex(std::string fileLocation);
std::vector<std::string> convertFromHex(std::string fileLocation);

std::string getFilename(std::string hexNameStream);

std::vector<std::string> split(const std::string &string, const char delim);