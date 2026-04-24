from setuptools import setup, Extension

module = Extension(     # описание модуля
    'poly_capi', 
    sources=['ext_capi.c', '../c_core/poly.c'],     # файлы, которые нужно скомпилировать
    include_dirs=['../c_core']      # путь к заголовочному файлу
)

# вызов компилятора и получение результата
setup(
    name='poly_capi',
    version='1.0',
    ext_modules=[module]
)
