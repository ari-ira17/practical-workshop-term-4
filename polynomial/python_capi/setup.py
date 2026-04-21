from setuptools import setup, Extension

module = Extension(
    'poly_capi', 
    sources=['ext_capi.c', '../c_core/poly.c'],
    include_dirs=['../c_core']
)

setup(
    name='poly_capi',
    version='1.0',
    ext_modules=[module]
)
