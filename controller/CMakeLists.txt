find_package(Python3  COMPONENTS Interpreter Development REQUIRED)

set(PYBIND11_FINDPYTHON ON)
find_package(pybind11 CONFIG REQUIRED)

pybind11_add_module(field_provider pybind_module.cpp)
target_link_libraries(field_provider PUBLIC creeper-simulation-library)

target_link_libraries(field_provider PRIVATE Python3::Python)

target_include_directories(field_provider PRIVATE ${Python3_INCLUDE_DIRS})

set_target_properties( field_provider
        PROPERTIES
        PREFIX ""
        SUFFIX ".so"
)

target_include_directories(field_provider PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})