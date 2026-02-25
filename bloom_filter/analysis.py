from false_positive_rate import generate_items
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


m_values = [100, 200, 500, 800, 1000]
k_values = [x for x in range(1, 10)]
attemps = 100
num_of_elements = 100

results = []

for m in m_values:
    for k in k_values:
        res = experiment(m, k, attemps, num_of_elements)
        results.append({'m': m, 'k': k, 'Результат': res})

df = pd.DataFrame(results)

fig, ax = plt.subplots(figsize=(10, 15))
ax.axis('off')

table = ax.table(
    cellText=df.values,
    colLabels=df.columns,
    loc='center',
    cellLoc='center'
)

table.auto_set_font_size(False)
table.set_fontsize(12)    
table.scale(0.5, 1.5)       
plt.title('Зависимость вероятности от числа хеш-функций', fontsize=20, pad=20)

plt.savefig('bloom_filter/empirical_probability_of_a_false_positive_table.png')

plt.figure(figsize=(10, 6))
for m in m_values:
    subset = df[df["m"] == m]
    plt.plot(subset["k"], subset["Результат"], label=f"m = {m}")

plt.xlabel("Число хеш-функций (k)")
plt.ylabel("Эмпирическая вероятность ложноположительного срабатывания")
plt.title("Зависимость вероятности от числа хеш-функций для различных m (m фиксировано)")
plt.legend()
plt.grid(True)

plt.savefig('bloom_filter/empirical_probability_of_a_false_positive_image.png')
