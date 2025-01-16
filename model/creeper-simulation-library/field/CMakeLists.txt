add_library(field INTERFACE FieldParams.cpp)
target_link_libraries(field INTERFACE utils)
target_include_directories(field INTERFACE ${CMAKE_CURRENT_SOURCE_DIR})
