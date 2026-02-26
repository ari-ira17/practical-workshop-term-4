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
            self.p = math.ceil(2 * math.log2((1.04 / eps)))
        else:
            self.p = 12

        self.m = 2 ** self.p
        self.registers = [0] * self.m


    def process_element(self, value):
        hash_value = HashFunction.hash_function(value)
        register_index = hash_value & (self.m - 1)  # номер регистра
        remaining_hash = hash_value >> self.p

        if remaining_hash == 0:
            position = 0
        else:
            position = (remaining_hash & -remaining_hash).bit_length()      # ро
        
        self.registers[register_index] = max(self.registers[register_index], position)

    def estimate_cardinality(self):

        z = 1 / sum([2 ** (-reg) for reg in self.registers])

        if self.m == 16:
            a_m = 0.673
        elif self.m == 32:
            a_m = 0.697
        elif self.m == 64:
            a_m = 0.709
        else:
            a_m = (0.7213 / (1 + (1.079 / self.m)))

        E = a_m * (self.m ** 2) * z
        V = self.registers.count(0)

        if E < 2.5 * self.m and V > 0:
            n = self.m * math.log(self.m / V)
        elif E > (2 ** 32) / 30:
            n = (-(2 ** 32)) * math.log(1 - E / 2 ** 32)
        else: 
            n = E

        return(n)
    
    def hyperloglog_estimate(self, values):
        for val in values:
            self.process_element(val)

        cardinality = self.estimate_cardinality()

        return cardinality
    
    def __add__(self, other):
        if self.p == other.p:
            result = Hyperloglog(p=self.p)
            for i in range(self.m):
                result.registers[i] = max(self.registers[i], other.registers[i])
            return result
        else:
            print("Параметр р должен быть одинаковым")
