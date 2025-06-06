#!/usr/bin/env python-sirius

"""SIRIUSHLAFAC Setup."""

import pathlib

from setuptools import find_packages, setup


def get_abs_path(relative):
    """."""
    return str(pathlib.Path(__file__).parent / relative)


with open(get_abs_path("README.md"), "r") as _f:
    _long_description = _f.read().strip()

with open(get_abs_path("VERSION"), "r") as _f:
    __version__ = _f.read().strip()

with open(get_abs_path("requirements.txt"), "r") as _f:
    _requirements = _f.read().strip().split("\n")

setup(
    name='siriushlafac',
    version=__version__,
    author='lnls-fac',
    description='FAC Client Applications for Sirius',
    long_description=_long_description,
    url='https://github.com/lnls-fac/hlafac',
    download_url='https://github.com/lnls-fac/hlafac',
    license='GNU GPLv3',
    classifiers=[
        'Intended Audience :: Science/Research',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering'
        ],
    packages=find_packages(),
    install_requires=_requirements,
    package_data={
        'siriushlafac': ['VERSION', '*/*.py'],
    },
    include_package_data=True,
    scripts=[
        'scripts/sirius-hla-bo-ap-trajfit.py',
        'scripts/sirius-hla-si-ap-trajfit.py',
        'scripts/sirius-hla-si-ap-coupmeas.py',
        ],
    zip_safe=False,
    )
