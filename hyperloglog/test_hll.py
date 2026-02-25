import random
from datetime import datetime, timedelta

from algorithm import Hyperloglog


def date_gen():
    start = datetime(2026, 2, 24)
    total_days = 365 * 100

    while True:
        random_date = start + timedelta(days=random.randint(0, total_days))
        yield random_date.strftime("%d/%m/%Y")


def test_thread():
    threads = [25_000, 200_000, 1_000_00]
    for thread in threads:

        random.seed(thread / 1000)
        runs = 5
        abs_errors = []
        rel_errors = []

        for i in range(runs):
            gen = date_gen()
            hyperloglog = Hyperloglog(eps=0.01)
            seen = set()
            
            for j in range(thread):
                date = next(gen)
                seen.add(date)
                hyperloglog.process_element(date)

            estimate = hyperloglog.estimate_cardinality()
            abs_error = abs(estimate - len(seen))       
            rel_error = abs(estimate - len(seen)) / len(seen)

            abs_errors.append(abs_error)
            rel_errors.append(rel_error)

        avg_abs_error = sum(abs_errors) / runs
        avg_rel_errors = sum(rel_errors) / runs 
        print(f"При размере потока {thread}: средняя абсолютная погрешность = {avg_abs_error}")
        print(f"При размере потока {thread}: средняя относительная погрешность = {round(avg_rel_errors * 100, 2)}%")

        assert avg_rel_errors <= 0.01


def test_thread_union():
    threads = [25_000, 200_000]
    for thread in threads:
        random.seed(thread / 1000)
        runs = 5
        abs_errors = []
        rel_errors = []

        for i in range(runs):
            gen_1 = date_gen()
            gen_2 = date_gen()
            hyperloglog_1 = Hyperloglog(eps=0.01)
            hyperloglog_2 = Hyperloglog(eps=0.01)
            seen_1 = set()
            seen_2 = set()
            
            for j in range(thread):
                date_1 = next(gen_1)
                date_2 = next(gen_2)
                seen_1.add(date_1)
                seen_2.add(date_2)
                hyperloglog_1.process_element(date_1)
                hyperloglog_2.process_element(date_2)

            hyperloglog_union = hyperloglog_1 + hyperloglog_2
            estimate = hyperloglog_union.estimate_cardinality()
            abs_error = abs(estimate - len(seen_1 | seen_2))        
            rel_error = abs_error / len(seen_1 | seen_2)

            abs_errors.append(abs_error)
            rel_errors.append(rel_error)

        avg_abs_error = sum(abs_errors) / runs
        avg_rel_errors = sum(rel_errors) / runs 
        print(f"При размере потока {thread}: средняя абсолютная погрешность = {avg_abs_error}")
        print(f"При размере потока {thread}: средняя относительная погрешность = {round(avg_rel_errors * 100, 2)}%")

        assert avg_rel_errors <= 0.01
