#!/usr/bin/python3

import random, time
start = time.time
array_one = []
array_two = []
original_string = "in the game, a spaceship crew tries to keep the ship running.\
    however, there are 'imposters' among them attempting to hijack the ship and \
    destroy the occupants. doesn't this sound familiar? on september 11th, 2001.."
mixed_string = ""
new_string = ""

def convert_to():
    
    pass
random.seed(0)
for i in range(256):
    random.seed(i)
    rand_int = random.randrange(255)
    while((rand_int in array_one) == True):
        rand_int = (rand_int + 1) % 256
    array_one.append(rand_int)
array_two = array_one[128:]
for i in range(128):
    random.seed(i+128)
    rand_int = random.randrange(255)
    while((rand_int in array_two) == True):
        rand_int = (rand_int + 1) % 256
    array_two.append(rand_int)
end = time.time
print((end - start))
print(array_two[:128] == array_one[128:])
#array_one.sort()
print(array_one[128:])
print(array_two[:128])

