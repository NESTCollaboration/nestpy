#include <pybind11/numpy.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include <algorithm>
#include <cstdint>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

#include "NEST.hh"
#include "execNEST.hh"

namespace py = pybind11;
using namespace pybind11::literals;


// numpy arrays of doubles, converted (e.g. from lists) only when necessary
using double_array = py::array_t<double, py::array::c_style | py::array::forcecast>;

// Read-only numpy view of a field, sharing its memory and keeping owner alive
template <typename T>
static py::array_t<T> field_view(const std::vector<T>& field, py::handle owner){
    py::array_t<T> view(field.size(), field.data(), owner);
    view.attr("setflags")("write"_a = false);
    return view;
}

// Variable-length field as an awkward array with one list per event (copied)
template <typename T>
static py::object ragged_field(const std::vector<std::vector<T>>& field){
    py::array_t<int64_t> counts(field.size());
    size_t total = 0;
    for (size_t i = 0; i < field.size(); ++i){
        counts.mutable_at(i) = static_cast<int64_t>(field[i].size());
        total += field[i].size();
    }
    py::array_t<T> content(total);
    T* out = content.mutable_data();
    for (const auto& event : field)
        out = std::copy(event.begin(), event.end(), out);
    return py::module_::import("awkward").attr("unflatten")(content, counts);
}

// Getter for a field: one value per event gives a numpy view, a list per event
// gives an awkward array
template <typename T>
static auto field_getter(std::vector<T> NESTObservableArray::*field){
    return [field](py::object self){
        return field_view(self.cast<const NESTObservableArray&>().*field, self);
    };
}

template <typename T>
static auto field_getter(std::vector<std::vector<T>> NESTObservableArray::*field){
    return [field](const NESTObservableArray& self){ return ragged_field(self.*field); };
}

// runNESTvec taking energies of shape (n,) and positions of shape (n, 3) as numpy arrays
static NESTObservableArray runNESTvec_numpy(
    VDetector* detector,
    INTERACTION_TYPE particleType,
    double_array energies,
    double_array positions,
    double inField,
    int seed,
    std::vector<double> ERYieldsParam,
    std::vector<double> NRYieldsParam,
    std::vector<double> NRERWidthsParam,
    S1CalculationMode s1mode,
    S2CalculationMode s2mode,
    bool calculate_times
){
    const size_t n_events = energies.size();
    if (energies.ndim() != 1)
        throw std::invalid_argument("energies must be 1-dimensional");
    if (n_events > 0 and (positions.ndim() != 2 or positions.shape(1) != 3))
        throw std::invalid_argument("positions must have shape (n_events, 3)");
    if (positions.size() != 3 * n_events)
        throw std::invalid_argument("energies and positions must have the same length");

    const double* e = energies.data();
    const double* p = positions.data();
    std::vector<double> eList(e, e + n_events);
    std::vector<std::vector<double>> pos3dxyz;
    pos3dxyz.reserve(n_events);
    for (size_t i = 0; i < n_events; ++i)
        pos3dxyz.push_back({p[3 * i], p[3 * i + 1], p[3 * i + 2]});

    // The GIL is deliberately kept: NEST's random number generator is a shared
    // global, so concurrent calls from Python threads would race on it
    return runNESTvec(detector, particleType, std::move(eList), std::move(pos3dxyz),
                      inField, seed, std::move(ERYieldsParam), std::move(NRYieldsParam),
                      std::move(NRERWidthsParam), s1mode, s2mode, calculate_times);
}


void init_array(py::module& m){
    auto m_array = m.def_submodule("array", "array");

    py::class_<NESTObservableArray> observables(m_array, "NESTObservableArray", py::dynamic_attr());
    observables.def(py::init<>());

    // Each field becomes a read-only attribute and a field of runNESTvec's output
    std::vector<std::string> field_names;
    auto add_field = [&](const char* name, auto member){
        observables.def_property_readonly(name, field_getter(member));
        field_names.push_back(name);
    };
    add_field("s1_nhits", &NESTObservableArray::s1_nhits);
    add_field("s1_nhits_thr", &NESTObservableArray::s1_nhits_thr);
    add_field("s1_nhits_dpe", &NESTObservableArray::s1_nhits_dpe);
    add_field("s1r_phe", &NESTObservableArray::s1r_phe);
    add_field("s1c_phe", &NESTObservableArray::s1c_phe);
    add_field("s1r_phd", &NESTObservableArray::s1r_phd);
    add_field("s1c_phd", &NESTObservableArray::s1c_phd);
    add_field("s1r_spike", &NESTObservableArray::s1r_spike);
    add_field("s1c_spike", &NESTObservableArray::s1c_spike);
    add_field("s2_Nee", &NESTObservableArray::s2_Nee);
    add_field("s2_Nph", &NESTObservableArray::s2_Nph);
    add_field("s2_nhits", &NESTObservableArray::s2_nhits);
    add_field("s2_nhits_dpe", &NESTObservableArray::s2_nhits_dpe);
    add_field("s2r_phe", &NESTObservableArray::s2r_phe);
    add_field("s2c_phe", &NESTObservableArray::s2c_phe);
    add_field("s2r_phd", &NESTObservableArray::s2r_phd);
    add_field("s2c_phd", &NESTObservableArray::s2c_phd);
    add_field("s1_waveform_time", &NESTObservableArray::s1_waveform_time);
    add_field("s1_waveform_amp", &NESTObservableArray::s1_waveform_amp);
    add_field("s2_waveform_time", &NESTObservableArray::s2_waveform_time);
    add_field("s2_waveform_amp", &NESTObservableArray::s2_waveform_amp);
    add_field("n_electrons", &NESTObservableArray::n_electrons);
    add_field("n_photons", &NESTObservableArray::n_photons);
    add_field("s1_photon_times", &NESTObservableArray::s1_photon_times);

    m_array.def("runNESTvec",
        [field_names](VDetector* detector, INTERACTION_TYPE particleType,
                      double_array energies, double_array positions,
                      double inField, int seed,
                      std::vector<double> ERYieldsParam,
                      std::vector<double> NRYieldsParam,
                      std::vector<double> NRERWidthsParam,
                      S1CalculationMode s1mode, S2CalculationMode s2mode,
                      bool calculate_times){
            // The C++ result owns the memory that the numpy fields point into
            py::object result = py::cast(runNESTvec_numpy(
                detector, particleType, std::move(energies), std::move(positions),
                inField, seed, std::move(ERYieldsParam), std::move(NRYieldsParam),
                std::move(NRERWidthsParam), s1mode, s2mode, calculate_times));
            py::dict columns;
            for (const auto& name : field_names)
                columns[name.c_str()] = result.attr(name.c_str());
            return py::module_::import("awkward").attr("Array")(columns);
        },
        "Generate (S1, S2) for a vector of recoil energies, returned as an awkward\n"
        "array with one record per event.\n"
        "energies has shape (n,) and positions shape (n, 3); float64 numpy arrays are\n"
        "read directly and other inputs (e.g. lists) are converted.",
        py::arg("detector"),
        py::arg("interaction_type"),
        py::arg("energies"),
        py::arg("positions"),
        py::arg("inField") = -1.0,
        py::arg("seed") = 0,
        py::arg("er_yield_params") = default_ERYieldsParam,
        py::arg("nr_yield_params") = default_NRYieldsParam,
        py::arg("width_params") = default_NRERWidthsParam,
        py::arg("s1_mode") = NEST::S1CalculationMode::Hybrid,
        py::arg("s2_mode") = NEST::S2CalculationMode::Full,
        py::arg("calculate_times") = false
    );
}