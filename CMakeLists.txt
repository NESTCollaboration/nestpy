set (CMAKE_CXX_STANDARD 17)
cmake_minimum_required(VERSION 3.15)
project(nestpy)

# Set source directory
set(NEST_SOURCE_DIR "${CMAKE_CURRENT_SOURCE_DIR}/lib/nest/src")
set(NESTPY_SOURCE_DIR "${CMAKE_CURRENT_SOURCE_DIR}/src/nestpy")

# Tell CMake that headers are also in SOURCE_DIR
include_directories(
    "lib/nest/include/NEST/" 
    "lib/nest/include/Detectors"
    "lib/gcem/include"
    "include"
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

set(NEST_SOURCES "${NEST_SOURCE_DIR}/NEST.cpp" "${NEST_SOURCE_DIR}/LArNEST.cpp" "${NEST_SOURCE_DIR}/RandomGen.cpp"  "${NEST_SOURCE_DIR}/VDetector.cpp" "${NEST_SOURCE_DIR}/execNEST.cpp" "${NEST_SOURCE_DIR}/TestSpectra.cpp" "${NEST_SOURCE_DIR}/GammaHandler.cpp" "${NEST_SOURCE_DIR}/ValidityTests.cpp")
set(NESTPY_SOURCES "${NESTPY_SOURCE_DIR}/bindings.cpp" "${NESTPY_SOURCE_DIR}/spectra.cpp" "${NESTPY_SOURCE_DIR}/detector.cpp" "${NESTPY_SOURCE_DIR}/array.cpp")



# Generate Python module
add_subdirectory(lib/pybind11)
pybind11_add_module(_nestpy ${NEST_SOURCES} ${NESTPY_SOURCES})

target_compile_definitions(_nestpy
                           PRIVATE NESTPY_VERSION=${NESTPY_VERSION_INFO} NEST_VERSION=${NEST_VERSION})

install(TARGETS _nestpy DESTINATION nestpy)
