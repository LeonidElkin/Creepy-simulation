cmake_minimum_required(VERSION 3.20 FATAL_ERROR)

option(BUILD_TESTING "enable test" OFF)

project(Creepy-simulation LANGUAGES CXX VERSION 1.0)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(CMAKE_POSITION_INDEPENDENT_CODE ON)

# Compiler check up
if (CMAKE_CXX_COMPILER_ID STREQUAL "GNU")
    if (CMAKE_CXX_COMPILER_VERSION VERSION_LESS 14.0)
        message(FATAL_ERROR "GCC version 14.0 or higher is required, but ${CMAKE_CXX_COMPILER_VERSION} was given.")
    endif ()
elseif (CMAKE_CXX_COMPILER_ID STREQUAL "Clang")
    if (CMAKE_CXX_COMPILER_VERSION VERSION_LESS 18.0)
        message(FATAL_ERROR "Clang version 18.0 or higher is required, but ${CMAKE_CXX_COMPILER_VERSION} was given.")
    endif ()
elseif (CMAKE_CXX_COMPILER_ID STREQUAL "MSVC")
    if (CMAKE_CXX_COMPILER_VERSION VERSION_LESS 19.40)
        message(FATAL_ERROR "MSVC version 19.40 or higher is required, but ${CMAKE_CXX_COMPILER_VERSION} was given.")
    endif ()
    add_compile_options(/openmp)
else ()
    message(WARNING "You are using an unsupported compiler! Compilation has only been tested with Clang, MSVC and GCC.")
endif ()

find_package(glog REQUIRED)

# Subdirectories
add_subdirectory(creeper-simulation-library)
add_subdirectory(pybind-interface)

# Sanitizers for Debug build
include(cmake/sanitizers.cmake)
if (CMAKE_BUILD_TYPE STREQUAL "Debug")
    add_sanitizers()
endif ()

# Testing
if (BUILD_TESTING)
    include(CTest)
    enable_testing()
    add_subdirectory(tests)
endif ()
