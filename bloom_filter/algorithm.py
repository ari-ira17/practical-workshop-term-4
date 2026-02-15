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
            self.n = n
            self.eps = eps

            self.m =  int( - (self.n * math.log(eps)) / (math.log(2) ** 2))
            self.k = max(1, int((self.m / self.n) * math.log(2)))
    
        self.hash_functions = [HashFunction(seed = i) for i in range(self.k)]  
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


class BloomFilterCount(BloomFilter):

    def __init__(self, m=None, k=None, n=None, eps=None):
        super().__init__(m, k, n, eps)

        self.counter_array = [0] * self.m


    def add(self, element): 

        for hash_f in self.hash_functions:
            value = hash_f.new_hash_f(element)
            index = value % self.m
            self.counter_array[index] += 1


    def check(self, element):

        for hash_f in self.hash_functions:
            value = hash_f.new_hash_f(element)
            index = value % self.m

            if self.counter_array[index] == 0: 
                return False
                
        return True
            
    
    def remove(self, element):
        
        for hash_f in self.hash_functions:
            value = hash_f.new_hash_f(element)
            index = value % self.m
            self.counter_array[index] = max(0, self.counter_array[index] - 1)   
