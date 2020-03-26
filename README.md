# nestpy

[![Join the chat at https://gitter.im/NESTCollaboration/nestpy](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/NESTCollaboration/nestpy?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
[![Build Status](https://travis-ci.org/NESTCollaboration/nestpy.svg?branch=master)](https://travis-ci.org/NESTCollaboration/nestpy)
[![DOI](https://zenodo.org/badge/140174447.svg)](https://zenodo.org/badge/latestdoi/140174447)
[![PyPi version](https://pypip.in/v/nestpy/badge.png)](https://pypi.org/project/nestpy/)
[![Project Status: Active – The project has reached a stable, usable state and is being actively developed.](https://www.repostatus.org/badges/latest/active.svg)](https://www.repostatus.org/#active)
[![Python Versions](https://img.shields.io/pypi/pyversions/nestpy.svg)](https://pypi.python.org/pypi/nestpy)

These are the Python bindings for the [NEST library](https://github.com/NESTCollaboration/nest), which provides a direct wrapping of functionality.  The library is not Pythonic at this point but just uses the existing naming conventions from the C++ library.

You do *not* have to have NEST already installed to use this package.

## Note from Xin:
This package is forked from [nestpy](https://github.com/NESTCollaboration/nestpy) and updated to LUX Run3 Detector template. In addition,  two functions are added to `testNEST.cpp`. 
1. A function that produce (S1, S2) observables
2. A vectorized function that accept energy in a list as input. 

Please see `example/demo_v0.ipynb` for the usage of the two functions.

## Installing from PyPI (not for this repo)

For 64-bit Linux or Mac systems, instally 'nestpy' should just require running:

```
pip install nestpy
```

You can then test that it works by running the example above.

## Installing from source

Requirements: You must have CMake>=2.8.12 and a C++11 compatible compiler (GCC>=4.8) to build.

First, you must check out this repository then simply run the installer:

```
git clone https://github.com/xxiang4/nestpy.git
cd nestpy
python setup.py install
```


## Usage

Python bindings to the NEST library:

```
import nestpy

# This is same as C++ NEST with naming
nc = nestpy.NESTcalc()

interaction = nestpy.INTERACTION_TYPE(0)  # NR

E = 10  # keV
print('For an %s keV %s' % (E, interaction))

# Get particle yields
y = nc.GetYields(interaction,
		 E)

print('The photon yield is:', y.PhotonYield)
print('With statistical fluctuations',
      nc.GetQuanta(y).photons)
```

For more examples on possible calls, please see the tests folder.

### Support

* Bugs: Please report bugs to the [issue tracker on Github](https://github.com/NESTCollaboration/nestpy/issues) such that we can keep track of them and eventually fix them.  Please explain how to reproduce the issue (including code) and which system you are running on.
* Help: Help can be provided also via the issue tracker by tagging your issue with 'question'
* Contributing:  Please fork this repository then make a pull request.  In this pull request, explain the details of your change and include tests.

## Technical implementation

This package is a [pybind11](https://pybind11.readthedocs.io/en/stable/intro.html) wrapper of [NEST](https://github.com/NESTCollaboration/nest) that uses [TravisCI](https://travis-ci.org) to build binaries using the [manylinux](https://github.com/pypa/python-manylinux-demo) [Docker image](https://www.docker.com).

* Help from Henry Schreiner, which included a great [binding tutorial](https://indico.cern.ch/event/694818/contributions/2985778/attachments/1682465/2703470/PyHEPTalk.pdf)
* Implementation also based on [this](http://www.benjack.io/2018/02/02/python-cpp-revisited.html)

See AUTHORS.md for information on the developers.

## Citation

When you use `nestpy`, please say so in your slides or publications (for publications, see Zenodo link above).  You can mention this in addition to how you cite NEST.  This is important for us being able to get funding to support this project.
