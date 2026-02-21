from algorithm import BloomFilter
import string, math
from random import randint, choices


def generate_items(count, start=17_000, end=17_000_00):
    items = set()
    while len(items) < count:
        items.add(str(randint(start, end)))

    return list(items)


def generate_lines(count, lenght):
    return [''.join(choices(string.ascii_letters, k=lenght)) for _ in range(count)]


def bloom_filter_test_num(n, eps, num_of_attemps, fill_percent):

    total_false_positive = 0
    num_to_add = int(fill_percent * n)

    for attempt in range(num_of_attemps):

        bloom_filter = BloomFilter(n=n, eps=eps)

        items_to_add = generate_items(num_to_add)
        items_to_check = generate_items(num_to_add, start=17_002, end=18_000_000)

        for item in items_to_add:
            bloom_filter.add(item)

        false_positive = 0

        for item in items_to_check:
            if item not in items_to_add and bloom_filter.check(item):
                false_positive += 1

        false_positive_rate = false_positive / len(items_to_check)
        total_false_positive += false_positive_rate
        print(f"Попытка №{attempt + 1}: ложные срабатывания составляют {round(false_positive_rate, 2)}%")

    avg_rate = total_false_positive / num_of_attemps
    print(f"Средний % ложных срабатываний при {round(fill_percent*100, 2)}% наполненности: {round(avg_rate*100, 2)}%")

    return avg_rate


def bloom_filter_test_str(n, eps, num_of_attemps, fill_percent=0.25):

    total_false_positive = 0
    num_to_add = int(fill_percent * n)

    for attempt in range(num_of_attemps):

        bloom_filter = BloomFilter(n=n, eps=eps)

        items_to_add = generate_lines(count=num_to_add, lenght=10)
        items_to_check = generate_lines(count=num_to_add, lenght=10)

        for item in items_to_add:
            bloom_filter.add(item)

        false_positive = 0

        for item in items_to_check:
            if item not in items_to_add and bloom_filter.check(item):
                false_positive += 1

        false_positive_rate = false_positive / len(items_to_check)
        total_false_positive += false_positive_rate
        print(f"Попытка №{attempt + 1}: ложные срабатывания составляют {round(false_positive_rate, 2)}%")

    avg_rate = total_false_positive / num_of_attemps
    print(f"Средний % ложных срабатываний при {round(fill_percent*100, 2)}% наполненности: {round(avg_rate*100, 2)}%")

    return avg_rate


n = 15_000
eps = 0.5 
m =  int( - (n * math.log(eps)) / (math.log(2) ** 2))
k = max(1, int((m / n) * math.log(2)))
eps = (1 - math.exp(-(k*n) / m ) ) ** k

for fill in [0.25, 0.5, 0.75, 0.95]:
    print(f"\n Наполненность {round(fill*100, 2)}% (числа)")
    bloom_filter_test_num(n=15_000, eps=0.5, num_of_attemps=5, fill_percent=fill)
    print(f"\n Наполненность {round(fill*100, 2)}% (строки)")
    bloom_filter_test_str(n=15_000, eps=0.5, num_of_attemps=5, fill_percent=fill)

print(f"\n m = {int(m)}, k = {(k)}, eps = {round(eps, 3) * 100}%")
