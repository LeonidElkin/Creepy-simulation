add_library(run-test run-test.cpp)
target_link_libraries(run-test PUBLIC GTest::gtest glog::glog)

add_subdirectory(creeper-simulation-library)