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

###############        Get NEST version from git        #####################
execute_process(COMMAND git describe --tag
        WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/lib/nest/
        OUTPUT_VARIABLE NEST_VERSION
        OUTPUT_STRIP_TRAILING_WHITESPACE)

function(get_versions versionString version)
    if ("${versionString}" STREQUAL "")
        set(version "0.0.0" PARENT_SCOPE)
        return()
    endif ()

    string(REGEX REPLACE "v([0-9]*)([.][0-9]*[.][0-9]*-?.*)$" "\\1" numbers ${versionString})
    set(major ${numbers})
    string(REGEX REPLACE "v([0-9]*[.])([0-9]*)([.][0-9]*-?.*)$" "\\2" numbers ${versionString})
    set(minor ${numbers})
    string(REGEX REPLACE "v([0-9]*[.][0-9]*[.])([0-9]*)(-?.*)$" "\\2" numbers ${versionString})
    set(patch ${numbers})
    set(version "${major}.${minor}.${patch}" PARENT_SCOPE)
endfunction()

get_versions("${NEST_VERSION}" version)
set(NEST_VERSION ${version})

set(SOURCES "${SOURCE_DIR}/NEST.cpp" "${SOURCE_DIR}/LArNEST.cpp" "${SOURCE_DIR}/RandomGen.cpp"  "${SOURCE_DIR}/VDetector.cpp" "${SOURCE_DIR}/execNEST.cpp" "${SOURCE_DIR}/TestSpectra.cpp" "${SOURCE_DIR}/GammaHandler.cpp" "${SOURCE_DIR}/ValidityTests.cpp")

# Generate Python module
add_subdirectory(lib/pybind11)
pybind11_add_module(nestpy ${SOURCES} "src/nestpy/bindings.cpp")

target_compile_definitions(nestpy
                           PRIVATE NESTPY_VERSION=${NESTPY_VERSION_INFO} NEST_VERSION=${NEST_VERSION})

