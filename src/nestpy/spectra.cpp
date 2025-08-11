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

// Function to vectorise spectra sampling (emin, emax)
py::array_t<double> fill_spectra(
	double emin, 
	double emax,
	int number,
	std::function<double(double, double)> spectra
){
	auto vec = std::vector<double>(number);
	std::transform(vec.begin(), vec.end(), vec.begin(), [&](double _){return spectra(emin, emax);});
	return py::array(py::cast(vec));
}

// Function to vectorise WIMP sampling
py::array_t<double> fill_spectra(
	double mass, 
	double eStep,
	double day,
	int number
){
	auto ws = TestSpectra::WIMP_prep_spectrum(mass, eStep, day);
	auto vec = std::vector<double>(number);
	std::transform(vec.begin(), vec.end(), vec.begin(), [&](double _){return TestSpectra::WIMP_spectrum(ws, mass, 0);});
	return py::array(py::cast(vec));
}

// Function to vectorise spectra sampling (DD)
py::array_t<double>fill_spectra(
	double emin,
	double emax,
	double expFall,
	double peakFrac,
	double peakMu,
	double peakSig,
	double peakSkew,
	int number,
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
	py::class_<TestSpectra, std::unique_ptr<TestSpectra, py::nodelete>>(m, "spectra", py::module_local())
		.def(py::init<>())
		.def_static(
			"CH3T", 
			[](double emin, double emax, int number){return fill_spectra(emin, emax, number, &TestSpectra::CH3T_spectrum);},  
			py::arg("xMin") = 0.,
			py::arg("xMax") = 18.6,
			py::arg("number")
		)
		.def_static("C14",
			[](double emin, double emax, int number){return fill_spectra(emin, emax, number, &TestSpectra::C14_spectrum);},  
			py::arg("xMin") = 0.,
			py::arg("xMax") = 156.,
			py::arg("number")
		)
		.def_static("B8", 
			[](double emin, double emax, int number){return fill_spectra(emin, emax, number, &TestSpectra::B8_spectrum);},  
			py::arg("xMin") = 0.,
			py::arg("xMax") = 4.,
			py::arg("number")
		)
		.def_static("AmBe", 
			[](double emin, double emax, int number){return fill_spectra(emin, emax, number, &TestSpectra::AmBe_spectrum);},  
			py::arg("xMin") = 0.,
			py::arg("xMax") = 200.,
			py::arg("number")
		)
		.def_static("Cf", 
			[](double emin, double emax, int number){return fill_spectra(emin, emax, number, &TestSpectra::Cf_spectrum);},  
			py::arg("xMin") = 0.,
			py::arg("xMax") = 200.,
			py::arg("number")
		)
		.def_static("DD",
			[](double emin, double emax, double expFall, double peakFrac, double peakMu, double peakSig, double peakSkew, int number){
				return fill_spectra(emin, emax, expFall, peakFrac, peakMu, peakSig, peakSkew, number, &TestSpectra::DD_spectrum);
			},  
			py::arg("xMin") = 0.,
			py::arg("xMax") = 80.,
			py::arg("expFall") =  13.,
			py::arg("peakFrac") = 0.12,
			py::arg("peakMu") = 71.2,
			py::arg("peakSig") = 20.,
			py::arg("peakSkew") = -20.5,
            py::arg("number")
		)
		.def_static("ppSolar", 
			[](double emin, double emax, int number){return fill_spectra(emin, emax, number, &TestSpectra::ppSolar_spectrum);},  
			py::arg("xMin") = 0.,
			py::arg("xMax") = 250.,
			py::arg("number")
		)
		.def_static("atmNu",
			[](double emin, double emax, int number){return fill_spectra(emin, emax, number, &TestSpectra::atmNu_spectrum);},  
			py::arg("xMin") = 0.,
			py::arg("xMax") = 85.,
			py::arg("number")
		)
		.def_static("WIMP_prep", 
			&TestSpectra::WIMP_prep_spectrum,
			py::arg("mass") = 50.,
			py::arg("eStep") = 5.,
			py::arg("day")=0.
		)
		.def_static("WIMP",
			[](double mass, int number, double eStep, double day){return fill_spectra(mass, eStep, day, number);},  
			py::arg("mass"),
			py::arg("number"),
			py::arg("eStep") = 5.,
			py::arg("day")= 0.
		);
}