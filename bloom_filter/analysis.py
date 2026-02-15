from tests import generate_items
from algorithm import BloomFilter

import matplotlib.pyplot as plt
import pandas as pd


def experiment(m, k, attemps, num_of_elements):
    false_positive = 0
    for i in range(attemps):
        bloom_filter = BloomFilter(m=m, k=k)

        items_to_add = generate_items(num_of_elements)
        items_to_check = generate_items(num_of_elements, start=17_002, end=18_000_000)

        for item in items_to_add:
            bloom_filter.add(item)

        for item in items_to_check:
            if item not in items_to_add and bloom_filter.check(item):
                false_positive += 1

    return false_positive / (attemps * num_of_elements)


m = [100, 200, 500, 800, 1000]
k = [x for x in range(1, 10)]
attemps = 100
num_of_elements = 100

results = []

for m_value in m:
    for k_value in k:
        res = experiment(m_value, k_value, attemps, num_of_elements)
        results.append({'m': m_value, 'k': k_value, 'res': res})

df = pd.DataFrame(results)

fig, ax = plt.subplots(figsize=(9, 9))
ax.axis('tight')
ax.axis('off')

table = ax.table(
    cellText=df.values,
    colLabels=df.columns,
    loc='center',
    cellLoc='center'
)
plt.savefig('bloom_filter/empirical_probability_of_a_false_positive_table.png')

plt.figure(figsize=(10, 6))
for m_v in m:
    subset = df[df["m"] == m_v]
    plt.plot(subset["k"], subset["res"], marker='o', label=f"m = {m_v}")

plt.xlabel("Число хеш-функций (k)")
plt.ylabel("Эмпирическая вероятность ложноположительного срабатывания")
plt.title("Зависимость вероятности от числа хеш-функций для различных m (m фиксировано)")
plt.legend()
plt.grid(True)

plt.savefig('bloom_filter/empirical_probability_of_a_false_positive_image.png')
