#include <pybind11/pybind11.h>
#include "NEST.hh"

namespace py = pybind11;

PYBIND11_MODULE(nestpy, m) {
  py::class_<NEST::NESTcalc>(m, "NESTcalc")
    .def(py::init<>())
    .def("BinomFluct", &NEST::NESTcalc::BinomFluct)
    ;
}

