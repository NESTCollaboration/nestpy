#include <algorithm>
#include <functional>
#include <pybind11/pybind11.h>

#include "TestSpectra.hh"

#include <pybind11/numpy.h>
#include <pybind11/stl_bind.h>
#include <pybind11/stl.h>
#include <pybind11/functional.h>

#include "spectra.hh"

namespace py = pybind11;
using namespace pybind11::literals; 

// Function to vectorise spectra sampling (emin, emax)
py::array_t<double> fill_spectra(
	int number,
	double emin, 
	double emax,
	std::function<double(double, double)> spectra
){
	auto vec = std::vector<double>(number);
	std::transform(vec.begin(), vec.end(), vec.begin(), [&](double _){return spectra(emin, emax);});
	return py::array(py::cast(vec));
}

// Function to vectorise WIMP sampling
py::array_t<double> fill_spectra(
	int number,
	double mass, 
	double eStep,
	double day
){
	auto ws = TestSpectra::WIMP_prep_spectrum(mass, eStep, day);
	auto vec = std::vector<double>(number);
	std::transform(vec.begin(), vec.end(), vec.begin(), [&](double _){return TestSpectra::WIMP_spectrum(ws, mass, day);});
	return py::array(py::cast(vec));
}

// Function to vectorise spectra sampling (DD)
py::array_t<double>fill_spectra(
	int number,
	double emin,
	double emax,
	double expFall,
	double peakFrac,
	double peakMu,
	double peakSig,
	double peakSkew,
	std::function<double(double, double, double, double, double, double, double)> spectra
){
	auto vec = std::vector<double>(number);
	std::transform(vec.begin(), vec.end(), vec.begin(), [&](double _){return spectra(emin, emax, expFall,
		peakFrac,
		peakMu,
		peakSig,
		peakSkew
	);});
	return py::array(py::cast(vec));
}

void init_spectra(py::module& m){

	auto m_spectra = m.def_submodule("spectra", "spectra");

	// Binding for the WIMP Spectrum Prep struct
	py::class_<TestSpectra::WIMP_spectrum_prep>(m_spectra, "WIMP_spectrum_prep", py::dynamic_attr())
		.def(py::init<>());

	m_spectra.def("CH3T_spectrum", 
		&TestSpectra::CH3T_spectrum, 
		py::arg("xMin") = 0.,
		py::arg("xMax") = 18.6
	);
	m_spectra.def("C14_spectrum",
		&TestSpectra::C14_spectrum,
		py::arg("xMin") = 0.,
		py::arg("xMax") = 156.
	);
	m_spectra.def("B8_spectrum", 
		&TestSpectra::B8_spectrum,
		py::arg("xMin") = 0.,
		py::arg("xMax") = 4.
	);
	m_spectra.def("AmBe_spectrum", 
		&TestSpectra::AmBe_spectrum,
		py::arg("xMin") = 0.,
		py::arg("xMax") = 200.
	);
	m_spectra.def("Cf_spectrum", 
		&TestSpectra::Cf_spectrum,
		py::arg("xMin") = 0.,
		py::arg("xMax") = 200.
	);
	m_spectra.def("DD_spectrum",
		&TestSpectra::DD_spectrum,
		py::arg("xMin") = 0.,
		py::arg("xMax") = 80.,
		py::arg("expFall") =  10.,
		py::arg("peakFrac") = 0.1,
		py::arg("peakMu") = 60.,
		py::arg("peakSig") = 25.,
		py::arg("peakSkew") = 0.
	);
	m_spectra.def("ppSolar_spectrum", 
		&TestSpectra::ppSolar_spectrum,
		py::arg("xMin") = 0.,
		py::arg("xMax") = 250.
	);
	m_spectra.def("atmNu_spectrum",
		&TestSpectra::atmNu_spectrum,
		py::arg("xMin") = 0.,
		py::arg("xMax") = 85.
	);
	m_spectra.def("WIMP_prep_spectrum", 
		&TestSpectra::WIMP_prep_spectrum,
		py::arg("mass") = 50.,
		py::arg("eStep") = 5.,
		py::arg("day")=0.
	);
	m_spectra.def("WIMP_spectrum",
		&TestSpectra::WIMP_spectrum,
		py::arg("wprep"),
		py::arg("mass") = 50.,
		py::arg("day") = 0.
	);
	m_spectra.def(
		"CH3T", 
		[](int number, double emin, double emax){return fill_spectra(number, emin, emax, &TestSpectra::CH3T_spectrum);},  
		py::arg("number"),
		py::arg("xMin") = 0.,
		py::arg("xMax") = 18.6
	);
	m_spectra.def("C14",
		[](int number, double emin, double emax){return fill_spectra(number, emin, emax, &TestSpectra::C14_spectrum);},  
		py::arg("number"),
		py::arg("xMin") = 0.,
		py::arg("xMax") = 156.
	);
	m_spectra.def("B8", 
		[](int number, double emin, double emax){return fill_spectra(number, emin, emax, &TestSpectra::B8_spectrum);},  
		py::arg("number"),
		py::arg("xMin") = 0.,
		py::arg("xMax") = 4.
	);
	m_spectra.def("AmBe", 
		[](int number, double emin, double emax){return fill_spectra(number, emin, emax, &TestSpectra::AmBe_spectrum);},  
		py::arg("number"),
		py::arg("xMin") = 0.,
		py::arg("xMax") = 200.
	);
	m_spectra.def("Cf", 
		[](int number, double emin, double emax){return fill_spectra(number, emin, emax, &TestSpectra::Cf_spectrum);},  
		py::arg("number"),
		py::arg("xMin") = 0.,
		py::arg("xMax") = 200.
	);
	m_spectra.def("DD",
		[](int number, double emin, double emax, double expFall, double peakFrac, double peakMu, double peakSig, double peakSkew){
			return fill_spectra(number, emin, emax, expFall, peakFrac, peakMu, peakSig, peakSkew, &TestSpectra::DD_spectrum);
		},  
		py::arg("number"),
		py::arg("xMin") = 0.,
		py::arg("xMax") = 80.,
		py::arg("expFall") =  13.,
		py::arg("peakFrac") = 0.12,
		py::arg("peakMu") = 71.2,
		py::arg("peakSig") = 20.,
		py::arg("peakSkew") = -20.5
	);
	m_spectra.def("ppSolar", 
		[](int number, double emin, double emax){return fill_spectra(number, emin, emax, &TestSpectra::ppSolar_spectrum);},  
		py::arg("number"),
		py::arg("xMin") = 0.,
		py::arg("xMax") = 250.
	);
	m_spectra.def("atmNu",
		[](int number, double emin, double emax){return fill_spectra(number, emin, emax, &TestSpectra::atmNu_spectrum);},  
		py::arg("number"),
		py::arg("xMin") = 0.,
		py::arg("xMax") = 85.
	);
	m_spectra.def("WIMP_prep", 
		&TestSpectra::WIMP_prep_spectrum,
		py::arg("mass") = 50.,
		py::arg("eStep") = 5.,
		py::arg("day")=0.
	);
	m_spectra.def("WIMP",
		[](int number, double mass, double eStep, double day){return fill_spectra(number, mass, eStep, day);},  
		py::arg("number"),
		py::arg("mass"),
		py::arg("eStep") = 5.,
		py::arg("day")= 0.
	);

	// Binding for the TestSpectra class
	// py::class_<TestSpectra, std::unique_ptr<TestSpectra, py::nodelete>>(m, "spectra", py::module_local());
		// .def(py::init<>());
		// 		m_spectra.def("CH3T_spectrum", 
		// 	&TestSpectra::CH3T_spectrum, 
		// 	py::arg("xMin") = 0.,
		// 	py::arg("xMax") = 18.6
		// );
		// m_spectra.def("C14_spectrum",
		// 	&TestSpectra::C14_spectrum,
		// 	py::arg("xMin") = 0.,
		// 	py::arg("xMax") = 156.
		// );
		// m_spectra.def("B8_spectrum", 
		// 	&TestSpectra::B8_spectrum,
		// 	py::arg("xMin") = 0.,
		// 	py::arg("xMax") = 4.
		// );
		// m_spectra.def("AmBe_spectrum", 
		// 	&TestSpectra::AmBe_spectrum,
		// 	py::arg("xMin") = 0.,
		// 	py::arg("xMax") = 200.
		// );
		// m_spectra.def("Cf_spectrum", 
		// 	&TestSpectra::Cf_spectrum,
		// 	py::arg("xMin") = 0.,
		// 	py::arg("xMax") = 200.
		// );
		// m_spectra.def("DD_spectrum",
		// 	&TestSpectra::DD_spectrum,
		// 	py::arg("xMin") = 0.,
		// 	py::arg("xMax") = 80.,
		// 	py::arg("expFall") =  10.,
		// 	py::arg("peakFrac") = 0.1,
		// 	py::arg("peakMu") = 60.,
		// 	py::arg("peakSig") = 25.,
		// 	py::arg("peakSkew") = 0.
		// );
		// m_spectra.def("ppSolar_spectrum", 
		// 	&TestSpectra::ppSolar_spectrum,
		// 	py::arg("xMin") = 0.,
		// 	py::arg("xMax") = 250.
		// );
		// m_spectra.def("atmNu_spectrum",
		// 	&TestSpectra::atmNu_spectrum,
		// 	py::arg("xMin") = 0.,
		// 	py::arg("xMax") = 85.
		// );
		// m_spectra.def("WIMP_prep_spectrum", 
		// 	&TestSpectra::WIMP_prep_spectrum,
		// 	py::arg("mass") = 50.,
		// 	py::arg("eStep") = 5.,
		// 	py::arg("day")=0.
		// );
		// m_spectra.def("WIMP_spectrum",
		// 	&TestSpectra::WIMP_spectrum,
		// 	py::arg("wprep"),
		// 	py::arg("mass") = 50.,
		// 	py::arg("day") = 0.
		// );
		// m_spectra.def(
		// 	"CH3T", 
		// 	[](int number, double emin, double emax){return fill_spectra(number, emin, emax, &TestSpectra::CH3T_spectrum);},  
		// 	py::arg("number"),
		// 	py::arg("xMin") = 0.,
		// 	py::arg("xMax") = 18.6
		// );
		// m_spectra.def("C14",
		// 	[](int number, double emin, double emax){return fill_spectra(number, emin, emax, &TestSpectra::C14_spectrum);},  
		// 	py::arg("number"),
		// 	py::arg("xMin") = 0.,
		// 	py::arg("xMax") = 156.
		// );
		// m_spectra.def("B8", 
		// 	[](int number, double emin, double emax){return fill_spectra(number, emin, emax, &TestSpectra::B8_spectrum);},  
		// 	py::arg("number"),
		// 	py::arg("xMin") = 0.,
		// 	py::arg("xMax") = 4.
		// );
		// m_spectra.def("AmBe", 
		// 	[](int number, double emin, double emax){return fill_spectra(number, emin, emax, &TestSpectra::AmBe_spectrum);},  
		// 	py::arg("number"),
		// 	py::arg("xMin") = 0.,
		// 	py::arg("xMax") = 200.
		// );
		// m_spectra.def("Cf", 
		// 	[](int number, double emin, double emax){return fill_spectra(number, emin, emax, &TestSpectra::Cf_spectrum);},  
		// 	py::arg("number"),
		// 	py::arg("xMin") = 0.,
		// 	py::arg("xMax") = 200.
		// );
		// m_spectra.def("DD",
		// 	[](int number, double emin, double emax, double expFall, double peakFrac, double peakMu, double peakSig, double peakSkew){
		// 		return fill_spectra(number, emin, emax, expFall, peakFrac, peakMu, peakSig, peakSkew, &TestSpectra::DD_spectrum);
		// 	},  
		// 	py::arg("number"),
		// 	py::arg("xMin") = 0.,
		// 	py::arg("xMax") = 80.,
		// 	py::arg("expFall") =  13.,
		// 	py::arg("peakFrac") = 0.12,
		// 	py::arg("peakMu") = 71.2,
		// 	py::arg("peakSig") = 20.,
		// 	py::arg("peakSkew") = -20.5
		// );
		// m_spectra.def("ppSolar", 
		// 	[](int number, double emin, double emax){return fill_spectra(number, emin, emax, &TestSpectra::ppSolar_spectrum);},  
		// 	py::arg("number"),
		// 	py::arg("xMin") = 0.,
		// 	py::arg("xMax") = 250.
		// );
		// m_spectra.def("atmNu",
		// 	[](int number, double emin, double emax){return fill_spectra(number, emin, emax, &TestSpectra::atmNu_spectrum);},  
		// 	py::arg("number"),
		// 	py::arg("xMin") = 0.,
		// 	py::arg("xMax") = 85.
		// );
		// m_spectra.def("WIMP_prep", 
		// 	&TestSpectra::WIMP_prep_spectrum,
		// 	py::arg("mass") = 50.,
		// 	py::arg("eStep") = 5.,
		// 	py::arg("day")=0.
		// );
		// m_spectra.def("WIMP",
		// 	[](int number, double mass, double eStep, double day){return fill_spectra(number, mass, eStep, day);},  
		// 	py::arg("number"),
		// 	py::arg("mass"),
		// 	py::arg("eStep") = 5.,
		// 	py::arg("day")= 0.
		// );
}