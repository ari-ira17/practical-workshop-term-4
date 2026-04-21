#include <Python.h>
#include "../c_core/poly.h"
#include <stdlib.h>

// 1. Реализация функции-обертки
static PyObject* method_calc_poly(PyObject* self, PyObject* args) {
    PyObject* list_obj;
    double x;

    // Парсинг аргументов: O (объект/список) и d (double)
    if (!PyArg_ParseTuple(args, "Od", &list_obj, &x)) {
        return NULL;
    }

    // Проверка, что первый аргумент — список 
    if (!PyList_Check(list_obj)) {
        PyErr_SetString(PyExc_TypeError, "Первый аргумент должен быть списком коэффициентов.");
        return NULL;
    }

    int n = PyList_Size(list_obj);
    if (n == 0) {
        return PyFloat_FromDouble(0.0);
    }

    // Выделение памяти под массив C 
    double* coeffs = (double*)malloc(n * sizeof(double));
    if (coeffs == NULL) {
        return PyErr_NoMemory();
    }

    // Конвертация элементов списка Python в double 
    for (int i = 0; i < n; i++) {
        PyObject* item = PyList_GetItem(list_obj, i);
        coeffs[i] = PyFloat_AsDouble(item);
        if (PyErr_Occurred()) {
            free(coeffs);
            return NULL;
        }
    }

    // Вызов основной функции из poly.c 
    double res = calc_poly(coeffs, n, x);

    free(coeffs);

    // Возврат результата в виде объекта Python 
    return PyFloat_FromDouble(res);
}

// 2. Описание методов модуля 
static PyMethodDef PolyMethods[] = {
    {"calc_poly", method_calc_poly, METH_VARARGS, "Вычисляет значение полинома по схеме Горнера."},
    {NULL, NULL, 0, NULL} // Маркер конца массива
};

// 3. Структура описания модуля
static struct PyModuleDef polymodule = {
    PyModuleDef_HEAD_INIT,
    "poly_capi",       // Имя модуля для импорта в Python
    NULL,              // Документация модуля
    -1,                // Размер состояния модуля (не используется)
    PolyMethods
};

// 4. Функция инициализации модуля 
PyMODINIT_FUNC PyInit_poly_capi(void) {
    return PyModule_Create(&polymodule);
}
