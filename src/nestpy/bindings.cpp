#include <pybind11/pybind11.h>
#include <iostream>
#include "NEST.hh"
#include "LArNEST.hh"
#include "execNEST.hh"
#include "RandomGen.hh"
#include <pybind11/numpy.h>
#include <pybind11/stl_bind.h>
#include <pybind11/stl.h>
#include <pybind11/functional.h>
#include "execNEST.hh"
#include "spectra.hh"
#include "detector.hh"
#include "array.hh"

#define STRINGIFY(x) #x
#define MACRO_STRINGIFY(x) STRINGIFY(x)
 
namespace py = pybind11;
using namespace pybind11::literals; 

PYBIND11_MODULE(_nestpy, m) 
{
	// versioning
#ifdef NESTPY_VERSION
    m.attr("__version__") = MACRO_STRINGIFY(NESTPY_VERSION);
#else
    m.attr("__version__") = "dev";
#endif
#ifdef NEST_VERSION
    m.attr("__nest_version__") = MACRO_STRINGIFY(NEST_VERSION);
#else
    m.attr("__nest_version__") = "";
#endif
	//-----------------------------------------------------------------------
	// LXe NEST bindings
	
	// Init random seed
	RandomGen::rndm()->SetSeed( time(nullptr) );
	// Binding for RandomGen class
	py::class_<RandomGen>(m, "RandomGen")
		.def_static("rndm", &RandomGen::rndm, py::return_value_policy::reference)
		.def("set_seed", &RandomGen::SetSeed)
		.def("lock_seed", &RandomGen::LockSeed)
		.def("unlock_seed", &RandomGen::UnlockSeed);

	// Binding for YieldResult struct

	py::class_<NEST::YieldResult>(m, "YieldResult", py::dynamic_attr())
		.def(py::init<>())
		.def_readonly("PhotonYield", &NEST::YieldResult::PhotonYield)
		.def_readonly("ElectronYield", &NEST::YieldResult::ElectronYield)
		.def_readonly("ExcitonRatio", &NEST::YieldResult::ExcitonRatio)
		.def_readonly("Lindhard", &NEST::YieldResult::Lindhard)
		.def_readonly("ElectricField", &NEST::YieldResult::ElectricField)
		.def_readonly("DeltaT_Scint", &NEST::YieldResult::DeltaT_Scint);
	
	//	Binding for QuantaResult struct
	py::class_<NEST::QuantaResult>(m, "QuantaResult", py::dynamic_attr())
		.def(py::init<>())
		.def_readonly("photons", &NEST::QuantaResult::photons)
		.def_readonly("electrons", &NEST::QuantaResult::electrons)
		.def_readonly("ions", &NEST::QuantaResult::ions)
		.def_readonly("excitons", &NEST::QuantaResult::excitons);

	//	Binding for NESTresult struct
	py::class_<NEST::NESTresult>(m, "NESTresult", py::dynamic_attr())
		.def(py::init<>())
		.def_readonly("yields", &NEST::NESTresult::yields)
		.def_readonly("quanta", &NEST::NESTresult::quanta)
		.def_readonly("photon_times", &NEST::NESTresult::photon_times);

	// Binding for Wvalue struct...
	py::class_<NEST::NESTcalc::Wvalue>(m, "Wvalue", py::dynamic_attr())
		.def(py::init<>())
		.def_readonly("Wq_eV", &NEST::NESTcalc::Wvalue::Wq_eV)
		.def_readonly("alpha", &NEST::NESTcalc::Wvalue::alpha);


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

	py::enum_<NEST::S1CalculationMode>(m, "S1CalculationMode", py::arithmetic())
		.value("Full", NEST::S1CalculationMode::Full)
		.value("Parametric", NEST::S1CalculationMode::Parametric)
		.value("Hybrid", NEST::S1CalculationMode::Hybrid)
		.value("Waveform", NEST::S1CalculationMode::Waveform)
		.export_values();

	py::enum_<NEST::S2CalculationMode>(m, "S2CalculationMode", py::arithmetic())
		.value("Full", NEST::S2CalculationMode::Full)
		.value("Waveform", NEST::S2CalculationMode::Waveform)
		.value("WaveformWithEtrain", NEST::S2CalculationMode::WaveformWithEtrain)
		.export_values();
		
	//	Binding for the NESTcalc class
	py::class_<NEST::NESTcalc, std::unique_ptr<NEST::NESTcalc, py::nodelete>>(m, "NESTcalc")
		//.def(py::init<>())
		.def(py::init<VDetector*>())
		.def_readonly_static("default_nr_parameters", &default_NRYieldsParam)
		.def_readonly_static("default_nr_er_width_parameters", &default_NRERWidthsParam)
		.def_readonly_static("default_er_parameters", &default_ERYieldsParam)
		//     .def_static("BinomFluct", &NEST::NESTcalc::BinomFluct)
		.def("FullCalculation", &NEST::NESTcalc::FullCalculation,
			"Perform the full yield calculation with smearings",
			py::arg("interaction") = NEST::INTERACTION_TYPE::NR,
			py::arg("energy"),
		   	py::arg("density") = 2.9,
			py::arg("drift_field") = 124,
			py::arg("A") = 131.293,
			py::arg("Z") = 54,
			py::arg("nr_parameters") = &default_NRYieldsParam,
			py::arg("er_parameters") = &default_ERYieldsParam,
			py::arg("nr_er_width_parameters") = &default_NRERWidthsParam,
			py::arg("do_times") = false
	    )
		.def("PhotonTime", &NEST::NESTcalc::PhotonTime)
		.def("AddPhotonTransportTime", &NEST::NESTcalc::AddPhotonTransportTime)
		.def("GetPhotonTimes", &NEST::NESTcalc::GetPhotonTimes)
		.def("GetYieldKr83m",
			&NEST::NESTcalc::GetYieldKr83m,
			py::arg("energy") = 41.5,
			py::arg("density") = 2.9,
			py::arg("drift_field") = 124,
			py::arg("maxTimeSeparation") = 2000.,
			py::arg("minTimeSeparation") = 0.0
		)
		.def("GetYieldERWeighted", 
			&NEST::NESTcalc::GetYieldERWeighted, 
			py::arg("energy") = 5.2,
			py::arg("density") = 2.9, 
			py::arg("drift_field") = 124,
			py::arg("er_parameters") = &default_ERYieldsParam,
			py::arg("EnergyParams") = std::vector<double>({0.23, 0.77, 2.95, -1.44}),
			py::arg("FieldParams") = std::vector<double>({421.15, 3.27})
		)
		.def("GetYields",
			&NEST::NESTcalc::GetYields,
			py::arg("interaction") = NEST::INTERACTION_TYPE::NR,
			py::arg("energy") = 100,
			py::arg("density") = 2.9,
			py::arg("drift_field") = 124,
			py::arg("A") = 131.293,
			py::arg("Z") = 54,
			py::arg("nr_parameters") = &default_NRYieldsParam,
			py::arg("er_parameters") = &default_ERYieldsParam
		)
		.def("GetQuanta", &NEST::NESTcalc::GetQuanta,
			py::arg("yields"),
			py::arg("density") = 2.9,
			py::arg("nr_er_width_parameters") = &default_NRERWidthsParam, 
			py::arg("SkewnessER") = -999.
		)   
		.def("GetS1", &NEST::NESTcalc::GetS1)
		.def("GetSpike", &NEST::NESTcalc::GetSpike)
		// Currently VDetector.FitTBA() requires we reinitialize the detector every time:
		.def("GetS2", &NEST::NESTcalc::GetS2)
		.def("CalculateG2", &NEST::NESTcalc::CalculateG2, py::arg("vebosity") = 0)
		.def("GetG2",  [](NEST::NESTcalc &self){return self.CalculateG2(0).at(3);})
		.def("GetG2Params", [](NEST::NESTcalc &self){auto vec = self.CalculateG2(0); return py::dict("g2"_a=vec.at(3), "extraction_eff"_a=vec.at(1));})
		.def("SetDriftVelocity", &NEST::NESTcalc::SetDriftVelocity)
		.def("SetDriftVelocity_NonUniform", &NEST::NESTcalc::SetDriftVelocity_NonUniform)
		.def("SetDensity", &NEST::NESTcalc::SetDensity)
		.def_static("GetDensity", &NEST::NESTcalc::GetDensity,
			py::arg("T") = 174.,
			py::arg("P") = 1.80,
			py::arg("inGas") = false,
			py::arg("evtNum") = 0,
			py::arg("molarMass") = 131.293
		)
		.def_static("WorkFunction", &NEST::NESTcalc::WorkFunction,
			py::arg("rho") = 2.89,
			py::arg("MolarMass") = 131.293,
			py::arg("OldW13eV") = true
		)
		

		// Currently VDetector.FitTBA() requires we reinitialize the detector every time:
		.def("xyResolution", &NEST::NESTcalc::xyResolution)
		.def("PhotonEnergy", &NEST::NESTcalc::PhotonEnergy)
		.def("CalcElectronLET", &NEST::NESTcalc::CalcElectronLET)
		.def("GetDetector", &NEST::NESTcalc::GetDetector)
		
		// Have to set "inGas" like this to solve reference issues
		.def_property_readonly("density_liquid", [](NEST::NESTcalc &self){bool inGas = false; return NEST::NESTcalc::GetDensity(self.GetDetector()->get_T_Kelvin(), self.GetDetector()->get_p_bar(), inGas, 0, self.GetDetector()->get_molarMass());})
		.def_property_readonly("density_gas", [](NEST::NESTcalc &self){bool inGas = true; return NEST::NESTcalc::GetDensity(self.GetDetector()->get_T_Kelvin(), self.GetDetector()->get_p_bar(), inGas, 0, self.GetDetector()->get_molarMass());})

		.def_static("calculate_drift_velocity_gas", 
			py::vectorize([](double temperature, double pressure, double density, double field, double molarMass)
			{return NEST::NESTcalc::GetDriftVelocity_MagBoltz(temperature, density, field, pressure, molarMass);}),
			"temperature"_a, "pressure"_a, "density"_a, "field"_a,  "molarMass"_a = 131.293
		)
    	.def_static("calculate_drift_velocity_liquid", 
			py::vectorize([](double temperature, double pressure, double density, double field, double stddev)
			{return NEST::NESTcalc::GetDriftVelocity_Liquid(temperature, field, density, pressure, stddev);}),
			"temperature"_a, "pressure"_a, "density"_a, "field"_a, "stddev"_a = -1
		);

		//	execNEST function
		m.def("execNEST", &execNEST);
		m.def("GetEnergyRes", &GetEnergyRes);
		m.def("GetBand", &GetBand);
		m.attr("default_nr_parameters") =  py::cast(default_NRYieldsParam);
		m.attr("default_nr_er_width_parameters") =  py::cast(default_NRERWidthsParam);
		m.attr("default_er_parameters") =  py::cast(default_ERYieldsParam);

	//-----------------------------------------------------------------------
	// LAr NEST bindings

	//	Binding for the enumeration LArInteraction
	py::enum_<NEST::LArInteraction>(m, "LArInteraction", py::arithmetic())
		.value("NR", NEST::LArInteraction::NR)
		.value("ER", NEST::LArInteraction::ER)
		.value("Alpha", NEST::LArInteraction::Alpha)
		.export_values();

	// NR Yields Parameters
	py::class_<NEST::LArNRYieldsParameters>(m, "LArNRYieldsParameters", py::dynamic_attr())
		.def(py::init<>())
		.def_readwrite("alpha", &NEST::LArNRYieldsParameters::alpha)
		.def_readwrite("beta", &NEST::LArNRYieldsParameters::beta)
		.def_readwrite("gamma", &NEST::LArNRYieldsParameters::gamma)
		.def_readwrite("delta", &NEST::LArNRYieldsParameters::delta)
		.def_readwrite("epsilon", &NEST::LArNRYieldsParameters::epsilon)
		.def_readwrite("zeta", &NEST::LArNRYieldsParameters::zeta)
		.def_readwrite("eta", &NEST::LArNRYieldsParameters::eta);
		
	// ER Electron Yields Alpha Parameters
	py::class_<NEST::LArERElectronYieldsAlphaParameters>(m, "LArERElectronYieldsAlphaParameters", py::dynamic_attr())
		.def(py::init<>())
		.def_readwrite("A", &NEST::LArERElectronYieldsAlphaParameters::A)
		.def_readwrite("B", &NEST::LArERElectronYieldsAlphaParameters::B)
		.def_readwrite("C", &NEST::LArERElectronYieldsAlphaParameters::C)
		.def_readwrite("D", &NEST::LArERElectronYieldsAlphaParameters::D)
		.def_readwrite("E", &NEST::LArERElectronYieldsAlphaParameters::E)
		.def_readwrite("F", &NEST::LArERElectronYieldsAlphaParameters::F)
		.def_readwrite("G", &NEST::LArERElectronYieldsAlphaParameters::G);
	
	// ER Electron Yields Beta Parameters
	py::class_<NEST::LArERElectronYieldsBetaParameters>(m, "LArERElectronYieldsBetaParameters", py::dynamic_attr())
		.def(py::init<>())
		.def_readwrite("A", &NEST::LArERElectronYieldsBetaParameters::A)
		.def_readwrite("B", &NEST::LArERElectronYieldsBetaParameters::B)
		.def_readwrite("C", &NEST::LArERElectronYieldsBetaParameters::C)
		.def_readwrite("D", &NEST::LArERElectronYieldsBetaParameters::D)
		.def_readwrite("E", &NEST::LArERElectronYieldsBetaParameters::E)
		.def_readwrite("F", &NEST::LArERElectronYieldsBetaParameters::F);

	// ER Electron Yields Gamma Parameters
	py::class_<NEST::LArERElectronYieldsGammaParameters>(m, "LArERElectronYieldsGammaParameters", py::dynamic_attr())
		.def(py::init<>())
		.def_readwrite("A", &NEST::LArERElectronYieldsGammaParameters::A)
		.def_readwrite("B", &NEST::LArERElectronYieldsGammaParameters::B)
		.def_readwrite("C", &NEST::LArERElectronYieldsGammaParameters::C)
		.def_readwrite("D", &NEST::LArERElectronYieldsGammaParameters::D)
		.def_readwrite("E", &NEST::LArERElectronYieldsGammaParameters::E)
		.def_readwrite("F", &NEST::LArERElectronYieldsGammaParameters::F);
	
	// ER Electron Yields DokeBirks Parameters
	py::class_<NEST::LArERElectronYieldsDokeBirksParameters>(m, "LArERElectronYieldsDokeBirksParameters", py::dynamic_attr())
		.def(py::init<>())
		.def_readwrite("A", &NEST::LArERElectronYieldsDokeBirksParameters::A)
		.def_readwrite("B", &NEST::LArERElectronYieldsDokeBirksParameters::B)
		.def_readwrite("C", &NEST::LArERElectronYieldsDokeBirksParameters::C)
		.def_readwrite("D", &NEST::LArERElectronYieldsDokeBirksParameters::D)
		.def_readwrite("E", &NEST::LArERElectronYieldsDokeBirksParameters::E);

	// ER Electron Yields Parameters
	py::class_<NEST::LArERYieldsParameters>(m, "LArERYieldsParameters", py::dynamic_attr())
		.def(py::init<>())
		.def_readwrite("alpha", &NEST::LArERYieldsParameters::alpha)
		.def_readwrite("beta", &NEST::LArERYieldsParameters::beta)
		.def_readwrite("gamma", &NEST::LArERYieldsParameters::gamma)
		.def_readwrite("doke_birks", &NEST::LArERYieldsParameters::doke_birks)
		.def_readwrite("p1", &NEST::LArERYieldsParameters::p1)
		.def_readwrite("p2", &NEST::LArERYieldsParameters::p2)
		.def_readwrite("p3", &NEST::LArERYieldsParameters::p3)
		.def_readwrite("p4", &NEST::LArERYieldsParameters::p4)
		.def_readwrite("p5", &NEST::LArERYieldsParameters::p5)
		.def_readwrite("delta", &NEST::LArERYieldsParameters::delta)
		.def_readwrite("let", &NEST::LArERYieldsParameters::let);

	// Alpha Electron Yields Parameters
	py::class_<NEST::LArAlphaElectronYieldsParameters>(m, "LArAlphaElectronYieldsParameters", py::dynamic_attr())
		.def(py::init<>())
		.def_readwrite("A", &NEST::LArAlphaElectronYieldsParameters::A)
		.def_readwrite("B", &NEST::LArAlphaElectronYieldsParameters::B)
		.def_readwrite("C", &NEST::LArAlphaElectronYieldsParameters::C)
		.def_readwrite("D", &NEST::LArAlphaElectronYieldsParameters::D)
		.def_readwrite("E", &NEST::LArAlphaElectronYieldsParameters::E)
		.def_readwrite("F", &NEST::LArAlphaElectronYieldsParameters::F)
		.def_readwrite("G", &NEST::LArAlphaElectronYieldsParameters::G)
		.def_readwrite("H", &NEST::LArAlphaElectronYieldsParameters::H)
		.def_readwrite("I", &NEST::LArAlphaElectronYieldsParameters::I)
		.def_readwrite("J", &NEST::LArAlphaElectronYieldsParameters::J);

	// Alpha Photon Yields Parameters
	py::class_<NEST::LArAlphaPhotonYieldsParameters>(m, "LArAlphaPhotonYieldsParameters", py::dynamic_attr())
		.def(py::init<>())
		.def_readwrite("A", &NEST::LArAlphaPhotonYieldsParameters::A)
		.def_readwrite("B", &NEST::LArAlphaPhotonYieldsParameters::B)
		.def_readwrite("C", &NEST::LArAlphaPhotonYieldsParameters::C)
		.def_readwrite("D", &NEST::LArAlphaPhotonYieldsParameters::D)
		.def_readwrite("E", &NEST::LArAlphaPhotonYieldsParameters::E)
		.def_readwrite("F", &NEST::LArAlphaPhotonYieldsParameters::F)
		.def_readwrite("G", &NEST::LArAlphaPhotonYieldsParameters::G)
		.def_readwrite("H", &NEST::LArAlphaPhotonYieldsParameters::H)
		.def_readwrite("I", &NEST::LArAlphaPhotonYieldsParameters::I)
		.def_readwrite("J", &NEST::LArAlphaPhotonYieldsParameters::J)
		.def_readwrite("J", &NEST::LArAlphaPhotonYieldsParameters::K)
		.def_readwrite("J", &NEST::LArAlphaPhotonYieldsParameters::L)
		.def_readwrite("J", &NEST::LArAlphaPhotonYieldsParameters::M);

	// Alpha Yields Parameters
	py::class_<NEST::LArAlphaYieldsParameters>(m, "LArAlphaYieldsParameters", py::dynamic_attr())
		.def(py::init<>())
		.def_readwrite("Ye", &NEST::LArAlphaYieldsParameters::Ye)
		.def_readwrite("Yph", &NEST::LArAlphaYieldsParameters::Yph);

	// Thomas-Imel Parameters
	py::class_<NEST::ThomasImelParameters>(m, "ThomasImelParameters", py::dynamic_attr())
		.def(py::init<>())
		.def_readwrite("A", &NEST::ThomasImelParameters::A)
		.def_readwrite("B", &NEST::ThomasImelParameters::B);
	
	// Drift Parameters
	py::class_<NEST::DriftParameters>(m, "DriftParameters", py::dynamic_attr())
		.def(py::init<>())
		.def_readwrite("A", &NEST::DriftParameters::A)
		.def_readwrite("B", &NEST::DriftParameters::B)
		.def_readwrite("C", &NEST::DriftParameters::B)
		.def_readwrite("TempLow", &NEST::DriftParameters::TempLow)
		.def_readwrite("TempHigh", &NEST::DriftParameters::TempHigh);

	// LAr Mean Yield Result
	py::class_<NEST::LArYieldResult>(m, "LArYieldResult", py::dynamic_attr())
		.def(py::init<>())
		.def_readwrite("TotalYield", &NEST::LArYieldResult::TotalYield)
		.def_readwrite("QuantaYield", &NEST::LArYieldResult::QuantaYield)
		.def_readwrite("LightYield", &NEST::LArYieldResult::LightYield)
		.def_readwrite("Nph", &NEST::LArYieldResult::Nph)
		.def_readwrite("Ne", &NEST::LArYieldResult::Ne)
		.def_readwrite("Nex", &NEST::LArYieldResult::Nex)
		.def_readwrite("Nion", &NEST::LArYieldResult::Nion)
		.def_readwrite("Lindhard", &NEST::LArYieldResult::Lindhard)
		.def_readwrite("ElectricField", &NEST::LArYieldResult::ElectricField);

	// LAr Fluctuation Result
	py::class_<NEST::LArYieldFluctuationResult>(m, "LArYieldFluctuationResult", py::dynamic_attr())
		.def(py::init<>())
		.def_readwrite("NphFluctuation", &NEST::LArYieldFluctuationResult::NphFluctuation)
		.def_readwrite("NeFluctuation", &NEST::LArYieldFluctuationResult::NeFluctuation)
		.def_readwrite("NexFluctuation", &NEST::LArYieldFluctuationResult::NexFluctuation)
		.def_readwrite("NionFluctuation", &NEST::LArYieldFluctuationResult::NionFluctuation);

	// LAr Yields Result
	py::class_<NEST::LArNESTResult>(m, "LArNESTResult", py::dynamic_attr())
		.def(py::init<>())
		.def_readwrite("yields", &NEST::LArNESTResult::yields)
		.def_readwrite("fluctuations", &NEST::LArNESTResult::fluctuations)
		.def_readwrite("photon_times", &NEST::LArNESTResult::photon_times);

	//	Binding for the LArNEST class
	py::class_<NEST::LArNEST, NEST::NESTcalc, std::unique_ptr<NEST::LArNEST, py::nodelete>>(m, "LArNEST")
		.def(py::init<VDetector*>())
		.def("set_density", &NEST::LArNEST::SetDensity)
		.def("set_r_ideal_gas", &NEST::LArNEST::SetRIdealGas)
		.def("set_real_gas_a", &NEST::LArNEST::SetRealGasA)
		.def("set_real_gas_b", &NEST::LArNEST::SetRealGasB)
		.def("set_work_quanta_function", &NEST::LArNEST::SetWorkQuantaFunction)
		.def("set_work_ion_function", &NEST::LArNEST::SetWorkIonFunction)
		.def("set_work_photon_function", &NEST::LArNEST::SetWorkPhotonFunction)
		.def("set_fano_er", &NEST::LArNEST::SetFanoER)
		.def("set_nex_over_nion", &NEST::LArNEST::SetNexOverNion)
		// .def("set_nuisance_parameters", &NEST::LArNEST::setNuisanceParameters)
		// .def("set_temperature", &NEST::LArNEST::setTemperature)
		// .def("set_nr_yields_parameters", &NEST::LArNEST::setNRYieldsParameters)
		// .def("set_er_yields_parameters", &NEST::LArNEST::setERYieldsParameters)
		// .def("set_er_electron_yields_alpha_parameters", &NEST::LArNEST::setERElectronYieldsAlphaParameters)
		// .def("set_er_electron_yields_beta_parameters", &NEST::LArNEST::setERElectronYieldsBetaParameters)
		//.def("set_er_electron_yields_gamma_parameters", &NEST::LArNEST::setERElectronYieldsGammaParameters)
		// .def("set_er_electron_yields_doke_birks_parameters", &NEST::LArNEST::setERElectronYieldsDokeBirksParameters)
		// .def("set_thomas_imel_parameters", &NEST::LArNEST::setThomasImelParameters)
		//.def("set_drift_parameters", &NEST::LArNEST::setDriftParameters)
     
		//.def("get_density", &NEST::LArNEST::GetDensity)
		.def("get_r_ideal_gas", &NEST::LArNEST::GetRIdealGas)
		.def("get_real_gas_a", &NEST::LArNEST::GetRealGasA)
		.def("get_real_gas_b", &NEST::LArNEST::GetRealGasB)
		.def("get_work_quanta_function", &NEST::LArNEST::GetWorkQuantaFunction)
		.def("get_work_ion_function", &NEST::LArNEST::GetWorkIonFunction)
		.def("get_work_photon_function", &NEST::LArNEST::GetWorkPhotonFunction)
		.def("get_fano_er", &NEST::LArNEST::GetFanoER)
		.def("get_nex_over_nion", &NEST::LArNEST::GetNexOverNion)
		.def("get_nr_yields_parameters", &NEST::LArNEST::GetNRYieldsParameters)
		.def("get_er_yields_parameters", &NEST::LArNEST::GetERYieldsParameters)
		.def("get_er_electron_yields_alpha_parameters", &NEST::LArNEST::GetERElectronYieldsAlphaParameters)
		.def("get_er_electron_yields_beta_parameters", &NEST::LArNEST::GetERElectronYieldsBetaParameters)
		.def("get_er_electron_yields_gamma_parameters", &NEST::LArNEST::GetERElectronYieldsGammaParameters)
		.def("get_er_electron_yields_doke_birks_parameters", &NEST::LArNEST::GetERElectronYieldsDokeBirksParameters)
		.def("get_thomas_imel_parameters", &NEST::LArNEST::GetThomasImelParameters)
		.def("get_drift_parameters", &NEST::LArNEST::GetDriftParameters)

		.def("get_recombination_yields", &NEST::LArNEST::GetRecombinationYields)
		.def("get_yields", &NEST::LArNEST::GetYields)
		.def("get_yield_fluctuations", &NEST::LArNEST::GetYieldFluctuations)
		.def("full_calculation", &NEST::LArNEST::FullCalculation)
		.def("get_nr_total_yields", &NEST::LArNEST::GetNRTotalYields)
		.def("get_nr_electron_yields", &NEST::LArNEST::GetNRElectronYields)
		.def("get_nr_photon_yields", &NEST::LArNEST::GetNRPhotonYields)
		.def("get_nr_photon_yields_conserved", &NEST::LArNEST::GetNRPhotonYieldsConserved)
		.def("get_nr_yields", &NEST::LArNEST::GetNRYields)
		.def("get_er_total_yields", &NEST::LArNEST::GetERTotalYields)
		.def("get_er_electron_yields_alpha", &NEST::LArNEST::GetERElectronYieldsAlpha)
		.def("get_er_electron_yields_beta", &NEST::LArNEST::GetERElectronYieldsBeta)
		.def("get_er_electron_yields_gamma", &NEST::LArNEST::GetERElectronYieldsGamma)
		.def("get_er_electron_yields_doke_birks", &NEST::LArNEST::GetERElectronYieldsDokeBirks)
		.def("get_er_electron_yields", &NEST::LArNEST::GetERElectronYields)
		.def("get_er_yields", &NEST::LArNEST::GetERYields)
		.def("get_alpha_total_yields", &NEST::LArNEST::GetAlphaTotalYields)
		.def("get_alpha_electron_yields", &NEST::LArNEST::GetAlphaElectronYields)
		.def("get_alpha_photon_yields", &NEST::LArNEST::GetAlphaPhotonYields)
		.def("get_alpha_yields", &NEST::LArNEST::GetAlphaYields)

		//.def("get_default_fluctuations", &NEST::LArNEST::GetDefaultFluctuations)
		.def("get_photon_time", &NEST::LArNEST::GetPhotonTime)
		//.def("get_photon_energy", &NEST::LArNEST::GetPhotonEnergy)
		//.def("get_drift_velocity_liquid", &NEST::LArNEST::GetDriftVelocity_Liquid)
		//.def("get_drift_velocity_magboltz", &NEST::LArNEST::GetDriftVelocity_MagBoltz)
		//.def("get_let", &NEST::LArNEST::GetLinearEnergyTransfer)
		//.def("get_density", &NEST::LArNEST::GetDensity)
		//.def("calculate_g2", &NEST::LArNEST::CalculateG2)

		.def("legacy_get_yields", &NEST::LArNEST::LegacyGetYields)
		.def("legacy_calculation", &NEST::LArNEST::LegacyCalculation)
		.def("legacy_get_recombination_probability", &NEST::LArNEST::LegacyGetRecombinationProbability)
		.def("legacy_get_let", &NEST::LArNEST::LegacyGetLinearEnergyTransfer);

	// Initialise new spectra class
	init_spectra(m);

	// Initilase new array functions
	init_array(m);

	// Initialise new detector class
	init_detector(m);

}