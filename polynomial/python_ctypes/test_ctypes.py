import ctypes

# Загрузка библиотеки 
lib = ctypes.CDLL('./libpoly.so')

# Описание типов аргументов и возврата 
lib.calc_poly.argtypes = [ctypes.POINTER(ctypes.c_double), ctypes.c_int, ctypes.c_double]
lib.calc_poly.restype = ctypes.c_double

def run_ctypes(coeffs, x):
    n = len(coeffs)
    # Преобразование списка в массив C 
    c_arr = (ctypes.c_double * n)(*coeffs)
    return lib.calc_poly(c_arr, n, x)
