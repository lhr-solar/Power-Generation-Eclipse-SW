# !/bin/python3
# isort: skip_file
"""_summary_
"""

from setuptools import setup
from Cython.Build import cythonize

setup(
    name="FiveParameterPVCell",
    ext_modules=cythonize("FiveParameterPVCell.pyx"),
    zip_safe=False,
)

setup(
    name="ModifiedFiveParameterPVCell",
    ext_modules=cythonize("ModifiedFiveParameterPVCell.pyx"),
    zip_safe=False,
)
