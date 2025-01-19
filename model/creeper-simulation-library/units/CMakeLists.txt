add_library(units Unit.cpp Creeper.cpp Steve.cpp)

target_include_directories(units PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})

target_link_libraries(units PUBLIC utils field glog::glog)
