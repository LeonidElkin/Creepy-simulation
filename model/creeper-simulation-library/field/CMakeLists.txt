add_library(field FieldParams.cpp)
target_link_libraries(field PUBLIC utils)
target_include_directories(field PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})
