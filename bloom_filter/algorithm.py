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
    

    def __add__(self, other):

        if self.m == other.m and self.k == other.k:
            union = BloomFilter(m=self.m, k=self.k)
            union.bit_array = [False] * union.m

            for i in range (union.m):
                union.bit_array[i] = self.bit_array[i] or other.bit_array[i]

            return union
    
    
    def __sub__(self, other):

        if self.m == other.m and self.k == other.k:
            crossing = BloomFilter(m=self.m, k=self.k)
            crossing.bit_array = [False] * crossing.m

            for i in range(crossing.m):
                crossing.bit_array[i] = self.bit_array[i] and other.bit_array[i]

            return crossing


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


    def __add__(self, other):

        if self.m == other.m and self.k == other.k:
            union = BloomFilterCount(m=self.m, k=self.k)
            union.counter_array = [0] * union.m

            for i in range (union.m):
                union.counter_array[i] = max(self.counter_array[i], other.counter_array[i])

            return union
        
    def __sub__(self, other):

        if self.m == other.m and self.k == other.k:
            crossing = BloomFilterCount(m=self.m, k=self.k)
            crossing.counter_array = [0] * crossing.m

            for i in range (crossing.m):
                crossing.counter_array[i] = min(self.counter_array[i], other.counter_array[i])

            return crossing
