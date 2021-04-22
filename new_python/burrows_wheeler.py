#!/usr/bin/python3

def burrows_wheeler(input):
    rotations = []
    one_rotation = input
    for x in range(len(input)):
        one_rotation = one_rotation[-1] + one_rotation [:-1]
        rotations.append(one_rotation)
        pass
    sorted_array = sorted(rotations)
    print("Data sorted lexicographically.")
    location = 0
    for i in range(len(sorted_array)):
        if(sorted_array[i] == input):
            location = i
            break
    transformation = ""
    for x in range(len(sorted_array)):
        sorted_array[x] = sorted_array[x][-1]
        transformation += sorted_array[x]
        pass
    if(len(transformation) == 16384):
        transformation += str(location) + " "
        print("Equal to 16384")
    else:
        transformation += " " + str(location)
        print("Not equal to 16384. ", len(transformation), " vs ", len(input))
    rotations.clear()

    return transformation