import hashlib
import math

# .encode() - преобразует строку в последовательность байтов (в кодировке UTF-8 по умолчанию).
# Потому что криптографические хеш-функции работают только с байтами, а не со строками
class HashFunction:
    def hash_function(value):
        hash_value = hashlib.sha256(str(value).encode()).digest()
        return int.from_bytes(hash_value, byteorder='big')
    

class Hyperloglog:
    def __init__(self, p=None, eps=None):

        if p is not None:
            self.p = p
        elif eps is not None:
            self.p = int(2 * math.log2((1.04 / eps)))
        else:
            self.p = 12

        self.m = 2 ** self.p
        self.registers = [0] * self.m
        self.r = 0
        self.tail = 0

    def rho(self, value):
        hash_value = HashFunction.hash_function(value)
        

        


