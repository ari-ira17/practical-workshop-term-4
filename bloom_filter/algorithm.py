import math
import random
import hashlib


class HashFunction:

    def __init__(self, seed=None):
        
        if seed is None:
            self.seed = random.randint(0, 17_000)
        else:
            self.seed = seed

    def new_hash_f(self, x):
        return (int(hashlib.md5(x.encode('utf-8')).hexdigest(), 16)+ self.seed) % (2 ** 30) 


class BloomFilter:

    def __init__(self, m=None, k=None, n=None, eps=None):

        if m != None and k != None:
            self.m = m
            self.k = k
        
        elif n != None and eps != None:
            self.m =  int( - (n * math.log(eps)) / (math.log(2) ** 2))
            self.k = int((self.m / n) * math.log(2))
    
        self.hash_functions = [HashFunction(seed = i) for i in range(self.k)]   # создаем k объектов класса и кладем их в список
        self.bit_array = [False] * self.m


    def add(self, element): 

        for hash_f in self.hash_functions:
            value = hash_f.new_hash_f(element)
            index = value % self.m
            self.bit_array[index] = True


    def check(self, element):

        for hash_f in self.hash_functions:
            value = hash_f.new_hash_f(element)
            index = value % self.m

            if self.bit_array[index] == False: 
                return False
                
        return True

bloom_filter = BloomFilter(m=100, k=1000)
bloom_filter.add('meow')
print(bloom_filter.check('meow'))