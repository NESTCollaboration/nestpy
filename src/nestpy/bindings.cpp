#include <pybind11/pybind11.h>
#include "NEST.hh"
#include "VDetector.hh"
#include "testNEST.hh"
//#include "DetectorExample_XENON10.hh"
#include "LUX_Run03.hh"
// #include "TestSpectra.hh" // XX: Added

#include <pybind11/numpy.h>
#include <pybind11/stl_bind.h>
#include <pybind11/stl.h>
#include <pybind11/functional.h>



namespace py = pybind11;

PYBIND11_MODULE(nestpy, m) {
  //	Binding for YieldResult struct
  py::class_<NEST::YieldResult>(m, "YieldResult", py::dynamic_attr())
    .def(py::init<>())
	.def_readwrite("PhotonYield", &NEST::YieldResult::PhotonYield)
	.def_readwrite("ElectronYield", &NEST::YieldResult::ElectronYield)
	.def_readwrite("ExcitonRatio", &NEST::YieldResult::ExcitonRatio)
	.def_readwrite("Lindhard", &NEST::YieldResult::Lindhard)
	.def_readwrite("ElectricField", &NEST::YieldResult::ElectricField)
	.def_readwrite("DeltaT_Scint", &NEST::YieldResult::DeltaT_Scint);

  //	Binding for QuantaResult struct
  py::class_<NEST::QuantaResult>(m, "QuantaResult", py::dynamic_attr())
    .def(py::init<>())
	.def_readwrite("photons", &NEST::QuantaResult::photons)
	.def_readwrite("electrons", &NEST::QuantaResult::electrons)
	.def_readwrite("ions", &NEST::QuantaResult::ions)
	.def_readwrite("excitons", &NEST::QuantaResult::excitons);

  //	Binding for NESTresult struct
  py::class_<NEST::NESTresult>(m, "NESTresult", py::dynamic_attr())
    .def(py::init<>())
	.def_readwrite("yields", &NEST::NESTresult::yields)
	.def_readwrite("quanta", &NEST::NESTresult::quanta)
	.def_readwrite("photon_times", &NEST::NESTresult::photon_times);

  //	Binding for the enumeration INTERACTION_TYPE
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

  //	Binding for the VDetector class
  py::class_<VDetector, std::unique_ptr<VDetector, py::nodelete>>(m, "VDetector")	//	py::nodelete added so that NESTcalc() deconstructor does
		  	  	  	  	  	  	  	  	  	  	  	  	  	  	  	  	  	  	  	//	not delete instance of VDetector()
	.def(py::init<>())
	.def("Initialization", &VDetector::Initialization)
	.def("get_g1", &VDetector::get_g1)
	.def("get_sPEres", &VDetector::get_sPEres)
	.def("get_sPEthr", &VDetector::get_sPEthr)
	.def("get_sPEeff", &VDetector::get_sPEeff)
	.def("get_noiseB", &VDetector::get_noiseB) //XX: edit
  .def("get_noiseL", &VDetector::get_noiseL) //XX: edit
  .def("get_P_dphe", &VDetector::get_P_dphe)
  .def("get_P_dphe", &VDetector::get_P_dphe)
	.def("get_extraPhot", &VDetector::get_extraPhot) //XX: added
	.def("get_coinLevel", &VDetector::get_coinLevel)
	.def("get_numPMTs", &VDetector::get_numPMTs)

	.def("get_g1_gas", &VDetector::get_g1_gas)
	.def("get_s2Fano", &VDetector::get_s2Fano)
	.def("get_s2_thr", &VDetector::get_s2_thr)
	//.def("get_S2botTotRatio", &VDetector::get_S2botTotRatio)
	.def("get_E_gas", &VDetector::get_E_gas)
	.def("get_eLife_us", &VDetector::get_eLife_us)

	.def("get_inGas", &VDetector::get_inGas)
	.def("get_T_Kelvin", &VDetector::get_T_Kelvin)
	.def("get_p_bar", &VDetector::get_p_bar)

	.def("get_dtCntr", &VDetector::get_dtCntr)
	.def("get_dt_min", &VDetector::get_dt_min)
	.def("get_dt_max", &VDetector::get_dt_max)
	.def("get_radius", &VDetector::get_radius)
  .def("get_radmax", &VDetector::get_radmax) //XX: added
	.def("get_TopDrift", &VDetector::get_TopDrift)
	.def("get_anode", &VDetector::get_anode)
	.def("get_cathode", &VDetector::get_cathode)
	.def("get_gate", &VDetector::get_gate)

	.def("get_PosResExp", &VDetector::get_PosResExp)
	.def("get_PosResBase", &VDetector::get_PosResBase)
  .def("get_molarMass", &VDetector::get_molarMass) //XX: added

	.def("set_g1", &VDetector::set_g1)
	.def("set_sPEres", &VDetector::set_sPEres)
	.def("set_sPEthr", &VDetector::set_sPEthr)
	.def("set_sPEeff", &VDetector::set_sPEeff)
	.def("set_noiseB", &VDetector::set_noiseB) //XX: edit
  .def("set_noiseL", &VDetector::set_noiseL) //XX: edit
	.def("set_P_dphe", &VDetector::set_P_dphe)

  .def("set_extraPhot", &VDetector::set_extraPhot) //XX: added
	.def("set_coinWind", &VDetector::set_coinWind)
	.def("set_coinLevel", &VDetector::set_coinLevel)
	.def("set_numPMTs", &VDetector::set_numPMTs)

	.def("set_g1_gas", &VDetector::set_g1_gas)
	.def("set_s2Fano", &VDetector::set_s2Fano)
	.def("set_s2_thr", &VDetector::set_s2_thr)
	//.def("set_S2botTotRatio", &VDetector::set_S2botTotRatio)
	.def("set_E_gas", &VDetector::set_E_gas)
	.def("set_eLife_us", &VDetector::set_eLife_us)

	.def("set_inGas", &VDetector::set_inGas)
	.def("set_T_Kelvin", &VDetector::set_T_Kelvin)
	.def("set_p_bar", &VDetector::set_p_bar)

	.def("set_dtCntr", &VDetector::set_dtCntr)
	.def("set_dt_min", &VDetector::set_dt_min)
	.def("set_dt_max", &VDetector::set_dt_max)
	.def("set_radius", &VDetector::set_radius)
  .def("set_radmax", &VDetector::set_radmax) //XX: added
	.def("set_TopDrift", &VDetector::set_TopDrift)
	.def("set_anode", &VDetector::set_anode)
	.def("set_cathode", &VDetector::set_cathode)
	.def("set_gate", &VDetector::set_gate)

	.def("set_PosResExp", &VDetector::set_PosResExp)
	.def("set_PosResBase", &VDetector::set_PosResBase)

  .def("set_molarMass", &VDetector::set_molarMass)


	.def("FitS1", &VDetector::FitS1)
	.def("FitEF", &VDetector::FitEF)
	.def("FitS2", &VDetector::FitS2)
	.def("FitTBA", &VDetector::FitTBA)

	.def("OptTrans", &VDetector::OptTrans)
  	.def("SinglePEWaveForm", &VDetector::SinglePEWaveForm);


  /*
  //	Binding for example XENONnT
  py::class_<DetectorExample_XENON10, VDetector, std::unique_ptr<DetectorExample_XENON10, py::nodelete>>(m, "DetectorExample_XENON10")
     .def(py::init<>())
	 .def("Initialization", &DetectorExample_XENON10::Initialization)
	 .def("FitTBA", &DetectorExample_XENON10::FitTBA)
	 .def("OptTrans", &DetectorExample_XENON10::OptTrans)
	 .def("SinglePEWaveForm", &DetectorExample_XENON10::SinglePEWaveForm);
  */


  py::class_<DetectorExample_LUX_RUN03, VDetector, std::unique_ptr<DetectorExample_LUX_RUN03, py::nodelete>>(m, "DetectorExample_LUX_RUN03")
     .def(py::init<>())
	 .def("Initialization", &DetectorExample_LUX_RUN03::Initialization)
	 .def("FitTBA", &DetectorExample_LUX_RUN03::FitTBA)
	 .def("OptTrans", &DetectorExample_LUX_RUN03::OptTrans)
	 .def("SinglePEWaveForm", &DetectorExample_LUX_RUN03::SinglePEWaveForm);


  //	Binding for the NESTcalc class
  py::class_<NEST::NESTcalc>(m, "NESTcalc")
    // .def(py::init<>()) //XX: remove
	.def(py::init<VDetector*>())
    .def("BinomFluct", &NEST::NESTcalc::BinomFluct)

  // XX: add default input arguments
  .def("FullCalculation", &NEST::NESTcalc::FullCalculation,
      "Perform the full yield calculation with smearings",
      py::arg("interaction") = NEST::INTERACTION_TYPE::NR,
      py::arg("energy") = 100,
  		py::arg("density") = 2.9,
      py::arg("drift_field") = 124,
      py::arg("A") = 131.293,
      py::arg("Z") = 54,
      py::arg("nuisance_parameters") = std::vector<double>({ 11., 1.1, 0.0480, -0.0533, 12.6, 0.3, 2., 0.3, 2., 0.5, 1., 1.}),
      py::arg("free_parameters") = std::vector<double>({1.,1.,0.1,0.5,0.07}),
      py::arg("do_times") = false)
	.def("PhotonTime", &NEST::NESTcalc::PhotonTime)
	.def("AddPhotonTransportTime", &NEST::NESTcalc::AddPhotonTransportTime)
	.def("GetPhotonTimes", &NEST::NESTcalc::GetPhotonTimes)
        .def("GetYields",
	     &NEST::NESTcalc::GetYields,
	     py::arg("interaction") = NEST::INTERACTION_TYPE::NR,
	     py::arg("energy") = 100,
	     py::arg("density") = 2.9,
	     py::arg("drift_field") = 124,
	     py::arg("A") = 131.293,
	     py::arg("Z") = 54,
	     py::arg("nuisance_parameters") = std::vector<double>({ 11., 1.1, 0.0480, -0.0533, 12.6, 0.3, 2., 0.3, 2., 0.5, 1., 1.})
	 )
    .def("GetQuanta", &NEST::NESTcalc::GetQuanta,
	 py::arg("yields"),
	 py::arg("density") = 2.9,
	 py::arg("free_parameters") = std::vector<double>({1., 1., 0.1, 0.5, 0.07}))
	.def("GetS1", &NEST::NESTcalc::GetS1)
	.def("GetSpike", &NEST::NESTcalc::GetSpike)
	//.def("GetS2", &NEST::NESTcalc::GetS2) 					Currently not working because of VDetector.FitTBA()
	.def("CalculateG2", &NEST::NESTcalc::CalculateG2)
	.def("SetDriftVelocity", &NEST::NESTcalc::SetDriftVelocity)
	// .def("SetDriftVelocity_MagBoltz", &NEST::NESTcalc::SetDriftVelocity_MagBoltz)
	.def("SetDriftVelocity_NonUniform", &NEST::NESTcalc::SetDriftVelocity_NonUniform)
	.def("SetDensity", &NEST::NESTcalc::SetDensity)
  //.def("xyResolution", &NEST::NESTcalc::xyResolution)		Currently not working because of VDetector.FitTBA()
	.def("PhotonEnergy", &NEST::NESTcalc::PhotonEnergy)
	.def("CalcElectronLET", &NEST::NESTcalc::CalcElectronLET)
  .def("GetDensity", &NEST::NESTcalc::GetDensity)
	.def("GetDetector", &NEST::NESTcalc::GetDetector);

  // testNEST functions
  m.def("testNEST", &testNEST);
  m.def("GetEnergyRes", &GetEnergyRes);
  m.def("GetBand", &GetBand);

  // XX: added
  py::class_<NESTObservable>(m, "NESTObservable", py::dynamic_attr())
    .def(py::init<>())
  .def_readwrite("s1_nhits_phd", &NESTObservable::s1_nhits_phd)
  .def_readwrite("s1_nhits_phe", &NESTObservable::s1_nhits_phe)
  .def_readwrite("s1r_phe", &NESTObservable::s1r_phe)
  .def_readwrite("s1c_phe", &NESTObservable::s1c_phe)
  .def_readwrite("s1r_phd", &NESTObservable::s1r_phd)
  .def_readwrite("s1c_phd", &NESTObservable::s1c_phd)
  .def_readwrite("Nee", &NESTObservable::Nee)
  .def_readwrite("s2r_phe", &NESTObservable::s2r_phe)
  .def_readwrite("s2c_phe", &NESTObservable::s2c_phe)
  .def_readwrite("s2r_phd", &NESTObservable::s2r_phd)
  .def_readwrite("s2c_phd", &NESTObservable::s2c_phd);

  py::class_<NESTObservableArray>(m, "NESTObservableArray", py::dynamic_attr())
    .def(py::init<>())
  .def_readwrite("s1_nhits_phd", &NESTObservableArray::s1_nhits_phd)
  .def_readwrite("s1_nhits_phe", &NESTObservableArray::s1_nhits_phe)
  .def_readwrite("s1r_phe", &NESTObservableArray::s1r_phe)
  .def_readwrite("s1c_phe", &NESTObservableArray::s1c_phe)
  .def_readwrite("s1r_phd", &NESTObservableArray::s1r_phd)
  .def_readwrite("s1c_phd", &NESTObservableArray::s1c_phd)
  .def_readwrite("Nee", &NESTObservableArray::Nee)
  .def_readwrite("s2r_phe", &NESTObservableArray::s2r_phe)
  .def_readwrite("s2c_phe", &NESTObservableArray::s2c_phe)
  .def_readwrite("s2r_phd", &NESTObservableArray::s2r_phd)
  .def_readwrite("s2c_phd", &NESTObservableArray::s2c_phd);

  m.def("runNEST", &runNEST,
  "Generate (S1, S2) for a single recoil",
  py::arg("detector"),
  py::arg("keV") = 10.,
  py::arg("interaction") = NEST::INTERACTION_TYPE::NR,
  py::arg("inField") = 180,
  py::arg("pos_x") = 0.,
  py::arg("pos_y") = 0.,
  py::arg("pos_z") = 0.,
  py::arg("seed") = 0.);

  m.def("runNEST_vec", &runNEST_vec,
  "Generate (S1, S2) for a vectorized recoil energies");

  // py::class_<TestSpectra>(m, "TestSpectra", py::dynamic_attr())
  // .def(py::init<>())
  // .def("WIMP_dRate", &TestSpectra::WIMP_dRate, "SI WIMP at 1e-36 cm2", py::arg("Er")=10., py::arg("mass")=10.)
  // .def("CH3T_spectrum", &TestSpectra::CH3T_spectrum, py::arg("emin"), py::arg("emax"))
  // .def("C14_spectrum", &TestSpectra::C14_spectrum, py::arg("emin"), py::arg("emax"))
  // .def("B8_spectrum", &TestSpectra::B8_spectrum, py::arg("emin"), py::arg("emax"))
  // .def("AmBe_spectrum", &TestSpectra::AmBe_spectrum, py::arg("emin"), py::arg("emax"))
  // .def("Cf_spectrum", &TestSpectra::Cf_spectrum, py::arg("emin"), py::arg("emax"))
  // .def("DD_spectrum", &TestSpectra::DD_spectrum, py::arg("emin"), py::arg("emax"));


}
