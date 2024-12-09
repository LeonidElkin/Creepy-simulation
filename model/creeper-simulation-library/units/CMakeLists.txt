add_library(units Unit.cpp Creeper.cpp)

target_include_directories(units PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})

target_link_libraries(units PRIVATE utils fmt::fmt)
