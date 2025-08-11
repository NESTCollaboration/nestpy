#ifndef spectra_h
#define spectra_h

#include <functional>
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
#include "execNEST.hh"

namespace py = pybind11;

// Function to vectorize spectra sampling (emin, emax)
py::array_t<double> fill_spectra(
	double emin, 
	double emax,
	int number,
	std::function<double(double, double)> spectra
);

py::array_t<double> fill_ws_spectra(
	double mass, 
	double eStep,
	double day,
	int number
);

// Function to vectorize spectra sampling (DD)
py::array_t<double>fill_spectra(
	double emin,
	double emax,
	double expFall,
	double peakFrac,
	double peakMu,
	double peakSig,
	int number,
	std::function<double(double, double, double, double, double, double)> spectra
);

void init_spectra(py::module& m);

#endif