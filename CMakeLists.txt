set (CMAKE_CXX_STANDARD 17)
cmake_minimum_required(VERSION 2.8.12)
project(nestpy)

# Set source directory
set(SOURCE_DIR "lib/nest/src")
# Tell CMake that headers are also in SOURCE_DIR
include_directories(
    "lib/nest/include/NEST/" 
    "lib/nest/include/Detectors"
    "lib/gcem/include"
)
set(SOURCES "${SOURCE_DIR}/NEST.cpp" "${SOURCE_DIR}/RandomGen.cpp"  "${SOURCE_DIR}/VDetector.cpp" "${SOURCE_DIR}/execNEST.cpp" "${SOURCE_DIR}/TestSpectra.cpp" "${SOURCE_DIR}/GammaHandler.cpp" "${SOURCE_DIR}/ValidityTests.cpp")

# Generate Python module
add_subdirectory(lib/pybind11)
pybind11_add_module(nestpy ${SOURCES} "nestpy/bindings.cpp")

