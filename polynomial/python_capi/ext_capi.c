#include <Python.h>     // подключение инструментов для работы с объектами python
#include "../c_core/poly.h"
#include <stdlib.h>

static PyObject* method_calc_poly(PyObject* self, PyObject* args) {
    PyObject* list_obj;
    double x;

    if (!PyArg_ParseTuple(args, "Od", &list_obj, &x)) {
        return NULL;
    }

    if (!PyList_Check(list_obj)) {
        PyErr_SetString(PyExc_TypeError, "Первый аргумент должен быть списком коэффициентов.");
        return NULL;
    }

    int n = PyList_Size(list_obj);      // узнаем размер списка и создаем массив в памяти C
    if (n == 0) {
        return PyFloat_FromDouble(0.0);     // return 0.0;
    }

    double* coeffs = (double*)malloc(n * sizeof(double));
    if (coeffs == NULL) {
        return PyErr_NoMemory();
    }

    for (int i = 0; i < n; i++) {       // проходим по списку python и превращаем каждый элемент в double
        PyObject* item = PyList_GetItem(list_obj, i);
        coeffs[i] = PyFloat_AsDouble(item);     
        if (PyErr_Occurred()) {
            free(coeffs);
            return NULL;
        }
    }
    double res = calc_poly(coeffs, n, x);

    free(coeffs);

    return PyFloat_FromDouble(res);     // превращаем результат типа double обратно в объект python
}

static PyMethodDef PolyMethods[] = {
    {"calc_poly", method_calc_poly, METH_VARARGS, "Вычисляет значение полинома по схеме Горнера."},
    // { "Имя в Python", Функция_в_C, Тип_аргументов, "Описание" }
    {NULL, NULL, 0, NULL}
    // Маркер конца таблицы
};

static struct PyModuleDef polymodule = {
    PyModuleDef_HEAD_INIT,
    "poly_capi", // Официальное имя модуля
    NULL,        // Документация (у тебя тут NULL)
    -1,          // Состояние модуля (обычно -1 для простых модулей)
    PolyMethods  // Ссылка на то самое «меню» (таблицу методов)
};

PyMODINIT_FUNC PyInit_poly_capi(void) {
    return PyModule_Create(&polymodule);
}
