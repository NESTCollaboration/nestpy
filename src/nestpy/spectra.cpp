#include <algorithm>
#include <functional>
#include <pybind11/pybind11.h>
#include "NEST.hh"
#include "LArNEST.hh"
#include "VDetector.hh"
#include "execNEST.hh"
#include "TestSpectra.hh"
#include "LUX_Run03.hh"
#include "DetectorExample_XENON10.hh"
#include <pybind11/numpy.h>
#include <pybind11/stl_bind.h>
#include <pybind11/stl.h>
#include <pybind11/functional.h>
#include "execNEST.hh"

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
	std::transform(vec.begin(), vec.end(), vec.begin(), [&](double _){return TestSpectra::WIMP_spectrum(ws, mass, 0);});
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
	// Binding for the TestSpectra class

// Binding for the WIMP Spectrum Prep struct
	py::class_<TestSpectra::WIMP_spectrum_prep>(m, "WIMP_spectrum_prep", py::dynamic_attr())
		.def(py::init<>());

	// Binding for the TestSpectra class
	py::class_<TestSpectra, std::unique_ptr<TestSpectra, py::nodelete>>(m, "spectra", py::module_local())
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
			py::arg("peakSig") = 25.,
			py::arg("peakSkew") = 0.
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
		)
		.def_static(
			"CH3T", 
			[](int number, double emin, double emax){return fill_spectra(number, emin, emax, &TestSpectra::CH3T_spectrum);},  
			py::arg("number"),
			py::arg("xMin") = 0.,
			py::arg("xMax") = 18.6
		)
		.def_static("C14",
			[](int number, double emin, double emax){return fill_spectra(number, emin, emax, &TestSpectra::C14_spectrum);},  
			py::arg("number"),
			py::arg("xMin") = 0.,
			py::arg("xMax") = 156.
		)
		.def_static("B8", 
			[](int number, double emin, double emax){return fill_spectra(number, emin, emax, &TestSpectra::B8_spectrum);},  
			py::arg("number"),
			py::arg("xMin") = 0.,
			py::arg("xMax") = 4.
		)
		.def_static("AmBe", 
			[](int number, double emin, double emax){return fill_spectra(number, emin, emax, &TestSpectra::AmBe_spectrum);},  
			py::arg("number"),
			py::arg("xMin") = 0.,
			py::arg("xMax") = 200.
		)
		.def_static("Cf", 
			[](int number, double emin, double emax){return fill_spectra(number, emin, emax, &TestSpectra::Cf_spectrum);},  
			py::arg("number"),
			py::arg("xMin") = 0.,
			py::arg("xMax") = 200.
		)
		.def_static("DD",
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
		)
		.def_static("ppSolar", 
			[](int number, double emin, double emax){return fill_spectra(number, emin, emax, &TestSpectra::ppSolar_spectrum);},  
			py::arg("number"),
			py::arg("xMin") = 0.,
			py::arg("xMax") = 250.
		)
		.def_static("atmNu",
			[](int number, double emin, double emax){return fill_spectra(number, emin, emax, &TestSpectra::atmNu_spectrum);},  
			py::arg("number"),
			py::arg("xMin") = 0.,
			py::arg("xMax") = 85.
		)
		.def_static("WIMP_prep", 
			&TestSpectra::WIMP_prep_spectrum,
			py::arg("mass") = 50.,
			py::arg("eStep") = 5.,
			py::arg("day")=0.
		)
		.def_static("WIMP",
			[](int number, double mass, double eStep, double day){return fill_spectra(number, mass, eStep, day);},  
			py::arg("number"),
			py::arg("mass"),
			py::arg("eStep") = 5.,
			py::arg("day")= 0.
		);
}