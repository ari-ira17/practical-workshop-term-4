from Cython.Build import FFI

ffi = FFI()
ffi.cdef("double calc_poly(double* coeffs, int n, double x);")
# загрузка скомпилированной динамической библиотеки
lib = ffi.dlopen("./libpoly.so") 

def run_cffi(coeffs, x):
    # создаем настоящий массив double в памяти C и копируем в него данные из питоновского списка coeffs
    c_arr = ffi.new("double[]", coeffs) 
    return lib.calc_poly(c_arr, len(coeffs), x)
