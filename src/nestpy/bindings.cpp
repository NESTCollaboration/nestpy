#include <pybind11/pybind11.h>
#include "math.hpp"

namespace py = pybind11;

PYBIND11_PLUGIN(nestpy)
{
  py::module m("nestpy");
  m.def("add", &add);
  m.def("subtract", &subtract);
  return m.ptr();
}
