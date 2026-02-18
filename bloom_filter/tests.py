from algorithm import BloomFilter


def test_union(bloom_filter_1, bloom_filter_2):
    union = bloom_filter_1 + bloom_filter_2
    for el in ['1', '2', '4', '5']:
        assert union.check(el) == True
    assert union.check('8') == False


def test_crossing(bloom_filter_1, bloom_filter_2):
    crossing = bloom_filter_1 - bloom_filter_2
    assert crossing.check('4')
    for el in ['1', '2', '5']:
        assert crossing.check(el) == False


bf_1 = BloomFilter(m=100, k=5)
bf_1.add('1')   
bf_1.add('2')  
bf_1.add('4') 

bf_2 = BloomFilter(m=100, k=5)
bf_2.add('4')   
bf_2.add('5')  

test_union(bf_1, bf_2)
test_crossing(bf_1, bf_2)
