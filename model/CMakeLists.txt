cmake_minimum_required(VERSION 3.20 FATAL_ERROR)

option(BUILD_TESTING "enable test" ON)

project(Creepy-simulation LANGUAGES CXX VERSION 1.0)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(CMAKE_POSITION_INDEPENDENT_CODE ON)

if (CMAKE_INSTALL_PREFIX_INITIALIZED_TO_DEFAULT)
    set (CMAKE_INSTALL_PREFIX "${CMAKE_SOURCE_DIR}/dist" CACHE PATH "default install path" FORCE )
endif()

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
else ()
    message(WARNING "You are using an unsupported compiler! Compilation has only been tested with Clang, MSVC and GCC.")
endif ()

# Dependencies
include(FetchContent)

FetchContent_Declare(
        pybind11
        GIT_REPOSITORY https://github.com/pybind/pybind11.git
        GIT_TAG v2.13.6
        OVERRIDE_FIND_PACKAGE
)
FetchContent_MakeAvailable(pybind11)

FetchContent_Declare(
        fmt
        GIT_REPOSITORY https://github.com/fmtlib/fmt.git
        GIT_TAG 11.0.2
        OVERRIDE_FIND_PACKAGE
)
FetchContent_MakeAvailable(fmt)

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
    FetchContent_Declare(
            GTest
            GIT_REPOSITORY https://github.com/google/googletest.git
            GIT_TAG v1.15.2
            OVERRIDE_FIND_PACKAGE
    )

    FetchContent_MakeAvailable(GTest)

    include(CTest)
    enable_testing()
    add_subdirectory(tests)
endif ()
