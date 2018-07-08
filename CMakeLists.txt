cmake_minimum_required(VERSION 2.8.12)
project(nestpy)
# Set source directory
set(SOURCE_DIR "src/nestpy")
# Tell CMake that headers are also in SOURCE_DIR
include_directories(${SOURCE_DIR})
set(SOURCES "${SOURCE_DIR}/math.cpp")

# Generate Python module
add_subdirectory(lib/pybind11)
pybind11_add_module(nestpy ${SOURCES} "${SOURCE_DIR}/bindings.cpp")
