import random

class RandomOverlap:
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



def mix(file_path):
    r = RandomOverlap()
    with open(file_path, 'rb') as input_file,\
         open(f'{file_path}.mixed', 'wb') as output_file:
        while data := input_file.read(256):
            mixer = next(r)
            new_data = [mixer[i] for i in data]
            output_file.write(bytes(new_data))

    
def unmix(file_path):
    r = RandomOverlap()
    with open(file_path, 'rb') as input_file,\
         open(f'{file_path}.unmixed', 'wb') as output_file:
        while data := input_file.read(256):
            mixer = next(r)
            new_data = [mixer.index(i) for i in data]
            output_file.write(bytes(new_data))


def main():
    mix("/home/temmie19/codes/testing/mafiaTownIntro.mp3")
    unmix("/home/temmie19/codes/testing/mafiaTownIntro.mp3.mixed")


if __name__ == '__main__':
    main()