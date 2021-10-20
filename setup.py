
from distutils.core import setup
from Cython.Build import cythonize


setup(
    name='cy_array',
    ext_modules=cythonize("cy_array.pyx"),
    gdb_debug=True
)