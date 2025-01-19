find_package(OpenMP REQUIRED)

add_subdirectory(utils)
add_subdirectory(field)
add_subdirectory(units)

add_library(creeper-simulation-library Simulation.cpp CreepersManager.cpp StevesManager.cpp)

target_include_directories(creeper-simulation-library PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})

target_link_libraries(creeper-simulation-library PUBLIC units)
target_link_libraries(creeper-simulation-library PRIVATE utils OpenMP::OpenMP_CXX)
