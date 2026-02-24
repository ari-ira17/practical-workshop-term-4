import math
from algorithm import BloomFilter, BloomFilterCount

def test_builder_bf():
    bf_1 = BloomFilter(m=100, k=5)
    assert bf_1.m == 100
    assert bf_1.k == 5

    bf_2 = BloomFilter(n=1000, eps=50)
    true_m = int( - (bf_2.n * math.log(bf_2.eps)) / (math.log(2) ** 2))
    true_k = max(1, int((bf_2.m / bf_2.n) * math.log(2)))
    assert round(bf_2.m, 10) == round(true_m, 10)
    assert round(bf_2.k, 10) == round(true_k, 10)


def test_builder_bf_counter():
    bf_counter_1 = BloomFilter(m=100, k=5)
    assert bf_counter_1.m == 100
    assert bf_counter_1.k == 5

    bf_counter_2 = BloomFilter(n=1000, eps=50)
    true_m = int( - (bf_counter_2.n * math.log(bf_counter_2.eps)) / (math.log(2) ** 2))
    true_k = max(1, int((bf_counter_2.m / bf_counter_2.n) * math.log(2)))
    assert round(bf_counter_2.m, 10) == round(true_m, 10)
    assert round(bf_counter_2.k, 10) == round(true_k, 10)


def test_add_check_bf():
    bf = BloomFilter(m=100, k=5)
    bf.add('1')
    assert bf.check('1') == True
    assert bf.check('2') == False


def test_add_check_bf_counter():
    bf = BloomFilterCount(m=100, k=5)
    bf.add('cat')
    assert bf.check('cat') == True
    assert bf.check('dog') == False


def test_remove_bf_counter():
    bf_counter = BloomFilterCount(m=200, k=7)
    bf_counter.add('cat')
    assert bf_counter.check('cat') == True
    bf_counter.remove('cat')
    assert bf_counter.check('cat') == False 


def test_union_bf():

    bf_1 = BloomFilter(m=100, k=5)
    bf_1.add('1')   
    bf_1.add('2')  
    bf_1.add('4') 

    bf_2 = BloomFilter(m=100, k=5)
    bf_2.add('4')   
    bf_2.add('5')

    union = bf_1 + bf_2

    for el in ['1', '2', '4', '5']:
        assert union.check(el) == True

    assert union.check('8') == False


def test_union_bf_counter():
    bf_1 = BloomFilterCount(m=200, k=7)
    bf_1.add('cat')   
    bf_1.add('bird')  
    bf_1.add('dog') 

    bf_2 = BloomFilterCount(m=200, k=7)
    bf_2.add('dog')   
    bf_2.add('cow')

    union_counter = bf_1 + bf_2

    for el in ['cat', 'dog', 'bird', 'cow']:
        assert union_counter.check(el) == True

    assert union_counter.check('giraffe') == False


def test_crossing_bf():

    bf_1 = BloomFilter(m=100, k=5)
    bf_1.add('1')   
    bf_1.add('2')  
    bf_1.add('4') 

    bf_2 = BloomFilter(m=100, k=5)
    bf_2.add('4')   
    bf_2.add('5')
    
    crossing = bf_1 - bf_2
    assert crossing.check('4')
    for el in ['1', '2', '5']:
        assert crossing.check(el) == False


def test_crossing_bf_counter():

    bf_counter_1 = BloomFilterCount(m=200, k=7)
    bf_counter_1.add('cat')   
    bf_counter_1.add('bird')  
    bf_counter_1.add('dog') 

    bf_counter_2 = BloomFilterCount(m=200, k=7)
    bf_counter_2.add('dog')   
    bf_counter_2.add('cow')

    crossing = bf_counter_1 - bf_counter_2
    assert crossing.check('dog')
    for el in ['cat', 'bird', 'cow']:
        assert crossing.check(el) == False


test_builder_bf()
test_builder_bf_counter()
test_add_check_bf()
test_add_check_bf_counter()
test_remove_bf_counter()
test_union_bf()
test_union_bf_counter()
test_crossing_bf()
test_crossing_bf_counter()
