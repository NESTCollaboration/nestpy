#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "NEST.hh"

namespace py = pybind11;

PYBIND11_MODULE(nestpy, m) {
  py::class_<NEST::NESTcalc>(m, "NESTcalc")
    .def(py::init<>())
    .def("BinomFluct", &NEST::NESTcalc::BinomFluct)
    .def("FullCalculation", &NEST::NESTcalc::FullCalculation, 
	 "Perform the full yield calculation with smearings");


  py::enum_<NEST::INTERACTION_TYPE>(m, "INTERACTION_TYPE", py::arithmetic())
    .value("NR", NEST::INTERACTION_TYPE::NR)
    .value("WIMP", NEST::INTERACTION_TYPE::WIMP)
    .value("B8", NEST::INTERACTION_TYPE::B8)
    .value("DD", NEST::INTERACTION_TYPE::DD)
    .value("AmBe", NEST::INTERACTION_TYPE::AmBe)
    .value("Cf", NEST::INTERACTION_TYPE::Cf)
    .value("ion", NEST::INTERACTION_TYPE::ion)
    .value("gammaRay", NEST::INTERACTION_TYPE::gammaRay)
    .value("beta", NEST::INTERACTION_TYPE::beta)
    .value("CH3T", NEST::INTERACTION_TYPE::CH3T)
    .value("C14", NEST::INTERACTION_TYPE::C14)
    .value("Kr83m", NEST::INTERACTION_TYPE::Kr83m)
    .value("NoneType", NEST::INTERACTION_TYPE::NoneType)
    .export_values();

  py::class_<NEST::YieldResult>(m, "YieldResult")
    .def_readwrite("PhotonYield", &NEST::YieldResult::PhotonYield)    
    .def_readwrite("ElectronYield", &NEST::YieldResult::ElectronYield)   
    .def_readwrite("ExcitonRatio", &NEST::YieldResult::ExcitonRatio)   
    .def_readwrite("Lindhard", &NEST::YieldResult::Lindhard)   
    .def_readwrite("ElectricField", &NEST::YieldResult::ElectricField)   
    .def_readwrite("DeltaT_Scint", &NEST::YieldResult::DeltaT_Scint);

  py::class_<NEST::QuantaResult>(m, "QuantaResult")
    .def_readwrite("photons", &NEST::QuantaResult::photons)
    .def_readwrite("electrons", &NEST::QuantaResult::electrons)
    .def_readwrite("ions", &NEST::QuantaResult::ions)
    .def_readwrite("excitons", &NEST::QuantaResult::excitons);
  
  py::class_<NEST::NESTresult>(m, "NESTresult")
    .def_readwrite("yields", &NEST::NESTresult::yields)
    .def_readwrite("quanta", &NEST::NESTresult::quanta)
    .def_readwrite("photon_times", &NEST::NESTresult::photon_times);





}

