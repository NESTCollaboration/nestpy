# nestpy
Python bindings to the NEST library:

```
from nestpy import nestpy
nestpy.NESTcalc().BinomFluct(10, 0.2)
```

Install with `python setup.py install` (PyPI will come later) and be sure to have CMake and a C++ compatible compiler.

## Credit

* NEST collaboration.  
* Help from Henry Schreiner (https://indico.cern.ch/event/694818/contributions/2985778/attachments/1682465/2703470/PyHEPTalk.pdf)
* Implementation also based on http://www.benjack.io/2018/02/02/python-cpp-revisited.html
