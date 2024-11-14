add_library(creeper-simulation-library Field.cpp Creeper.cpp utils.cpp)

target_include_directories(creeper-simulation-library PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})