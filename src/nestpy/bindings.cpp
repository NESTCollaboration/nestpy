#include <pybind11/pybind11.h>
#include "NEST.hh"
#include "LArNEST.hh"
#include "VDetector.hh"
#include "execNEST.hh"
#include "TestSpectra.hh"
#include "LUX_Run03.hh"
#include "DetectorExample_XENON10.hh"
#include "RandomGen.hh"
#include <pybind11/numpy.h>
#include <pybind11/stl_bind.h>
#include <pybind11/stl.h>
#include <pybind11/functional.h>
#include "LZ_SR1.hh"

#define STRINGIFY(x) #x
#define MACRO_STRINGIFY(x) STRINGIFY(x)
 
namespace py = pybind11;

PYBIND11_MODULE(nestpy, m) 
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
		.def("rndm", &RandomGen::rndm)
		.def("set_seed", &RandomGen::SetSeed);

	// Binding for YieldResult struct
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

	// Binding for Wvalue struct...
	py::class_<NEST::NESTcalc::Wvalue>(m, "Wvalue", py::dynamic_attr())
		.def(py::init<>())
		.def_readwrite("Wq_eV", &NEST::NESTcalc::Wvalue::Wq_eV)
		.def_readwrite("alpha", &NEST::NESTcalc::Wvalue::alpha);

	// Binding for the WIMP Spectrum Prep struct
	py::class_<TestSpectra::WIMP_spectrum_prep>(m, "WIMP_spectrum_prep", py::dynamic_attr())
		.def(py::init<>());

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

	//	Binding for the VDetector class
	//	py::nodelete added so that NESTcalc() deconstructor does
	//	not delete instance of VDetector()
	py::class_<VDetector, std::unique_ptr<VDetector, py::nodelete>>(m, "VDetector")	
		.def(py::init<>())
		.def("Initialization", &VDetector::Initialization)
		.def("get_g1", &VDetector::get_g1)
		.def("get_sPEres", &VDetector::get_sPEres)
		.def("get_sPEthr", &VDetector::get_sPEthr)
		.def("get_sPEeff", &VDetector::get_sPEeff)
		.def("get_P_dphe", &VDetector::get_P_dphe)

		.def("get_noiseBaseline", &VDetector::get_noiseBaseline)
		.def("get_noiseLinear", &VDetector::get_noiseLinear)
		.def("get_noiseQuadratic", &VDetector::get_noiseQuadratic)
		.def("get_coinWind", &VDetector::get_coinWind)
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
		.def("get_radmax", &VDetector::get_radmax)
		.def("get_TopDrift", &VDetector::get_TopDrift)
		.def("get_anode", &VDetector::get_anode)
		.def("get_cathode", &VDetector::get_cathode)
		.def("get_gate", &VDetector::get_gate)

		.def("get_molarMass", &VDetector::get_molarMass )

		.def("get_PosResExp", &VDetector::get_PosResExp)
		.def("get_PosResBase", &VDetector::get_PosResBase)

		.def("set_g1", &VDetector::set_g1)
		.def("set_sPEres", &VDetector::set_sPEres)
		.def("set_sPEthr", &VDetector::set_sPEthr)
		.def("set_sPEeff", &VDetector::set_sPEeff)
		.def("set_P_dphe", &VDetector::set_P_dphe)

		.def("set_noiseBaseline", &VDetector::set_noiseBaseline)
                .def("set_noiseLinear", &VDetector::set_noiseLinear)
                .def("set_noiseQuadratic", &VDetector::set_noiseQuadratic)
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
		.def("set_radmax", &VDetector::set_radmax)
		.def("set_TopDrift", &VDetector::set_TopDrift)
		.def("set_anode", &VDetector::set_anode)
		.def("set_cathode", &VDetector::set_cathode)
		.def("set_gate", &VDetector::set_gate)

		.def("set_molarMarr", &VDetector::set_molarMass)

		.def("set_PosResExp", &VDetector::set_PosResExp)
		.def("set_PosResBase", &VDetector::set_PosResBase)

		.def("FitS1", &VDetector::FitS1)
		.def("FitS2", &VDetector::FitS1)
		.def("FitEF", &VDetector::FitEF)
		.def("FitTBA", &VDetector::FitTBA)
		//    .def("FitS1", &VDetector::FitS1,
		//         py::arg("xpos_mm") = 0.,
		//         py::arg("ypos_mm") = 0.,
		//         py::arg("zpos_mm") = 0.,
		//         py::arg("LCE") = VDetector::LCE::unfold)
		//	.def("FitS2", &VDetector::FitS2,
		//	     py::arg("xpos_mm") = 0.,
		//         py::arg("ypos_mm") = 0.,
		//         py::arg("LCE") = VDetector::LCE::unfold)

		.def("OptTrans", &VDetector::OptTrans)
		.def("SinglePEWaveForm", &VDetector::SinglePEWaveForm);

	//	Binding for example XENON10
	py::class_<DetectorExample_XENON10, VDetector, std::unique_ptr<DetectorExample_XENON10, py::nodelete>>(m, "DetectorExample_XENON10")
		.def(py::init<>())
		.def("Initialization", &DetectorExample_XENON10::Initialization)
		.def("FitTBA", &DetectorExample_XENON10::FitTBA)
		.def("OptTrans", &DetectorExample_XENON10::OptTrans)
		.def("SinglePEWaveForm", &DetectorExample_XENON10::SinglePEWaveForm);
	
	//	Binding for example LUX_Run03
	py::class_<DetectorExample_LUX_RUN03, VDetector, std::unique_ptr<DetectorExample_LUX_RUN03, py::nodelete>>(m, "LUX_Run03")
		.def(py::init<>())
		.def("Initialization", &DetectorExample_LUX_RUN03::Initialization)
		.def("FitTBA", &DetectorExample_LUX_RUN03::FitTBA)
		.def("OptTrans", &DetectorExample_LUX_RUN03::OptTrans)
		.def("SinglePEWaveForm", &DetectorExample_LUX_RUN03::SinglePEWaveForm);

    //  Binding for example LZ_SR1
    py::class_<LZ_Detector, VDetector, std::unique_ptr<LZ_Detector, py::nodelete>>(m, "LZ_SR1")
        .def(py::init<>())
        .def("Initialization", &LZ_Detector::Initialization)
        .def("FitTBA", &LZ_Detector::FitTBA)
        .def("OptTrans", &LZ_Detector::OptTrans)
        .def("SinglePEWaveForm", &LZ_Detector::SinglePEWaveForm);

	// Binding for the TestSpectra class
	py::class_<TestSpectra, std::unique_ptr<TestSpectra, py::nodelete>>(m, "TestSpectra")
		.def(py::init<>())
		.def_static("CH3T_spectrum", 
			&TestSpectra::CH3T_spectrum, 
			py::arg("xMin") = 0.,
			py::arg("xMax") = 18.6
		)
		.def_static("C14_spectrum",
			&TestSpectra::C14_spectrum,
			py::arg("xMin") = 0.,
			py::arg("xMax") = 156.
		)
		.def_static("B8_spectrum", 
			&TestSpectra::B8_spectrum,
			py::arg("xMin") = 0.,
			py::arg("xMax") = 4.
		)
		.def_static("AmBe_spectrum", 
			&TestSpectra::AmBe_spectrum,
			py::arg("xMin") = 0.,
			py::arg("xMax") = 200.
		)
		.def_static("Cf_spectrum", 
			&TestSpectra::Cf_spectrum,
			py::arg("xMin") = 0.,
			py::arg("xMax") = 200.
		)
		.def_static("DD_spectrum",
			&TestSpectra::DD_spectrum,
			py::arg("xMin") = 0.,
			py::arg("xMax") = 80.,
			py::arg("expFall") =  10.,
			py::arg("peakFrac") = 0.1,
			py::arg("peakMu") = 60.,
			py::arg("peakSig") = 25.
		)
		.def_static("ppSolar_spectrum", 
			&TestSpectra::ppSolar_spectrum,
			py::arg("xMin") = 0.,
			py::arg("xMax") = 250.
		)
		.def_static("atmNu_spectrum",
			&TestSpectra::atmNu_spectrum,
			py::arg("xMin") = 0.,
			py::arg("xMax") = 85.
		)
		.def_static("WIMP_prep_spectrum", 
			&TestSpectra::WIMP_prep_spectrum,
			py::arg("mass") = 50.,
			py::arg("eStep") = 5.,
			py::arg("day")=0.
		)
		.def_static("WIMP_spectrum",
			&TestSpectra::WIMP_spectrum,
			py::arg("wprep"),
			py::arg("mass") = 50.,
			py::arg("day") = 0.
		);
		
	//	Binding for the NESTcalc class
	py::class_<NEST::NESTcalc, std::unique_ptr<NEST::NESTcalc, py::nodelete>>(m, "NESTcalc")
		//.def(py::init<>())
		.def(py::init<VDetector*>())
		.def_readonly_static("default_NRYieldsParam", &default_NRYieldsParam)
		.def_readonly_static("default_NRERWidthsParam", &default_NRERWidthsParam)
		.def_readonly_static("default_ERYieldsParam", &default_ERYieldsParam)
		//     .def_static("BinomFluct", &NEST::NESTcalc::BinomFluct)
		.def("FullCalculation", &NEST::NESTcalc::FullCalculation,
				"Perform the full yield calculation with smearings")
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
			py::arg("nuisance_parameters") = std::vector<double>({ 11., 1.1, 0.0480, -0.0533, 12.6, 0.3, 2., 0.3, 2., 0.5, 1., 1.})
		)
		.def("GetYields",
			&NEST::NESTcalc::GetYields,
			py::arg("interaction") = NEST::INTERACTION_TYPE::NR,
			py::arg("energy") = 100,
			py::arg("density") = 2.9,
			py::arg("drift_field") = 124,
			py::arg("A") = 131.293,
			py::arg("Z") = 54,
			py::arg("nuisance_parameters") = std::vector<double>({ 11., 1.1, 0.0480, -0.0533, 12.6, 0.3, 2., 0.3, 2., 0.5, 1., 1.}), 
			py::arg("ERYieldsParam") = std::vector<double>({-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.}),
			py::arg("oldModelER") = false
		)
		.def("GetQuanta", &NEST::NESTcalc::GetQuanta,
			py::arg("yields"),
			py::arg("density") = 2.9,
			py::arg("free_parameters") = std::vector<double>({0.4,0.4,0.04,0.5,0.19,2.25,1.,0.046452,0.205,0.45,-0.2}), 
				py::arg("oldModelER") = false,
			py::arg("SkewnessER") = -999.
		)   
		.def("GetS1", &NEST::NESTcalc::GetS1)
		.def("GetSpike", &NEST::NESTcalc::GetSpike)
		// Currently VDetector.FitTBA() requires we reinitialize the detector every time:
		.def("GetS2", &NEST::NESTcalc::GetS2)
		.def("CalculateG2", &NEST::NESTcalc::CalculateG2)
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
		.def("GetDetector", &NEST::NESTcalc::GetDetector);

		//	execNEST function
		m.def("execNEST", &execNEST);
		m.def("GetEnergyRes", &GetEnergyRes);
		m.def("GetBand", &GetBand);
		m.def("default_nr_yields_params", []() { return default_NRYieldsParam; });
		m.def("default_nrer_widths_params", []() { return default_NRERWidthsParam; });
		m.def("default_er_yields_params", []() { return default_ERYieldsParam; });

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
		.def("set_density", &NEST::LArNEST::setDensity)
		.def("set_r_ideal_gas", &NEST::LArNEST::setRIdealGas)
		.def("set_real_gas_a", &NEST::LArNEST::setRealGasA)
		.def("set_real_gas_b", &NEST::LArNEST::setRealGasB)
		.def("set_work_quanta_function", &NEST::LArNEST::setWorkQuantaFunction)
		.def("set_work_ion_function", &NEST::LArNEST::setWorkIonFunction)
		.def("set_work_photon_function", &NEST::LArNEST::setWorkPhotonFunction)
		.def("set_fano_er", &NEST::LArNEST::setFanoER)
		.def("set_nex_over_nion", &NEST::LArNEST::setNexOverNion)
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

		.def("get_density", &NEST::LArNEST::getDensity)
		.def("get_r_ideal_gas", &NEST::LArNEST::getRIdealGas)
		.def("get_real_gas_a", &NEST::LArNEST::getRealGasA)
		.def("get_real_gas_b", &NEST::LArNEST::getRealGasB)
		.def("get_work_quanta_function", &NEST::LArNEST::getWorkQuantaFunction)
		.def("get_work_ion_function", &NEST::LArNEST::getWorkIonFunction)
		.def("get_work_photon_function", &NEST::LArNEST::getWorkPhotonFunction)
		.def("get_fano_er", &NEST::LArNEST::getFanoER)
		.def("get_nex_over_nion", &NEST::LArNEST::getNexOverNion)
		.def("get_nr_yields_parameters", &NEST::LArNEST::getNRYieldsParameters)
		.def("get_er_yields_parameters", &NEST::LArNEST::getERYieldsParameters)
		.def("get_er_electron_yields_alpha_parameters", &NEST::LArNEST::getERElectronYieldsAlphaParameters)
		.def("get_er_electron_yields_beta_parameters", &NEST::LArNEST::getERElectronYieldsBetaParameters)
		.def("get_er_electron_yields_gamma_parameters", &NEST::LArNEST::getERElectronYieldsGammaParameters)
		.def("get_er_electron_yields_doke_birks_parameters", &NEST::LArNEST::getERElectronYieldsDokeBirksParameters)
		.def("get_thomas_imel_parameters", &NEST::LArNEST::getThomasImelParameters)
		.def("get_drift_parameters", &NEST::LArNEST::getDriftParameters)

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

}
