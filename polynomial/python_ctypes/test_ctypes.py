import ctypes

# загружаем скомпилированный файл libpoly.so
lib = ctypes.CDLL('./libpoly.so')

# явно указываем типы аргументов 
lib.calc_poly.argtypes = [ctypes.POINTER(ctypes.c_double), ctypes.c_int, ctypes.c_double]
# и тип возвращаемого значения (restype)
lib.calc_poly.restype = ctypes.c_double

def run_ctypes(coeffs, x):
    n = len(coeffs)
    # Преобразование списка в массив C 
    c_arr = (ctypes.c_double * n)(*coeffs)
    return lib.calc_poly(c_arr, n, x)
