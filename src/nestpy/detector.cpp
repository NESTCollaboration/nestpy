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

void init_detector(py::module& m){

    auto m_detect = m.def_submodule("detectors", "detectors");

    //	Binding for example XENON10
    // py::class_<DetectorExample_XENON10, VDetector, std::unique_ptr<DetectorExample_XENON10, py::nodelete>>(m_detect, "DetectorExample_XENON10")
    // 	.def(py::init<>())
    // 	.def("Initialization", &DetectorExample_XENON10::Initialization)
    // 	.def("FitTBA", &DetectorExample_XENON10::FitTBA)
    // 	.def("OptTrans", &DetectorExample_XENON10::OptTrans)
    // 	.def("SinglePEWaveForm", &DetectorExample_XENON10::SinglePEWaveForm);
    
    // Binding for example LUX_Run03
    // py::class_<DetectorExample_LUX_RUN03, VDetector, std::unique_ptr<DetectorExample_LUX_RUN03, py::nodelete>>(m_detect, "LUX_Run03")
    // 	.def(py::init<>())
    // 	.def("Initialization", &DetectorExample_LUX_RUN03::Initialization)
    // 	.def("FitTBA", &DetectorExample_LUX_RUN03::FitTBA)
    // 	.def("OptTrans", &DetectorExample_LUX_RUN03::OptTrans)
    // 	.def("SinglePEWaveForm", &DetectorExample_LUX_RUN03::SinglePEWaveForm);

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
        .def_property_readonly("nr_yield_params", &LZ_Detector_2024::get_nr_yield_params)
        .def_property_readonly("er_yield_params", &LZ_Detector_2024::get_er_yield_params)
        .def_property_readonly("width_yield_params", &LZ_Detector_2024::get_nr_er_width_params);
}