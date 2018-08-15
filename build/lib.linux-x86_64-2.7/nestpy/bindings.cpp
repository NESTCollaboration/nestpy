#include <pybind11/pybind11.h>
#include "NEST.hh"
#include "VDetector.hh"
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

  //	Binding for the VDetector class
  py::class_<VDetector>(m, "VDetector")
	.def(py::init<>())
	.def("Initialization", &VDetector::Initialization)
	.def("get_g1", &VDetector::get_g1)
	.def("get_sPEres", &VDetector::get_sPEres)
	.def("get_sPEthr", &VDetector::get_sPEthr)
	.def("get_sPEeff", &VDetector::get_sPEeff)
	.def("get_noise", &VDetector::get_noise)
	.def("get_P_dphe", &VDetector::get_P_dphe)

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
	.def("get_TopDrift", &VDetector::get_TopDrift)
	.def("get_anode", &VDetector::get_anode)
	.def("get_cathode", &VDetector::get_cathode)
	.def("get_gate", &VDetector::get_gate)

	.def("get_PosResExp", &VDetector::get_PosResExp)
	.def("get_PosResBase", &VDetector::get_PosResBase)

	.def("set_g1", &VDetector::set_g1)
	.def("set_sPEres", &VDetector::set_sPEres)
	.def("set_sPEthr", &VDetector::set_sPEthr)
	.def("set_sPEeff", &VDetector::set_sPEeff)
	.def("set_noise", &VDetector::set_noise)
	.def("set_P_dphe", &VDetector::set_P_dphe)

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
	.def("set_TopDrift", &VDetector::set_TopDrift)
	.def("set_anode", &VDetector::set_anode)
	.def("set_cathode", &VDetector::set_cathode)
	.def("set_gate", &VDetector::set_gate)

	.def("set_PosResExp", &VDetector::set_PosResExp)
	.def("set_PosResBase", &VDetector::set_PosResBase)

	.def("FitS1", &VDetector::FitS1)
	.def("FitEF", &VDetector::FitEF)
	.def("FitS2", &VDetector::FitS2)

	.def("OptTrans", &VDetector::OptTrans)
  	.def("SinglePEWaveForm", &VDetector::SinglePEWaveForm);

  //	Binding for the NESTcalc class
  py::class_<NEST::NESTcalc>(m, "NESTcalc")
    .def(py::init<>())
	.def(py::init<VDetector*>())
    .def("BinomFluct", &NEST::NESTcalc::BinomFluct)
	.def("SetDensity", &NEST::NESTcalc::SetDensity)
	.def("GetSpike", &NEST::NESTcalc::GetSpike)
	.def("CalculateG2", &NEST::NESTcalc::CalculateG2)
	.def("SetDriftVelocity", &NEST::NESTcalc::SetDriftVelocity)
	.def("SetDriftVelocity_MagBoltz", &NEST::NESTcalc::SetDriftVelocity_MagBoltz)
	.def("SetDriftVelocity_NonUniform", &NEST::NESTcalc::SetDriftVelocity_NonUniform)
	.def("xyResolution", &NEST::NESTcalc::xyResolution)

	//NESTresult FullCalculation(INTERACTION_TYPE species,double energy,double density,double dfield,double A,double Z,std::vector<double> NuisParam={1,1});
	//double PhotonTime(INTERACTION_TYPE species,bool exciton, double dfield, double energy);
	//photonstream AddPhotonTransportTime (photonstream emitted_times, double x, double y, double z);
	//photonstream GetPhotonTimes(INTERACTION_TYPE species, int total_photons, int excitons, double dfield, double energy);
	//YieldResult GetYields ( INTERACTION_TYPE species, double energy, double density, double dfield,double A,double Z,std::vector<double> NuisParam);
	//QuantaResult GetQuanta(YieldResult yields, double density);
	//std::vector<double> GetS1 ( QuantaResult quanta, double dx, double dy, double dz, double driftSpeed, double dS_mid, INTERACTION_TYPE species, long evtNum, double dfield, double energy, bool useTiming,  bool outputTiming, vector<long int>& wf_time, vector<double>& wf_amp );

    ;
}

//std::vector<double> GetSpike(int Nph,double dx,double dy, double dz, double driftSpeed, double dS_mid, std::vector<double> origScint );
//std::vector<double> GetS2 ( int Ne, double dx, double dy, double dt, double driftSpeed, long evtNum, double dfield, bool useTiming, bool outputTiming, vector<long int>& wf_time, vector<double>& wf_amp,vector<double> &g2_params );


