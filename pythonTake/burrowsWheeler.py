#!/usr/bin/python3

def burrowsWheeler(input):
    rotations = []
    oneRotation = input + "+"
    for x in input:
        oneRotation = oneRotation[-1] + oneRotation [:-1]
        rotations.append(oneRotation)
        pass
    sortedArray = sorted(rotations)
    print("Data sorted lexicographically.")
    
    transformation = ""
    for x in range(len(sortedArray)):
        buffer = sortedArray[x]
        transformation += buffer[-1]
        pass
    transformation += "/"
    rotations.clear()

    return transformation