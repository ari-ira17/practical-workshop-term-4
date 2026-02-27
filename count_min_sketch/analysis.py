import sys
import os
import random
import pandas as pd
from collections import Counter
from matplotlib import pyplot as plt
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hyperloglog.test_hll import date_gen
from cms_algorithm import CountMinSketch


def experiment(d, w, num_of_elements):
    random.seed(10)
    abs_errors = []
    rel_errors = []
    seen = []
    thread = num_of_elements
    cms = CountMinSketch(d=d, w=w)
    gen = date_gen()

    for _ in range(thread):
        date = next(gen)
        seen.append(date)
        cms.update(date)

    true_freq = Counter(seen)
    for key, value in true_freq.items():
        frequency = cms.frequency(key)
        abs_error = abs(value - frequency)
        rel_error = abs_error / thread
        abs_errors.append(abs_error)
        rel_errors.append(rel_error)

    return abs_errors, rel_errors


d_fixed = 100
thread = 25_000
w_values = [100, 200, 500, 1000, 2000]
abs_errors_w = []
rel_errors_w = []
for w in w_values:
    a_e, r_e = experiment(d=d_fixed, w=w, num_of_elements=thread)
    abs_errors_w.append(a_e)
    rel_errors_w.append(r_e)

avg_abs_errors_w = [sum(x) / len(x) for x in abs_errors_w]
avg_rel_errors_w = [sum(x) / len(x) for x in rel_errors_w]


plt.figure(figsize=(12, 8))

plt.subplot(2, 2, 1)
plt.plot(w_values, avg_abs_errors_w, 'o-', label='Средняя абс. ошибка')
plt.xlabel('w')
plt.ylabel('Средняя абсолютная ошибка')
plt.title(f'Зависимость абсолютной ошибки от w (d = {d_fixed})')
plt.grid(True)

plt.subplot(2, 2, 2)
plt.plot(w_values, avg_rel_errors_w, 'o-', label='Средняя относ. ошибка')
plt.xlabel('w')
plt.ylabel('Средняя относительная ошибка')
plt.title(f'Зависимость относительной ошибки от w (d = {d_fixed})')
plt.grid(True)


w_fixed = 100
thread = 25_000
d_values = [100, 200, 500, 1000, 2000]
abs_errors_d = []
rel_errors_d = []
for d in d_values:
    a_e, r_e = experiment(d=d, w=w_fixed, num_of_elements=thread)
    abs_errors_d.append(a_e)
    rel_errors_d.append(r_e)

avg_abs_errors_d = [sum(x) / len(x) for x in abs_errors_d]
avg_rel_errors_d = [sum(x) / len(x) for x in rel_errors_d]

plt.subplot(2, 2, 3)
plt.plot(d_values, avg_abs_errors_d, 'o-', label='Средняя абс. ошибка')
plt.xlabel('d')
plt.ylabel('Средняя абсолютная ошибка')
plt.title(f'Зависимость абсолютной ошибки от d (w = {w_fixed})')
plt.grid(True)

plt.subplot(2, 2, 4)
plt.plot(d_values, avg_rel_errors_d, 'o-', label='Средняя относ. ошибка')
plt.xlabel('d')
plt.ylabel('Средняя относительная ошибка')
plt.title(f'Зависимость относительной ошибки от d (w = {w_fixed})')
plt.grid(True)
plt.subplots_adjust(hspace=0.4)
plt.savefig('count_min_sketch/dependence_of_the_error_on_parametrs_image.png')


data_w = pd.DataFrame({
    'w': w_values,
    'Средняя абс. ошибка': avg_abs_errors_w,
    'Средняя относ. ошибка': avg_rel_errors_w
})

fig, ax = plt.subplots(figsize=(12, 3))
ax.axis('off')
table_w = ax.table(
    cellText=data_w.values,
    colLabels=data_w.columns,
    loc='center',
    cellLoc='center'
)
table_w.auto_set_font_size(False)
table_w.set_fontsize(12)
table_w.scale(1.2, 2.0)
plt.title('Зависимость погрешности от параметра w', fontsize=14)
plt.savefig('count_min_sketch/dependence_of_the_error_on_w_table.png')
plt.close() 

data_d = pd.DataFrame({
    'd': d_values,
    'Средняя абс. ошибка': avg_abs_errors_d,
    'Средняя относ. ошибка': avg_rel_errors_d
})

fig, ax = plt.subplots(figsize=(10, 3))
ax.axis('off')
table_d = ax.table(
    cellText=data_d.values,
    colLabels=data_d.columns,
    loc='center',
    cellLoc='center'
)
table_d.auto_set_font_size(False)
table_d.set_fontsize(12)
table_d.scale(1.2, 2.0)
plt.title('Зависимость погрешности от параметра d', fontsize=14)
plt.savefig('count_min_sketch/dependence_of_the_error_on_d_table.png')
plt.close()
