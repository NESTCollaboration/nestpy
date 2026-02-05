#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "NEST.hh"
#include "execNEST.hh"
namespace py = pybind11;


void init_array(py::module& m){
    auto m_array = m.def_submodule("array", "array");

    py::class_<NESTObservableArray>(m_array, "NESTObservableArray", py::dynamic_attr())
        .def(py::init<int>(), py::arg("verbosity") = -1)
        .def_readwrite("s1_nhits", &NESTObservableArray::s1_nhits)
        .def_readwrite("s1_nhits_thr", &NESTObservableArray::s1_nhits_thr)
        .def_readwrite("s1_nhits_dpe", &NESTObservableArray::s1_nhits_dpe)
        .def_readwrite("s1r_phe", &NESTObservableArray::s1r_phe)
        .def_readwrite("s1c_phe", &NESTObservableArray::s1c_phe)
        .def_readwrite("s1r_phd", &NESTObservableArray::s1r_phd)
        .def_readwrite("s1c_phd", &NESTObservableArray::s1c_phd)
        .def_readwrite("s1r_spike", &NESTObservableArray::s1r_spike)
        .def_readwrite("s1c_spike", &NESTObservableArray::s1c_spike)
        .def_readwrite("s2_Nee", &NESTObservableArray::s2_Nee)
        .def_readwrite("s2_Nph", &NESTObservableArray::s2_Nph)
        .def_readwrite("s2_nhits", &NESTObservableArray::s2_nhits)
        .def_readwrite("s2_nhits_dpe", &NESTObservableArray::s2_nhits_dpe)
        .def_readwrite("s2r_phe", &NESTObservableArray::s2r_phe)
        .def_readwrite("s2c_phe", &NESTObservableArray::s2c_phe)
        .def_readwrite("s2r_phd", &NESTObservableArray::s2r_phd)
        .def_readwrite("s2c_phd", &NESTObservableArray::s2c_phd)
        .def_readwrite("s1_waveform_time", &NESTObservableArray::s1_waveform_time)
        .def_readwrite("s1_waveform_amp", &NESTObservableArray::s1_waveform_amp)
        .def_readwrite("s2_waveform_time", &NESTObservableArray::s2_waveform_time)
        .def_readwrite("s2_waveform_amp", &NESTObservableArray::s2_waveform_amp)
        .def_readwrite("n_electrons", &NESTObservableArray::n_electrons)
        .def_readwrite("n_photons", &NESTObservableArray::n_photons)
        .def_readwrite("s1_photon_times", &NESTObservableArray::s1_photon_times);


    m_array.def("runNESTvec", &runNESTvec,
        "Generate (S1, S2) for a vectorized recoil energies",
        py::arg("detector"),
        py::arg("interaction_type"),
        py::arg("energies"),
        py::arg("positions"),
        py::arg("inField") = -1.0,
        py::arg("seed") = 0,
        py::arg("er_yield_params") = default_ERYieldsParam,
        py::arg("nr_yield_params") = default_NRYieldsParam,
        py::arg("width_params") = default_NRERWidthsParam,
        py::arg("s1_mode") = NEST::S1CalculationMode::Parametric,
        py::arg("s2_mode") = NEST::S2CalculationMode::Full,
        py::arg("calculate_times") = false
    );
}