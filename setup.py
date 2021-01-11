#!/usr/bin/env python-sirius

"""SIRIUSHLAFAC Setup."""

from setuptools import setup, find_packages


with open('VERSION', 'r') as _f:
    __version__ = _f.read().strip()


with open('requirements.txt', 'r') as _f:
    _requirements = _f.read().strip().split('\n')


setup(
    name='siriushlafac',
    version=__version__,
    author='lnls-fac',
    description='FAC Client Applications for Sirius',
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
        ],
    zip_safe=False,
    )
