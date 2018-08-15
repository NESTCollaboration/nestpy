# nestpy (alpha status)

[![Build Status](https://travis-ci.org/NESTCollaboration/nestpy.svg?branch=master)](https://travis-ci.org/NESTCollaboration/nestpy)
[![DOI](https://zenodo.org/badge/140174447.svg)](https://zenodo.org/badge/latestdoi/140174447)
[![PyPi version](https://pypip.in/v/nestpy/badge.png)](https://crate.io/packages/nestpy/)
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

nc = nestpy.NESTcalc()
print('My favorite random number is', nc.BinomFluct(10, 0.2))

print('This is NR', nestpy.INTERACTION_TYPE(0))

A = 131.293
Z = 54.

x = nc.FullCalculation(nestpy.INTERACTION_TYPE(5), # NR                                  
                       -1, # keV                                                         
                       2.9, # g/cm^3                                                     
                       124, # Drift field, V/cm                                          
                       A,
                       Z,
                       (1,1))
print('Full calculation gives quanta object', x.quanta)  # This is QuantaResult          

print('This many:')
print('\t', x.quanta.photons)
print('\t', x.quanta.electrons)

detec = nestpy.VDetector()
detec.Initialization()

y = nc.GetYields(nestpy.INTERACTION_TYPE(0), # NR                                        
                 200, # keV                                                              
                 2.9, # g/cm^3                                                           
                 124, # Drift field, V/cm                                                
                 A,
                 Z,
                 (1,1))

print(y.PhotonYield)
```

## Credit

* Help from Henry Schreiner (https://indico.cern.ch/event/694818/contributions/2985778/attachments/1682465/2703470/PyHEPTalk.pdf)
* Implementation also based on http://www.benjack.io/2018/02/02/python-cpp-revisited.html
