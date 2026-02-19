#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "NEST.hh"
#include "execNEST.hh"
namespace py = pybind11;
using namespace pybind11::literals; 


void init_array(py::module& m){
    auto m_array = m.def_submodule("array", "array");

    py::class_<NESTObservableArray>(m_array, "NESTObservableArray", py::dynamic_attr())
        .def(py::init<>())
        .def_readonly("s1_nhits", &NESTObservableArray::s1_nhits)
        .def_readonly("s1_nhits_thr", &NESTObservableArray::s1_nhits_thr)
        .def_readonly("s1_nhits_dpe", &NESTObservableArray::s1_nhits_dpe)
        .def_readonly("s1r_phe", &NESTObservableArray::s1r_phe)
        .def_readonly("s1c_phe", &NESTObservableArray::s1c_phe)
        .def_readonly("s1r_phd", &NESTObservableArray::s1r_phd)
        .def_readonly("s1c_phd", &NESTObservableArray::s1c_phd)
        .def_readonly("s1r_spike", &NESTObservableArray::s1r_spike)
        .def_readonly("s1c_spike", &NESTObservableArray::s1c_spike)
        .def_readonly("s2_Nee", &NESTObservableArray::s2_Nee)
        .def_readonly("s2_Nph", &NESTObservableArray::s2_Nph)
        .def_readonly("s2_nhits", &NESTObservableArray::s2_nhits)
        .def_readonly("s2_nhits_dpe", &NESTObservableArray::s2_nhits_dpe)
        .def_readonly("s2r_phe", &NESTObservableArray::s2r_phe)
        .def_readonly("s2c_phe", &NESTObservableArray::s2c_phe)
        .def_readonly("s2r_phd", &NESTObservableArray::s2r_phd)
        .def_readonly("s2c_phd", &NESTObservableArray::s2c_phd)
        .def_readonly("s1_waveform_time", &NESTObservableArray::s1_waveform_time)
        .def_readonly("s1_waveform_amp", &NESTObservableArray::s1_waveform_amp)
        .def_readonly("s2_waveform_time", &NESTObservableArray::s2_waveform_time)
        .def_readonly("s2_waveform_amp", &NESTObservableArray::s2_waveform_amp)
        .def_readonly("n_electrons", &NESTObservableArray::n_electrons)
        .def_readonly("n_photons", &NESTObservableArray::n_photons)
        .def_readonly("s1_photon_times", &NESTObservableArray::s1_photon_times);


    m_array.def("runNESTvec", &runNESTvec,
        "Generate (S1, S2) for a vector of recoil energies",
        py::arg("detector"),
        py::arg("interaction_type"),
        py::arg("energies"),
        py::arg("positions"),
        py::arg("inField") = -1.0,
        py::arg("seed") = 0,
        py::arg("er_yield_params") = default_ERYieldsParam,
        py::arg("nr_yield_params") = default_NRYieldsParam,
        py::arg("width_params") = default_NRERWidthsParam,
        py::arg("s1_mode") = NEST::S1CalculationMode::Hybrid,
        py::arg("s2_mode") = NEST::S2CalculationMode::Full,
        py::arg("calculate_times") = false
    );
}