from setuptools import setup, Extension
from Cython.Build import cythonize
import numpy

# Define an extension that needs to be compiled
ext = Extension("graph_generator",
                sources=["graph_generator.pyx"],
                include_dirs=[numpy.get_include()])  # This line is added

setup(
    ext_modules=cythonize(ext)
)
