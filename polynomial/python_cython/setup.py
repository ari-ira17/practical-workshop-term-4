from setuptools import setup, Extension
from Cython.Build import cythonize

ext = Extension(
    "wrapper_cython",
    sources=["wrapper_cython.pyx", "../c_core/poly.c"],
    include_dirs=["../c_core"]
)

setup(
    ext_modules=cythonize(ext, language_level="3")
)
