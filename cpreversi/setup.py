from distutils.core import setup, Extension
from Cython.Build import cythonize
from numpy import get_include # cimport numpy を使うため

ext = Extension("reversi_out", sources=["reversi.pyx", "reversi.c"], include_dirs=['.', get_include()])
setup(name="reversi_out", ext_modules=cythonize([ext]))
