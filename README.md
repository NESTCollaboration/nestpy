# nestpy (alpha status)

[![Build Status](https://travis-ci.org/NESTCollaboration/nestpy.svg?branch=master)](https://travis-ci.org/NESTCollaboration/nestpy)
[![DOI](https://zenodo.org/badge/140174447.svg)](https://zenodo.org/badge/latestdoi/140174447)
[![PyPi version](https://pypip.in/v/nestpy/badge.png)](https://pypi.org/project/nestpy/)
[![PyPi downloads](https://pypip.in/d/nestpy/badge.png)](https://crate.io/packages/nestpy/)

These are the Python bindings for the [NEST library](https://github.com/NESTCollaboration/nest).  You do not have to have NEST already installed to use this package.

## Installing from PyPI

For nearly all systems, instally 'nestpy' should just require running:

```
pip install nestpy
```

You can then test that it works by running the example above.

## Installing from source

Requirements: You must have CMake>=2.8.12 and a C++11 compatible compiler (GCC>=4.8) to build.

First, you must check out this repository then simply run the installer:

```
git checkout https://github.com/NESTCollaboration/nestpy
cd nestpy
python setup.py install
```

## Usage

Python bindings to the NEST library:

```
import nestpy

# This is same as C++ NEST with naming                                                                            
nc = nestpy.NESTcalc()

A = 131.293
Z = 54.
density = 2.9 # g/cm^3                                                                                            

interaction = nestpy.INTERACTION_TYPE(0) # NR                                                                     
E = 10 # keV                                                                                                      
print('For an %s keV %s' % (E, interaction))

# Get particle yields                                                                                             
y = nc.GetYields(interaction,
                 E,
                 density,
                 124, # Drift field, V/cm                                                                         
                 A,
                 Z,
                 (1,1))

print('The photon yield is:', y.PhotonYield)

print('With statistical fluctuations', nc.GetQuanta(y, density).photons)

# Also                                                                                                            
detec = nestpy.VDetector()
detec.Initialization()
```

## Credit

* Help from Henry Schreiner (https://indico.cern.ch/event/694818/contributions/2985778/attachments/1682465/2703470/PyHEPTalk.pdf)
* Implementation also based on http://www.benjack.io/2018/02/02/python-cpp-revisited.html
