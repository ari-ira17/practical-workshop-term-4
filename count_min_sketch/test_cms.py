import sys
import os
import random
from datetime import datetime
from collections import Counter
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from hyperloglog.test_hll import date_gen

from count_min_sketch.cms_algorithm import CountMinSketch


def test_cms_threads():
    threads = [25_000, 200_000]

    for thread in threads:
        random.seed(thread / 1000)
        cms = CountMinSketch(eps=0.01, delta=0.01)
        gen = date_gen()
        seen = []

        for i in range(thread):
            date = next(gen)
            cms.update(date)
            seen.append(date)

        # frequency = cms.frequency(datetime(2026, 2, 26))
        true_freq = Counter(seen)
        for key, value in true_freq.items():
            frequency = cms.frequency(key)
            rel_error = abs(value - frequency) / thread
            print(f"{thread}: дата {key} добавлена {value} раз")
            print(f"{thread}: оценка даты {key} составляет {frequency}")
            print(f"Погрешность составялет {rel_error}")

        assert abs(value - frequency) <= cms.eps * thread

def test_cms_union():
    cms_1 = CountMinSketch(eps=0.01, delta=0.01)
    cms_2 = CountMinSketch(eps=0.01, delta=0.01)

    for _ in range(100):
        cms_1.update("A")
    for _ in range(200):
        cms_2.update("A")

    union = cms_1 + cms_2

    estimated = union.frequency("A")
    true_freq = 300
    assert abs(estimated - true_freq) <= 0.01 * 300 


cms = CountMinSketch(eps=0.01, delta=0.01)
data_stream = ["apple", "banana", "apple", "orange", "apple", "banana", "banana"]
for el in data_stream:
    cms.add(el)

print("Frequency of 'apple':", cms.frequency("apple"))
