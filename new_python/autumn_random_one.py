import random

"""class RandomOverlap:
    def __init__(self, n=256):
        self.r = random.Random()
        self.r.seed(0)
        initial = self.random_unique(n)
        self.current = initial
        self.half_length = len(initial) // 2
        self.i1, self.i2 = initial[:self.half_length], initial[self.half_length:]

    def random_unique(self, n):
        lst = list(range(n))
        self.r.shuffle(lst)
        return lst

    def __next__(self):
        result = self.i1 + self.i2
        self.i1, self.i2 = self.i2, self.i1
        self.r.shuffle(self.i2)
        return result

    def __iter__(self):
        return self


r = RandomOverlap()
print(next(r))
r = RandomOverlap()
print(next(r))
r = RandomOverlap()
print(next(r))
r = RandomOverlap()
print(next(r))
r = RandomOverlap()
print(next(r))
"""


r = random.Random()
r.seed(0)

def init_process(input:str):
    initial = [input[i] for i in range(len(input))]
    r.shuffle(initial)
    half_length = len(initial) // 2
    half_one, half_two = initial[:half_length], initial[half_length:]
    return half_one, half_two

half_one, half_two = init_process("in the game, a spaceship crew tries to keep \
    the ship running. however, there are 'imposters' among them attempting to \
    hijack the ship and destroy the occupants. doesn't this sound familiar? on september 11th, 2001..".encode())

print(half_one)
print(half_two)

def next_result():
    global half_one, half_two
    result = half_one + half_two
    half_one, half_two = half_two, half_one
    r.shuffle(half_two)
    return result
next_result()
print(half_one)
print(half_two)
next_result()
print(half_one)
print(half_two)