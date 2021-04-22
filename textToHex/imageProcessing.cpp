#include "lodepng.h"
#include "imageProcessing.hpp"
#include <iomanip>
#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <chrono> 
#include <string.h>
#include <cmath>

void writePNG(std::vector<std::string> hexValues, std::string fileName){
    auto start = std::chrono::system_clock::now();
    std::cout << "Converting from vector to image." << std::endl;
    int length = ceil(pow(hexValues.size(), 0.5));
    const unsigned w = length;
    const unsigned h = length * 1.05;
    std::vector<unsigned char> image;
    image.resize(w * h * 4);
    std::cout << "Image size calculated." << std::endl;
    int vecPos = 0;
    for(unsigned y = 0; y < h; y++)
        for(unsigned x = 0; x < w; x++) {
            //pixel start byte position in the new raw image
            unsigned newpos = 4 * y * w + 4 * x;
            if(vecPos < hexValues.size()){
                std::string hexString = hexValues[vecPos];
                vecPos++;
                image[newpos + 0] = (int)std::stoi(hexString.substr(0,2), nullptr, 16); //R
                image[newpos + 1] = (int)std::stoi(hexString.substr(2,2), nullptr, 16); //G
                image[newpos + 2] = (int)std::stoi(hexString.substr(4,2), nullptr, 16); //B
                image[newpos + 3] = (int)std::stoi(hexString.substr(6,2), nullptr, 16); //A
            }
            else{
                image[newpos + 0] = 255; //R;
                image[newpos + 1] = 255; //G
                image[newpos + 2] = 255; //B
                image[newpos + 3] = 255; //A
            }
    }
    std::cout << "Raw pixel data calculated. Pixels amount is: " << image.size() << std::endl;
    char filenameChar[fileName.size()+1];
    strcpy(filenameChar, fileName.c_str());

    auto end = std::chrono::system_clock::now();
    std::chrono::duration<double> elapsed = end - start;
    std::cout << "Finished image generation in " << elapsed.count() << " seconds." << std::endl;

    encodeWithState(filenameChar, image, w, h);

}

std::string readImage(std::string filePath){

    auto start = std::chrono::system_clock::now();

    std::cout << "Loading image to extract pixels." << std::endl;
    std::vector<unsigned char> png;
    std::vector<unsigned char> image; //the raw pixels
    unsigned w, h;

    //load and decode
    //unsigned error = lodepng::load_file(png, filePath);
    unsigned error = lodepng::decode(image, w, h, filePath);

    std::cout << "Decoded image into vector." << std::endl;
    int vecPos = 0;

    std::cout << "Image size calculated." << std::endl;

    std::vector<int> intVec;
    std::stringstream converter;
    std::string fileOutput = filePath + ".txt";
    std::ofstream out_stream(fileOutput, std::ofstream::out);

    for(int i = 0; i < image.size(); i++){
        converter << image[i];
    }
    out_stream << converter.str();

    /*for(unsigned y = 0; y < h; y++)
        for(unsigned x = 0; x < w; x++) {
            //pixel start byte position in the new raw image
            unsigned newpos = y * w + x;
            if(newpos < image.size()){
                
            }
    }*/

    for(int i = 0; i < intVec.size(); i++){
        converter << std::hex << intVec[i];
    }

    auto end = std::chrono::system_clock::now();
    std::chrono::duration<double> elapsed = end - start;
    std::cout << "Image converted to hex string in " << elapsed.count() << " seconds." << std::endl;

    return converter.str();

}


//The following function is more or less just copy and paste from the LodePNG example files. I take no credit designing this, as it belongs to Lode Vandevenne
void encodeWithState(const char* filename, std::vector<unsigned char>& image, unsigned width, unsigned height) {
    std::vector<unsigned char> png;
    auto start = std::chrono::system_clock::now();
    lodepng::State state; 
    state.encoder.filter_palette_zero = 0; //Try several filter types, including zero, allow trying them all on palette images too.
    state.encoder.add_id = false; //Don't add LodePNG version chunk to save more bytes
    state.encoder.zlibsettings.nicematch = 258; //Set this to the max possible, otherwise it can hurt compression
    state.encoder.zlibsettings.lazymatching = 1; //Definitely use lazy matching for better compression
    state.encoder.zlibsettings.windowsize = 32768; //Use maximum possible window size for best compression

    size_t bestsize = 0;
    bool inited = false;

    int beststrategy = 0;
    LodePNGFilterStrategy strategies[4] = { LFS_ZERO, LFS_MINSUM, LFS_ENTROPY, LFS_BRUTE_FORCE };
    std::string strategynames[4] = { "LFS_ZERO", "LFS_MINSUM", "LFS_ENTROPY", "LFS_BRUTE_FORCE" };
      // min match 3 allows all deflate lengths. min match 6 is similar to "Z_FILTERED" of zlib.
    int minmatches[2] = { 3, 6 };
    int bestminmatch = 0;

    int autoconverts[2] = { 0, 1 };
    std::string autoconvertnames[2] = { "0", "1" };
    int bestautoconvert = 0;

    int bestblocktype = 0;

    unsigned error;

    // Try out all combinations of everything
    for(int i = 0; i < 4; i++)   //filter strategy
    for(int j = 0; j < 2; j++)   //min match
    for(int k = 0; k < 2; k++)   //block type (for small images only)
    for(int l = 0; l < 2; l++) { //color convert strategy
        if(bestsize > 3000 && (k > 0 || l > 0)) continue; /* these only make sense on small images */
        std::vector<unsigned char> temp;
        state.encoder.filter_strategy = strategies[i];
        state.encoder.zlibsettings.minmatch = minmatches[j];
        state.encoder.zlibsettings.btype = k == 0 ? 2 : 1;
        state.encoder.auto_convert = autoconverts[l];
        error = lodepng::encode(temp, image, width, height, state);

        if(error){
            std::cout << "encoding error " << error << ": " << lodepng_error_text(error) << std::endl;
            return;
        }

        if(!inited || temp.size() < bestsize){
            bestsize = temp.size();
            beststrategy = i;
            bestminmatch = state.encoder.zlibsettings.minmatch;
            bestautoconvert = l;
            bestblocktype = state.encoder.zlibsettings.btype;
            temp.swap(png);
            inited = true;
        }
  }

    std::cout << "Chosen filter strategy: " << strategynames[beststrategy] << std::endl;
    std::cout << "Chosen min match: " << bestminmatch << std::endl;
    std::cout << "Chosen block type: " << bestblocktype << std::endl;
    std::cout << "Chosen auto convert: " << autoconvertnames[bestautoconvert] << std::endl;
    
    if(!error) lodepng::save_file(png, filename);

    auto end = std::chrono::system_clock::now();
    std::chrono::duration<double> elapsed = end - start;
    std::cout << "Finished image compression and writing in " << elapsed.count() << " seconds." << std::endl;

    //if there's an error, display it
    if(error) std::cout << "Encoder error \"" << error << "\": "<< lodepng_error_text(error) << std::endl;
}

//Same as above
std::vector<unsigned char> decodeTwoSteps(const char* filename) {
  std::vector<unsigned char> png;
  std::vector<unsigned char> image; //the raw pixels
  unsigned width, height;

  //load and decode
  unsigned error = lodepng::load_file(png, filename);
  if(!error) error = lodepng::decode(image, width, height, png);
  image.insert(image.begin(), height);
  image.insert(image.begin(), width);

  //if there's an error, display it
  if(error) std::cout << "decoder error " << error << ": " << lodepng_error_text(error) << std::endl;

  //the pixels are now in the vector "image", 4 bytes per pixel, ordered RGBARGBA..., use it as texture, draw it, ...
  return image;
}