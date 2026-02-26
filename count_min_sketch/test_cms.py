import sys
import os
import random
from collections import Counter
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from hyperloglog.test_hll import date_gen

from count_min_sketch.cms_algorithm import CountMinSketch


def test_cms_threads():
    threads = [200_000, 1_000_000]

    for thread in threads:
        random.seed(thread / 1000)
        runs = 5
        errors = []

        for _ in range(runs):
            cms = CountMinSketch(eps=0.01, delta=0.01)
            gen = date_gen()
            seen = []
            for _ in range(thread):
                date = next(gen)
                cms.update(date)
                seen.append(date)

            true_freq = Counter(seen)
            for key, value in true_freq.items():
                frequency = cms.frequency(key)
                abs_error = abs(value - frequency)
                errors.append(abs_error)

        avg_abs_error = sum(errors) / len(errors)
        print(f"В потоке {thread} абсолютная погрешность составялет {round(avg_abs_error, 3)}")
        assert sum(errors) / len(errors) <= cms.eps * thread


def test_cms_union():
    threads = [200_000, 1_000_000]
    random.seed(sum(threads) / 1000)
    runs = 5
    errors = []

    for _ in range(runs):
        cms_1 = CountMinSketch(eps=0.01, delta=0.01)
        cms_2 = CountMinSketch(eps=0.01, delta=0.01)
        gen_1 = date_gen()
        gen_2 = date_gen()
        seen = []

        for _ in range(threads[0]):
            date = next(gen_1)
            cms_1.update(date)
            seen.append(date)

        for _ in range(threads[1]):
            date = next(gen_2)
            cms_2.update(date)
            seen.append(date)

        cms_union = cms_1 + cms_2
        true_freq = Counter(seen)
        for key, value in true_freq.items():
            frequency = cms_union.frequency(key)
            abs_error = abs(value - frequency)
            errors.append(abs_error)

    avg_abs_error = sum(errors) / len(errors)
    print(f"В объединении абсолютная погрешность составялет {round(avg_abs_error, 3)}")
    assert sum(errors) / len(errors) <= cms_union.eps * sum(threads)
