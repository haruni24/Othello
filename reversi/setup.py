from setuptools import setup, Extension
from Cython.Build import cythonize
from numpy import get_include

ext = Extension(
    "creversi",
    sources=["creversi.pyx"],
    include_dirs=[get_include()],
    language="c++",
    extra_compile_args=["-std=c++11"],  # 必要に応じて追加のフラグを設定
)

setup(
    name="creversi",
    ext_modules=cythonize(
        [ext],
        compiler_directives={'language_level': "3"},
    ),
)