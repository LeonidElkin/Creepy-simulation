add_library(field FieldParams.cpp)
target_link_libraries(field PRIVATE utils)
target_include_directories(field PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})
