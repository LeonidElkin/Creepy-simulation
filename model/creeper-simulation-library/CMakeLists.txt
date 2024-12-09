find_package(OpenMP REQUIRED)

add_subdirectory(utils)
add_subdirectory(units)

add_library(creeper-simulation-library Field.cpp)

target_include_directories(creeper-simulation-library PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})

target_link_libraries(creeper-simulation-library PUBLIC units utils)
target_link_libraries(creeper-simulation-library PRIVATE OpenMP::OpenMP_CXX)