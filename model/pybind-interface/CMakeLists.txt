find_package(Python3 REQUIRED COMPONENTS Interpreter Development)
set(Python_SITEARCH "${VIRTUAL_ENV}/lib/python${Python_VERSION_MAJOR}.${Python_VERSION_MINOR}/site-packages")

set(PYBIND11_FINDPYTHON ON)
find_package(pybind11 REQUIRED)

pybind11_add_module(creepers_lib pybind-module.cpp)

target_link_libraries(creepers_lib PUBLIC creeper-simulation-library Python3::Python)

target_include_directories(creepers_lib PRIVATE ${Python3_INCLUDE_DIRS} ${CMAKE_CURRENT_SOURCE_DIR})
install(TARGETS creepers_lib LIBRARY DESTINATION ${Python3_SITEARCH})
