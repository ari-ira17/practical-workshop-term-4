import sys
import os

# Добавляем корень проекта в пути поиска модулей
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.join(current_dir, '..')
sys.path.append(root_dir)

import time
import numpy as np
import pandas as pd

from data_generator import get_test_data
import python_ctypes.test_ctypes as ct
import python_cffi.test_cffi as cf
import poly_capi  # Скомпилированный C API
import wrapper_cython  # Скомпилированный Cython

def measure(func, name, data):
    # Разогрев [cite: 135]
    func(data[0][0], data[0][1])
    
    run_times = []
    for _ in range(50): # 50 запусков [cite: 19]
        start = time.perf_counter() # [cite: 140]
        for coeffs, x in data:
            func(coeffs, x) # 100 000 вызовов внутри одного замера [cite: 20]
        run_times.append(time.perf_counter() - start)
    
    return {
        "Подход": name,
        "Min": np.min(run_times),
        "Max": np.max(run_times),
        "Mean": np.mean(run_times),
        "Median": np.median(run_times),
        "Std": np.std(run_times)
    }

if __name__ == "__main__":
    data = get_test_data() # 100 000 разных входных данных [cite: 21, 128]
    
    results = []
    results.append(measure(ct.run_ctypes, "ctypes", data))
    results.append(measure(cf.run_cffi, "cffi", data))
    results.append(measure(poly_capi.calc_poly, "CPython C API", data))
    results.append(measure(wrapper_cython.run_cython, "Cython", data))
    
    df = pd.DataFrame(results)
    print(df.to_string(index=False))
    df.to_csv("benchmark/results.csv", index=False) # Сохраняем для графиков
    