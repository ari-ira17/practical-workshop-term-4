import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from hyperloglog.hll_algorithm import Hyperloglog
from test_hll import date_gen

import random
import pandas as pd
import matplotlib.pyplot as plt

n = 100_000
p_values = [x for x in range(4, 22, 2)]   
errors = []
lenghts = []
estimates = []
random.seed(100)

for p in p_values:
    gen = date_gen()
    hyperloglog = Hyperloglog(p=p)
    seen = set()

    for i in range(n):
        date = next(gen)
        seen.add(date)
        hyperloglog.process_element(date)

    estimate = hyperloglog.estimate_cardinality()
    rel_err = abs(len(seen) - estimate) / len(seen)
    errors.append(rel_err)
    lenghts.append(len(seen))
    estimates.append(estimate)

plt.plot(p_values, errors)
plt.xlabel('Значения p')
plt.ylabel('Относительная погрешность')
plt.title('Зависимость погрешности от параметра p')
plt.grid(True)
plt.savefig('hyperloglog/dependence_of_the_error_on_p_image.png')


data = pd.DataFrame({
    'p': p_values,
    'm = 2^p': [2 ** x for x in p_values],
    'Истинная кардинальность': [int(x) for x in lenghts],
    'Оценка': [round(x, 2) for x in estimates],
    'Погрегшность (%)': [round(x * 100, 2) for x in errors]
})

fig, ax = plt.subplots(figsize=(15, 8))
ax.axis('off')

table = ax.table(
    cellText=data.values,
    colLabels=data.columns,
    loc='center',
    cellLoc='center'
)

table.auto_set_font_size(False)
table.set_fontsize(14)    
table.scale(1.3, 3.0)       
plt.title('Зависимость погрешности от параметра p', fontsize=20, pad=20)

plt.savefig('hyperloglog/dependence_of_the_error_on_p_table.png', bbox_inches='tight',)
