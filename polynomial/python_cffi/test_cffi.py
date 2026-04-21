from Cython.Build import FFI

ffi = FFI()
# Описание интерфейса через cdef 
ffi.cdef("double calc_poly(double* coeffs, int n, double x);")
lib = ffi.dlopen("./libpoly.so") 

def run_cffi(coeffs, x):
    c_arr = ffi.new("double[]", coeffs) 
    return lib.calc_poly(c_arr, len(coeffs), x)
