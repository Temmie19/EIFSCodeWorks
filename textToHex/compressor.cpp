#include "compressor.hpp"
#include <sstream>
#include <iostream>
#include <fstream>
#include <iomanip>
#include <bits/stdc++.h>
#include <chrono> 
#include <vector>


std::string burrowsWheeler(std::string fileInput){
    std::string transformation;
    std::string oneRotation = fileInput;
    std::vector<std::string> rotations;
    for(int i = 0; i < fileInput.length(); i++){
        std::rotate(oneRotation.begin(), oneRotation.begin()+1, oneRotation.end());
        rotations.push_back(oneRotation);
    }
    
    std::sort(rotations.begin(), rotations.end());

    //std::vector<std::string>::iterator it = std::find(rotations.begin(), rotations.end(), fileInput);
    int index; // = it - rotations.begin();
    for(int i = 0; i < rotations.size(); i++){
        if(rotations[i] == fileInput){
            index = i;
            i += rotations.size();
        }
    }

    for(int i = 0; i < rotations.size(); i++){
        transformation += rotations[i].back();
    }

    /*std::string transformBuff;
    char currentChar;
    for(int i = 0; i < transformation.size(); i++){
        if(currentChar != transformation[i]){
            currentChar = transformation[i];
            transformBuff += "0A0C0A0C0A0C";
            transformBuff += currentChar;
        }
        else{
            transformBuff += '0';
        }
    }

    transformBuff.erase(transformBuff.begin(),transformBuff.begin() + 8);*/

    std::cout << "Index is " << index << ". ";

    //transformation += "TemmieBWTransformSplitter";
    std::stringstream converter;

    converter << index;

    transformation +=  "TemmieBWTransformSplitter";
    transformation += converter.str();
    transformation += "TemmieEndOfChunk";

    rotations.clear();

    return transformation;
}

std::string reverter(std::string fileInput){

    std::stringstream converter;
    int eofMarker = fileInput.find("TemmieBWTransformSplitter") + 25;
    int index = std::stoi(fileInput.substr(eofMarker, fileInput.size() - eofMarker));
    std::cout << "Index is " << index << ". ";
    fileInput.erase(fileInput.begin() + eofMarker - 25, fileInput.end());

    /*char replaceBuffer;
    std::string mtfDecodeBuffer;
    int lastNot;
    for(int i = 0; i < fileInput.size(); i++){
        if(fileInput.substr(i,6) == "\n\f\n\f\n\f"){
            lastNot = fileInput.substr(0, i).find_last_not_of('0');
            replaceBuffer = fileInput[lastNot];
            for(int i = 0; i < mtfDecodeBuffer.size() - lastNot; i++){
                mtfDecodeBuffer[lastNot + i] = replaceBuffer;
            }
            i += 5;
        }
        else{
            mtfDecodeBuffer += fileInput[i];
        }
    }*/
    std::vector<char> sorter;
    std::string lexicoList;
    for(int i = 0; i < fileInput.length(); i++){
        sorter.push_back(fileInput[i]);
    }

    std::sort(sorter.begin(), sorter.end());
    for(int i = 0; i < sorter.size(); i++){
        lexicoList += sorter[i];
    }
    std::cout << "Data sorted lexicographically. " << std::endl;
    char currentChar = fileInput[index];
    char secondChar = lexicoList[index];
    std::string transformation;
    size_t itteration = 0;
    size_t inputPos = 0;
    size_t itterCount = -1;
    std::string lineBuffer;
    std::string test;
    for(int i = 0; i < fileInput.size(); i++){
        transformation += currentChar;
        itteration = index - lexicoList.find(secondChar);
        std::cout << "This is the " << itteration << " itteration. ";
        /*for(int i = 0; i < itteration; i++){
            inputPos = fileInput.find(secondChar, inputPos + 1);
        }*/
        std::stringstream subString(fileInput);
        while(getline(subString, lineBuffer, secondChar)){
            test += lineBuffer;
            test += secondChar;
            itterCount++;
            if(itterCount == itteration){
                break;
            }
        }
        index = lineBuffer.length();
        std::cout << "Index is " << index << ". ";
        inputPos = 0;
        currentChar = fileInput[index];
        secondChar = lexicoList[index];
        itteration = 0;
        std::cout << i << " character(s) selected." << std::endl;
    }
    std::rotate(transformation.begin(), transformation.begin()+1, transformation.end());

    /*std::vector<int> lexiLess;
    char charCounter;

    for(int i = 0; i < lexicoList.size(); i++){
        if(charCounter != lexicoList[i]){
            charCounter = lexicoList[i];
            lexiLess.push_back(1);
        }
        else{
            lexiLess.back()++;
        }
    }

    std::cout << "First unique character has " << lexiLess[0] << " itterations." << std::endl;

    for(int i = 0; i < lexiLess.size(); i++){
        lexicoList.erase(lexicoList.begin()+i, lexicoList.begin()+i+lexiLess[i]-1);
    }
    std::cout << "129th unique character is " << sorter[128] << " out of 256 possible." << std::endl;

    int lexiCounter = fileInput.size();
    for(int i = lexiLess.size() - 1; i >= 0; i--){
        lexiLess[i] = lexiCounter - lexiLess[i];
        lexiCounter = lexiLess[i];
    }

    std::cout << "First unique character has " << lexiLess[0] << " lexicographically less characters." << std::endl;
    std::cout << "Second unique character has " << lexiLess[1] << " lexicographically less characters." << std::endl;

    char currentChar = fileInput[index];
    std::string transformation;
    //size_t origPosition = index;
    size_t itteration = -1;
    std::string lineBuffer;

    for(int i = 0; i < fileInput.length(); i++){
        transformation.insert(transformation.begin(), currentChar);
        / *for(int i = 0; i < index - 1; i++){
            if(fileInput.substr(0, index-1)[i] == currentChar){
                itteration++;
            }
        }* /
        std::stringstream subString(fileInput.substr(0, index));
        while(getline(subString, lineBuffer, currentChar)){
            itteration++;
        }
        std::cout << "This is the " << itteration << " itteration of " << currentChar << ". ";
        index = lexiLess[lexicoList.find(currentChar)] + itteration;
        std::cout << "The index is " << index << "." << std::endl;
        currentChar = fileInput[index];
        itteration = -1;
    }*/

    
    return transformation;
}