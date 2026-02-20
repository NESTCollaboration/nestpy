#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include "detector.hh"

#include <iostream>
#include "NEST.hh"
#include "VDetector.hh"
#include "LUX_Run03.hh"
#include "LZ_WS2022.hh"
#include "LZ_WS2024.hh"
#include "DetectorExample_XENON10.hh"

namespace py = pybind11;
using namespace pybind11::literals; 

py::dict get_extraction_parameters(VDetector* detector, int verbosity = 0) {
	auto results = NEST::NESTcalc(detector).CalculateG2(verbosity);
	py::dict d;
	d["elYield"] = results[0];
	d["ExtEff"] = results[1];
	d["SE"] = results[2];
	d["g2"] = results[3];
	d["gasGap"] = results[4];
	d["valid"] = static_cast<float>(results[2] > 0);
	return d;
}


void init_detector(py::module& m){

    auto m_detect = m.def_submodule("detectors", "detectors");

    	//	Binding for the VDetector class
	//	py::nodelete added so that NESTcalc() deconstructor does
	//	not delete instance of VDetector()
	py::class_<VDetector, std::unique_ptr<VDetector, py::nodelete>>(m_detect, "VDetector")	
		.def(py::init<>())
		.def("Initialization", &VDetector::Initialization)
		.def("get_name", &VDetector::getName)
		.def_property_readonly("name", &VDetector::getName)

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

		.def("set_molarMass", &VDetector::set_molarMass)

		.def("set_PosResExp", &VDetector::set_PosResExp)
		.def("set_PosResBase", &VDetector::set_PosResBase)

		.def_property("g1", &VDetector::get_g1, &VDetector::set_g1)
		.def_property("sPEres", &VDetector::get_sPEres, &VDetector::set_sPEres)
		.def_property("sPEthr", &VDetector::get_sPEthr, &VDetector::set_sPEthr)
		.def_property("sPEeff", &VDetector::get_sPEeff, &VDetector::set_sPEeff)
		.def_property("P_dphe", &VDetector::get_P_dphe, &VDetector::set_P_dphe)

		.def_property("noiseBaseline", &VDetector::get_noiseBaseline, &VDetector::set_noiseBaseline)
        .def_property("noiseLinear", &VDetector::get_noiseLinear, &VDetector::set_noiseLinear)
        .def_property("noiseQuadratic", &VDetector::get_noiseQuadratic, &VDetector::set_noiseQuadratic)
		.def_property("coinWind", &VDetector::get_coinWind, &VDetector::set_coinWind)
		.def_property("coinLevel", &VDetector::get_coinLevel, &VDetector::set_coinLevel)
		.def_property("numPMTs", &VDetector::get_numPMTs, &VDetector::set_numPMTs)

		.def_property("g1_gas", &VDetector::get_g1_gas, &VDetector::set_g1_gas)
		.def_property("s2Fano", &VDetector::get_s2Fano, &VDetector::set_s2Fano)
		.def_property("s2_thr", &VDetector::get_s2_thr, &VDetector::set_s2_thr)
		//.d_propertye"t_S2botTotRatio", &VDetector::get_S2botTotRatio, &VDetector::set_S2botTotRatio)
		.def_property("E_gas", &VDetector::get_E_gas, &VDetector::set_E_gas)
		.def_property("eLife_us", &VDetector::get_eLife_us, &VDetector::set_eLife_us)

		.def_property("inGas", &VDetector::get_inGas, &VDetector::set_inGas)
		.def_property("T_Kelvin", &VDetector::get_T_Kelvin, &VDetector::set_T_Kelvin)
		.def_property("p_bar", &VDetector::get_p_bar, &VDetector::set_p_bar)

		.def_property("dtCntr", &VDetector::get_dtCntr, &VDetector::set_dtCntr)
		.def_property("dt_min", &VDetector::get_dt_min, &VDetector::set_dt_min)
		.def_property("dt_max", &VDetector::get_dt_max, &VDetector::set_dt_max)
		.def_property("radius", &VDetector::get_radius, &VDetector::set_radius)
		.def_property("radmax", &VDetector::get_radmax, &VDetector::set_radmax)
		.def_property("TopDrift", &VDetector::get_TopDrift, &VDetector::set_TopDrift)
		.def_property("anode", &VDetector::get_anode, &VDetector::set_anode)
		.def_property("cathode", &VDetector::get_cathode, &VDetector::set_cathode)
		.def_property("gate", &VDetector::get_gate, &VDetector::set_gate)

		.def_property("molarMass", &VDetector::get_molarMass, &VDetector::set_molarMass)

		.def_property("PosResExp", &VDetector::get_PosResExp, &VDetector::set_PosResExp)
		.def_property("PosResBase", &VDetector::get_PosResBase, &VDetector::set_PosResBase)

		.def_property_readonly("g2",[](VDetector *self){return NEST::NESTcalc(self).CalculateG2(0).at(3);})
		.def_property_readonly("extraction_parameters", [](VDetector *self){return get_extraction_parameters(self, 0);})
		
		// Have to set "inGas" like this to solve reference issues
		.def("calculate_density_liquid", [](VDetector* self, double temperature, double pressure, double molarMass){bool inGas = false; return NEST::NESTcalc::GetDensity(temperature, pressure, inGas, 0, molarMass);}, "temperature"_a, "pressure"_a, "molarMass"_a = 131.293 )
		.def("calculate_density_gas", [](VDetector* self, double temperature, double pressure, double molarMass){bool inGas = true; return NEST::NESTcalc::GetDensity(temperature, pressure, inGas, 0, molarMass);}, "temperature"_a, "pressure"_a, "molarMass"_a = 131.293 )

		.def_property_readonly("density_liquid", [](VDetector *self){bool inGas = false; return NEST::NESTcalc::GetDensity(self->get_T_Kelvin(), self->get_p_bar(), inGas, 0, self->get_molarMass());})
		.def_property_readonly("density_gas", [](VDetector *self){bool inGas = true; return NEST::NESTcalc::GetDensity(self->get_T_Kelvin(), self->get_p_bar(), inGas, 0, self->get_molarMass());})

		.def("FitS1", &VDetector::FitS1)
		.def("FitS2", &VDetector::FitS1)
		.def("FitEF", &VDetector::FitEF)
		.def("FitTBA", &VDetector::FitTBA)

		.def("get_field", &VDetector::FitEF, "x_mm"_a, "y_mm"_a, "z_mm"_a)
		.def_property_readonly("field_at_center", [](VDetector* self){return self->FitEF(0, 0, self->get_TopDrift()/2);})

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
		.def("get_optical_transport_time", &VDetector::OptTrans, "x_mm"_a = 0, "y_mm"_a = 0, "z_mm"_a)
		.def("SinglePEWaveForm", &VDetector::SinglePEWaveForm);

	//	Binding for example XENON10
	py::class_<DetectorExample_XENON10, VDetector, std::unique_ptr<DetectorExample_XENON10, py::nodelete>>(m_detect, "DetectorExample_XENON10")
		.def(py::init<>())
		.def("Initialization", &DetectorExample_XENON10::Initialization)
		.def("FitTBA", &DetectorExample_XENON10::FitTBA)
		.def("OptTrans", &DetectorExample_XENON10::OptTrans)
		.def("SinglePEWaveForm", &DetectorExample_XENON10::SinglePEWaveForm);
	
	//	Binding for example LUX_Run03
	py::class_<DetectorExample_LUX_RUN03, VDetector, std::unique_ptr<DetectorExample_LUX_RUN03, py::nodelete>>(m_detect, "LUX_Run03")
		.def(py::init<>())
		.def("Initialization", &DetectorExample_LUX_RUN03::Initialization)
		.def("FitTBA", &DetectorExample_LUX_RUN03::FitTBA)
		.def("OptTrans", &DetectorExample_LUX_RUN03::OptTrans)
		.def("SinglePEWaveForm", &DetectorExample_LUX_RUN03::SinglePEWaveForm);

    //  Binding for LUX-ZEPLIN's WS2022 result
    py::class_<LZ_Detector_2022, VDetector, std::unique_ptr<LZ_Detector_2022, py::nodelete>>(m_detect, "LZ_WS2022")
        .def(py::init<>())
        .def("Initialization", &LZ_Detector_2022::Initialization)
        .def("FitTBA", &LZ_Detector_2022::FitTBA)
        .def("OptTrans", &LZ_Detector_2022::OptTrans)
        .def("SinglePEWaveForm", &LZ_Detector_2022::SinglePEWaveForm);

    py::class_<LZ_Detector_2024, VDetector, std::unique_ptr<LZ_Detector_2024, py::nodelete>>(m_detect, "LZ_WS2024")
        .def(py::init<>())
        .def("Initialization", &LZ_Detector_2024::Initialization)
        .def("FitTBA", &LZ_Detector_2024::FitTBA)
        .def("OptTrans", &LZ_Detector_2024::OptTrans)
        .def("SinglePEWaveForm", &LZ_Detector_2024::SinglePEWaveForm)
        .def_property_readonly("nr_yield_parameters", &LZ_Detector_2024::get_nr_yield_params)
        .def_property_readonly("er_yield_parameters", &LZ_Detector_2024::get_er_yield_params)
        .def_property_readonly("nr_er_width_parameters", &LZ_Detector_2024::get_nr_er_width_params);
}