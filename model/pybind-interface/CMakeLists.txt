find_package(Python3 REQUIRED COMPONENTS Interpreter Development)

set(PYBIND11_FINDPYTHON ON)
find_package(pybind11 REQUIRED)

pybind11_add_module(creepers pybind-module.cpp)
target_link_libraries(creepers PUBLIC creeper-simulation-library)

target_link_libraries(creepers PRIVATE Python3::Python)

target_include_directories(creepers PRIVATE ${Python3_INCLUDE_DIRS})

target_include_directories(creepers PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})
