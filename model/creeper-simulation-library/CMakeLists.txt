add_library(creeper-simulation-library Field.cpp Creeper.cpp)

target_include_directories(creeper-simulation-library PUBLIC ${CMAKE_INCLUDE_CURRENT_DIR})