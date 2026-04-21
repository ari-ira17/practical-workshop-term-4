#include "poly.h"

double calc_poly(double* coeffs, int n, double x) {
    if (n <= 0 || coeffs == 0) return 0.0; // Обработка некорректных аргументов
    
    double result = coeffs[n - 1];
    for (int i = n - 2; i >= 0; i--) {
        result = result * x + coeffs[i];
    }
    return result;
}
