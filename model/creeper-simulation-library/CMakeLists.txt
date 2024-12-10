find_package(OpenMP REQUIRED)
add_library(creeper-simulation-library Field.cpp Creeper.cpp utils.cpp)

target_include_directories(creeper-simulation-library PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})

target_link_libraries(creeper-simulation-library PRIVATE OpenMP::OpenMP_CXX)
target_link_libraries(creeper-simulation-library PRIVATE fmt::fmt)
