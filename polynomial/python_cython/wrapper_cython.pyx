from cpython.array cimport array
import array as py_array

# Подключаем заголовочный файл из папки c_core
cdef extern from "../c_core/poly.h":
    double calc_poly(double* coeffs, int n, double x)

def run_cython(list coeffs, double x):
    cdef int n = len(coeffs)
    if n == 0:
        return 0.0
    
    # Создаем массив через псевдоним
    cdef array a = py_array.array('d', coeffs)
    
    # Прямая передача указателя на данные в C-функцию
    return calc_poly(a.data.as_doubles, n, x)
    