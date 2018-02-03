from distutils.core import setup
from Cython.Build import cythonize


setup(
  ext_modules = cythonize("tester.pyx")
)

# python setup.py build_ext --inplace

