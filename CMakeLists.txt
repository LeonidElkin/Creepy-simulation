cmake_minimum_required(VERSION 3.20 FATAL_ERROR)

if (BUILD_TESTING)
    # vcpkg enable testing dependencies
    list(APPEND VCPKG_MANIFEST_FEATURES "tests")
endif ()

project(Creepy-simulation LANGUAGES CXX VERSION 1.0)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(CMAKE_POSITION_INDEPENDENT_CODE ON)

add_subdirectory(model)

# Sanitizers for Debug build
include(cmake/sanitizers.cmake)
if (CMAKE_BUILD_TYPE STREQUAL "Debug")
    add_sanitizers()
endif ()

# Sources
find_package(glog REQUIRED)

# Testing
include(CTest)
if (BUILD_TESTING)
endif ()
