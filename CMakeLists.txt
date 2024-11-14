cmake_minimum_required(VERSION 3.20 FATAL_ERROR)

set(BUILD_TESTING ON)
if (BUILD_TESTING)
    # vcpkg enable testing dependencies
    list(APPEND VCPKG_MANIFEST_FEATURES "tests")
endif ()

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
else ()
    message(WARNING "You are using an unsupported compiler! Compilation has only been tested with Clang and GCC.")
endif ()

add_subdirectory(model)

# Sanitizers for Debug build
include(cmake/sanitizers.cmake)
if (CMAKE_BUILD_TYPE STREQUAL "Debug")
    add_sanitizers()
endif ()

# Sources
find_package(glog REQUIRED)

# Testing
if (BUILD_TESTING)
    include(CTest)
    enable_testing()
    add_subdirectory(tests)
endif ()
