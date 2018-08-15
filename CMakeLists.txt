include(CheckCXXCompilerFlag)
CHECK_CXX_COMPILER_FLAG("-std=c++11" COMPILER_SUPPORTS_CXX11)
CHECK_CXX_COMPILER_FLAG("-std=c++0x" COMPILER_SUPPORTS_CXX0X)
if(COMPILER_SUPPORTS_CXX11)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")
elseif(COMPILER_SUPPORTS_CXX0X)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++0x")
else()
        message(STATUS "The compiler ${CMAKE_CXX_COMPILER} has no C++11 support. Please use a different C++ compiler.")
endif()

set (CMAKE_CXX_STANDARD 11)
cmake_minimum_required(VERSION 2.8.12)
project(nestpy)
# Set source directory
set(SOURCE_DIR "src/nestpy")
# Tell CMake that headers are also in SOURCE_DIR
include_directories(${SOURCE_DIR})
set(SOURCES "${SOURCE_DIR}/NEST.cpp" "${SOURCE_DIR}/NEST.cpp" "${SOURCE_DIR}/RandomGen.cpp"  "${SOURCE_DIR}/VDetector.cpp")
include_directories("${SOURCE_DIR}/include") 

# Generate Python module
add_subdirectory(lib/pybind11)
pybind11_add_module(nestpy ${SOURCES} "${SOURCE_DIR}/bindings.cpp")
