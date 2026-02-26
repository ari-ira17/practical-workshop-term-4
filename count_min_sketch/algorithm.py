import math
import hashlib


class HashFunction:
    def new_hash_f(x, i):
        hash_hex = hashlib.sha256(str(x).encode('utf-8')).hexdigest()
        return int(hash_hex, 16) + i
        

class CountMinSketch:
    def __init__(self, eps, delta):
        self.eps = eps
        self.delta = delta
        self.d = math.ceil((math.log(1 / delta)))
        self.w = math.ceil(math.e / eps)
        self.matrix = [[0] * self.w for _ in range(self.d)]

    def update(self, value):
        for i in range(self.d):
            hash_value = HashFunction.new_hash_f(x=value, i=i) 
            index = hash_value % self.w
            self.matrix[i][index] += 1

    def frequency(self, element):
        frequency = float('inf')

        for i in range(self.d):
            hash_value = HashFunction.new_hash_f(x=element, i=i) 
            index = hash_value % self.w
            frequency = min(frequency, self.matrix[i][index])

        return frequency
    
    def __add__(self, other):
        if self.eps == other.eps and self.delta == other.delta:
            union = CountMinSketch(eps=self.eps, delta=self.delta)

            for i in range(union.d):
                for j in range(union.w):
                    union.matrix[i][j] = self.matrix[i][j] + other.matrix[i][j]

            return union

        else: 
            print("Значения eps и delta должны совпадать.")
