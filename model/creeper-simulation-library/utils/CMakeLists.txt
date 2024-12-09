add_library(utils utils.cpp)

target_include_directories(utils PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})
target_link_libraries(utils PRIVATE fmt::fmt)